from direct.interval.IntervalGlobal import Sequence, Func, Wait
import json

def execute(client, iterator):
    charid = iterator.getString()
    targetid = iterator.getString()
    damages = iterator.getUint8()
    attackables = json.loads(iterator.getString())

    print damages
    target = client.party['chars'][targetid]
    target['hp'] = target['hp'] - damages
    if target['hp'] < 0:
        target['hp'] = 0

    client.setPhase('animation')
    seq = Sequence()
    seq.append( Func(client.matrix.setupAttackableZone, charid, attackables) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.updateCursorPos, client.matrix.getCharacterCoords(targetid)) )
    seq.append( Func(client.camhandler.move, client.battleGraphics.logic2terrain(client.matrix.getCharacterCoords(targetid))) )
    seq.append( Wait(0.5) )
    seq.append( client.getCharacterAttackSequence(charid, targetid) )
    seq.append( Func(client.camhandler.move, client.battleGraphics.logic2terrain(client.matrix.getCharacterCoords(charid))) )
    seq.append( Func(client.setPhase, 'listen') )
    seq.start()