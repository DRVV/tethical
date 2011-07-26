from panda3d.core import loadPrcFile
loadPrcFile("config.prc")
from pandac.PandaModules import *
import direct.directbase.DirectStart
from panda3d.core import *
from direct.task.Task import Task
from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *
import os, sys, json
from copy import deepcopy
import Map, Move, Attack, Character

GAME = ConfigVariableString('game', 'fft').getValue()

LOGIN_MESSAGE = 1
LOGIN_SUCCESS = 2
LOGIN_FAIL = 3
CREATE_PARTY = 4
PARTY_CREATED = 5
GET_MAPS = 6
MAP_LIST = 7
GET_PARTIES = 8
PARTY_LIST = 9
JOIN_PARTY = 10
PARTY_JOINED = 11
START_BATTLE = 12
UPDATE_PARTY = 13
PARTY_UPDATED = 14
GET_WALKABLES = 15
WALKABLES_LIST = 16
GET_PATH = 17
PATH = 18
MOVE_TO = 19
MOVED = 20
MOVED_PASSIVE = 21
WAIT = 22
WAIT_SUCCESS = 23
WAIT_PASSIVE = 24
GET_ATTACKABLES = 25
ATTACKABLES_LIST = 26
ATTACK = 27
ATTACK_SUCCESS = 28
ATTACK_PASSIVE = 29
UPDATE_PARTY_LIST = 30
PARTY_JOIN_FAIL = 31
BATTLE_COMPLETE = 32
GAME_OVER = 33
GET_PASSIVE_WALKABLES = 34
PASSIVE_WALKABLES_LIST = 35

class Server:

    def __init__(self):

        self.activeConnections = []
        self.players = {}
        self.parties = {}
        self.sessions = {}
        self.playersinlobby = []

        self.cManager  = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader   = QueuedConnectionReader(self.cManager, 0)
        self.cWriter   = ConnectionWriter(self.cManager, 0)
        self.cReader.setTcpHeaderSize(4)
        self.cWriter.setTcpHeaderSize(4)

        port = 3001
        if len(sys.argv) > 1:
            port = sys.argv[1]

        self.tcpSocket = self.cManager.openTCPServerRendezvous(port, 10)
        self.cListener.addConnection(self.tcpSocket)
        print "Server listening on port", port

        taskMgr.add(self.tskListenerPolling, "Poll the connection listener", -39)
        taskMgr.add(self.tskReaderPolling, "Poll the connection reader", -40)

    def processData(self, datagram):
        iterator = PyDatagramIterator(datagram)
        source = datagram.getConnection()
        msgID = iterator.getUint8()
        
        if msgID == LOGIN_MESSAGE:

            login = iterator.getString()
            password = iterator.getString()

            if login != password:
                myPyDatagram = PyDatagram()
                myPyDatagram.addUint8(LOGIN_FAIL)
                myPyDatagram.addString('Wrong credentials.')
                self.cWriter.send(myPyDatagram, source)
            elif self.sessions.has_key(source):
                myPyDatagram = PyDatagram()
                myPyDatagram.addUint8(LOGIN_FAIL)
                myPyDatagram.addString('Already logged in.')
                self.cWriter.send(myPyDatagram, source)
            elif login in self.players.keys():
                myPyDatagram = PyDatagram()
                myPyDatagram.addUint8(LOGIN_FAIL)
                myPyDatagram.addString('Username already in use.')
                self.cWriter.send(myPyDatagram, source)
            else:
                self.players[login] = source
                self.sessions[source] = {}
                self.sessions[source]['login'] = login
                print login, 'logged in.'
                myPyDatagram = PyDatagram()
                myPyDatagram.addUint8(LOGIN_SUCCESS)
                self.cWriter.send(myPyDatagram, source)
        
        elif msgID == CREATE_PARTY:

            name = iterator.getString()
            mapname = iterator.getString()
            
            party = {
                'name': name,
                'mapname': mapname,
                'map' : Map.load(mapname),
                'chars': {},
                'log': {},
                'creator': self.sessions[source]['login'],
                'players': [],
            }
            party['players'].append(self.sessions[source]['login'])

            self.parties[name] = party
            self.sessions[source]['party'] = name
            self.sessions[source]['player'] = len(party['players'])-1
            
            self.updateAllPartyLists()
            
            print self.sessions[source]['login'], "created the party", name, "using the map", mapname
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(PARTY_CREATED)
            myPyDatagram.addString32(json.dumps(party))
            self.cWriter.send(myPyDatagram, source)

        elif msgID == GET_MAPS:
            self.playersinlobby.remove(source)

            mapnames = map( lambda m: m.split('.')[0], os.listdir(GAME+'/maps'))

            maps = []
            for mapname in mapnames:
                mp = Map.load(mapname)
                del mp['tiles']
                maps.append(mp)

            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(MAP_LIST)
            myPyDatagram.addString(json.dumps(maps))
            self.cWriter.send(myPyDatagram, source)
        
        elif msgID == GET_PARTIES:
            self.playersinlobby.append(source)

            parties = deepcopy(self.parties)
            for party in parties.values():
                del party['map']['tiles']

            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(PARTY_LIST)
            myPyDatagram.addString32(json.dumps(parties))
            self.cWriter.send(myPyDatagram, source)
        
        elif msgID == JOIN_PARTY:
        
            name = iterator.getString()
            party = self.parties[name]
            
            if len(party['players']) >= len(party['map']['chartiles']):
                parties = deepcopy(self.parties)
                for party in parties.values():
                    del party['map']['tiles']
                myPyDatagram = PyDatagram()
                myPyDatagram.addUint8(PARTY_JOIN_FAIL)
                myPyDatagram.addString('Party '+name+' is full.')
                myPyDatagram.addString32(json.dumps(parties))
                self.cWriter.send(myPyDatagram, source)
            else:
                party['players'].append(self.sessions[source]['login'])
                self.sessions[source]['party'] = name
                self.sessions[source]['player'] = len(party['players'])-1
                self.playersinlobby.remove(source)

                print self.sessions[source]['login'], "joined the party", name
                myPyDatagram = PyDatagram()
                myPyDatagram.addUint8(PARTY_JOINED)
                myPyDatagram.addString32(json.dumps(party))
                self.cWriter.send(myPyDatagram, source)
                
                for teamid,team in enumerate(party['map']['chartiles']):
                    for chartile in team:
                        x = int(chartile['x'])
                        y = int(chartile['y'])
                        z = int(chartile['z'])
                        direction = int(chartile['direction'])
                        charid = str(x)+str(y)+str(z)
                        party['map']['tiles'][x][y][z]['char'] = charid
                        party['chars'][charid] = Character.Random(charid, teamid, direction)
                
                if len(party['players']) == len(party['map']['chartiles']):
                    for player in party['players']:
                        myPyDatagram = PyDatagram()
                        myPyDatagram.addUint8(START_BATTLE)
                        myPyDatagram.addString32(json.dumps(party))
                        self.cWriter.send(myPyDatagram, self.players[player])

                self.updateAllPartyLists()

        elif msgID == UPDATE_PARTY:

            party = self.parties[self.sessions[source]['party']]
            chars = party['chars']
            
            aliveteams = {}
            for charid in chars.keys():
                if chars[charid]['hp'] > 0:
                    if aliveteams.has_key(chars[charid]['team']):
                        aliveteams[chars[charid]['team']] = aliveteams[chars[charid]['team']] + 1
                    else:
                        aliveteams[chars[charid]['team']] = 1
            if len(aliveteams) < 2:
                for client in party['players']:
                    if source == self.players[client]:
                        myPyDatagram = PyDatagram()
                        myPyDatagram.addUint8(BATTLE_COMPLETE)
                        self.cWriter.send(myPyDatagram, self.players[client])
                    else:
                        myPyDatagram = PyDatagram()
                        myPyDatagram.addUint8(GAME_OVER)
                        self.cWriter.send(myPyDatagram, self.players[client])
                del self.parties[self.sessions[source]['party']]
                self.updateAllPartyLists()
                return

            for charid in chars.keys():
                party['yourturn'] = int(chars[charid]['team']) == int(self.sessions[source]['player'])
                if chars[charid]['active']:
                    myPyDatagram = PyDatagram()
                    myPyDatagram.addUint8(PARTY_UPDATED)
                    myPyDatagram.addBool(party['yourturn'])
                    myPyDatagram.addString32(json.dumps(chars))
                    self.cWriter.send(myPyDatagram, source)
                    return
            
            while True:
                for charid in chars.keys():
                    char = chars[charid]
                    char['ct'] = char['ct'] + char['speed']
                    if char['ct'] >= 100:
                        if char['hp'] > 0:
                            char['active'] = True
                            char['canmove'] = True
                            char['canact'] = True
                            party['yourturn'] = int(chars[charid]['team']) == int(self.sessions[source]['player'])
                            myPyDatagram = PyDatagram()
                            myPyDatagram.addUint8(PARTY_UPDATED)
                            myPyDatagram.addBool(party['yourturn'])
                            myPyDatagram.addString32(json.dumps(chars))
                            self.cWriter.send(myPyDatagram, source)
                            return
                        else:
                            char['ct'] = 0

        elif msgID == GET_WALKABLES:
        
            charid = iterator.getString()
            party = self.parties[self.sessions[source]['party']]
            walkables = Move.GetWalkables( party, charid )
            
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(WALKABLES_LIST)
            myPyDatagram.addString(charid)
            myPyDatagram.addString(json.dumps(walkables))
            self.cWriter.send(myPyDatagram, source)
        
        elif msgID == GET_PASSIVE_WALKABLES:
        
            charid = iterator.getString()
            party = self.parties[self.sessions[source]['party']]
            walkables = Move.GetWalkables( party, charid )
            
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(PASSIVE_WALKABLES_LIST)
            myPyDatagram.addString(charid)
            myPyDatagram.addString(json.dumps(walkables))
            self.cWriter.send(myPyDatagram, source)
        
        elif msgID == GET_PATH:
        
            charid = iterator.getString()
            x2 = iterator.getUint8()
            y2 = iterator.getUint8()
            z2 = iterator.getUint8()
            
            party = self.parties[self.sessions[source]['party']]
            
            orig = Character.Coords( party, charid )
            x1 = orig[0]
            y1 = orig[1]
            z1 = orig[2]
            
            path = Move.GetPath( party, charid, x1, y1, z1, x2, y2, z2 )
            
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(PATH)
            myPyDatagram.addString(charid)
            myPyDatagram.addString(json.dumps(orig))
            myPyDatagram.addUint8(party['chars'][charid]['direction'])
            myPyDatagram.addString(json.dumps((x2,y2,z2)))
            myPyDatagram.addString(json.dumps(path))
            self.cWriter.send(myPyDatagram, source)
        
        elif msgID == MOVE_TO:
            
            charid = iterator.getString()
            x2 = iterator.getUint8()
            y2 = iterator.getUint8()
            z2 = iterator.getUint8()
            
            party = self.parties[self.sessions[source]['party']]
            
            orig = Character.Coords( party, charid )
            x1 = orig[0]
            y1 = orig[1]
            z1 = orig[2]

            path = Move.GetPath( party, charid, x1, y1, z1, x2, y2, z2 )
            walkables = Move.GetWalkables( party, charid )

            del party['map']['tiles'][x1][y1][z1]['char']
            party['map']['tiles'][x2][y2][z2]['char'] = charid

            party['chars'][charid]['direction'] = Move.GetNewDirection( x1, y1, x2, y2 )
            party['chars'][charid]['canmove'] = False
            
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(MOVED)
            myPyDatagram.addString(charid)
            myPyDatagram.addUint8(x2)
            myPyDatagram.addUint8(y2)
            myPyDatagram.addUint8(z2)
            self.cWriter.send(myPyDatagram, source)
            
            for playerid,playerlogin in enumerate(party['players']):
                if playerid != self.sessions[source]['player']:
                    myPyDatagram = PyDatagram()
                    myPyDatagram.addUint8(MOVED_PASSIVE)
                    myPyDatagram.addString(charid)
                    myPyDatagram.addString(json.dumps(walkables))
                    myPyDatagram.addString(json.dumps(path))
                    self.cWriter.send(myPyDatagram, self.players[playerlogin])

        elif msgID == WAIT:
        
            charid = iterator.getString()
            direction = iterator.getUint8()
            
            party = self.parties[self.sessions[source]['party']]
            char = party['chars'][charid]

            if char['canmove'] and char['canact']:
                char['ct'] = char['ct'] - 60
            elif char['canmove'] or char['canact']:
                char['ct'] = char['ct'] - 80
            else:
                char['ct'] = char['ct'] - 100

            char['direction'] = direction

            char['active'] = False
            char['canmove'] = False
            char['canact'] = False
            
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(WAIT_SUCCESS)
            self.cWriter.send(myPyDatagram, source)

            for playerid,playerlogin in enumerate(party['players']):
                if playerid != self.sessions[source]['player']:
                    myPyDatagram = PyDatagram()
                    myPyDatagram.addUint8(WAIT_PASSIVE)
                    myPyDatagram.addString(charid)
                    myPyDatagram.addUint8(direction)
                    self.cWriter.send(myPyDatagram, self.players[playerlogin])

        elif msgID == GET_ATTACKABLES:
        
            charid = iterator.getString()
            
            party = self.parties[self.sessions[source]['party']]
            
            attackables = Attack.GetAttackables( party, charid )
            
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(ATTACKABLES_LIST)
            myPyDatagram.addString(charid)
            myPyDatagram.addString(json.dumps(attackables))
            self.cWriter.send(myPyDatagram, source)

        elif msgID == ATTACK:
        
            charid1 = iterator.getString()
            charid2 = iterator.getString()
            party = self.parties[self.sessions[source]['party']]
            char1 = party['chars'][charid1]
            char2 = party['chars'][charid2]
            
            damages = char1['pa'] * char1['br'] / 100 * char1['pa']
            
            char2['hp'] = char2['hp'] - damages*4
            if char2['hp'] < 0:
                char2['hp'] = 0
            
            char1['canact'] = False
            
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(ATTACK_SUCCESS)
            myPyDatagram.addString(charid1)
            myPyDatagram.addString(charid2)
            myPyDatagram.addUint8(damages)
            self.cWriter.send(myPyDatagram, source)
            
            attackables = Attack.GetAttackables( party, charid1 )
            
            for playerid,playerlogin in enumerate(party['players']):
                if playerid != self.sessions[source]['player']:
                    myPyDatagram = PyDatagram()
                    myPyDatagram.addUint8(ATTACK_PASSIVE)
                    myPyDatagram.addString(charid1)
                    myPyDatagram.addString(charid2)
                    myPyDatagram.addUint8(damages)
                    myPyDatagram.addString(json.dumps(attackables))
                    self.cWriter.send(myPyDatagram, self.players[playerlogin])

    def updateAllPartyLists(self):
        parties = deepcopy(self.parties)
        for party in parties.values():
            del party['map']['tiles']

        for player in self.playersinlobby:
            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(UPDATE_PARTY_LIST)
            myPyDatagram.addString32(json.dumps(parties))
            self.cWriter.send(myPyDatagram, player)

    def tskListenerPolling(self, taskdata):
        if self.cListener.newConnectionAvailable():

            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
     
            if self.cListener.getNewConnection(rendezvous, netAddress, newConnection):
                newConnection = newConnection.p()
                self.activeConnections.append(newConnection)
                self.cReader.addConnection(newConnection)
                print 'A new client is connected', newConnection
        return Task.cont

    def tskReaderPolling(self, taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                self.processData(datagram)
        return Task.cont

Server()
run()

