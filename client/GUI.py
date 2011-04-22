import direct.directbase.DirectStart
from direct.showbase import DirectObject
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

u = 1.0/128.0
hover_snd = base.loader.loadSfx("sounds/hover.ogg")
clicked_snd = base.loader.loadSfx("sounds/clicked.ogg")
cancel_snd = base.loader.loadSfx("sounds/cancel.ogg")
scale = u*12.0
font = loader.loadFont('fonts/fft.egg')

class Background(DirectObject.DirectObject):

    def __init__(self, command):
        
        tex = loader.loadTexture('textures/gui/loadingbackground.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        base.setBackgroundColor(.03125, .03125, .03125)

        self.frame = DirectFrame( color = (1, 1, 1, 1), frameTexture = tex, frameSize = ( -2.2, 2.2, -2.2, 2.2 ), scale = 10 )

        seq = Sequence()
        i = LerpScaleInterval(self.frame, 0.1, 1, startScale=10 )
        seq.append(i)
        seq.append( Wait(0.5) )
        seq.append( Func(command) )
        seq.start()

class LoginWindow(DirectObject.DirectObject):

    def __init__(self, command):
        
        tex = loader.loadTexture('textures/gui/login_window.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame( frameTexture = tex, color = (1, 1, 1, 1), frameSize = ( -.5, .5, -.25, .25 ), scale = 0.1 )
        self.frame.setTransparency(True)

        self.loginLabel = DirectLabel(
            text = 'Username:',
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.0625,.3125,.5,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.loginLabel.setPos(-u*50, 0, u*3)

        self.loginEntry = DirectEntry(
            color = (.62, .6, .5, 0),
            scale = scale,
            numLines = 1,
            focus = 1,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            parent = self.frame
        )
        self.loginEntry.setPos(-u*6, 0, u*3)

        self.passwordLabel = DirectLabel(
            text = 'Password:',
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.0625,.3125,.5,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.passwordLabel.setPos(-u*50, 0, -u*13)

        self.passwordEntry = DirectEntry(
            color = (.62, .6, .5, 0),
            scale = scale,
            numLines = 1,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            obscured = True,
            parent = self.frame
        )
        self.passwordEntry.setPos(-u*6, 0, -u*13)

        connectButton = DirectButton(
            scale = scale,
            text  = ("Connect", "Connect", "Connect", "disabled"),
            command = command,
            color = (.62, .6, .5, 1),
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            rolloverSound = hover_snd,
            clickSound = clicked_snd,
            pressEffect = 0,
            pad = (.15,.15),
            parent = self.frame
        )
        connectButton.setPos(u*38, 0, -u*40)

        seq = Sequence()
        i = LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1 )
        seq.append(i)
        seq.start()

    def commandanddestroy(self, command):
        seq = Sequence()
        i = LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1 )
        seq.append(i)
        seq.append( Func(self.frame.destroy) )
        seq.append( Wait(0.5) )
        seq.append( Func(command) )
        seq.start()

class PartyCreationWindow(DirectObject.DirectObject):

    def __init__(self, command):

        tex = loader.loadTexture('textures/gui/newparty_window.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame( frameTexture = tex, color = (1, 1, 1, 1), frameSize = ( -1, 1, -.25, .25 ), scale=0.1 )
        self.frame.setTransparency(True)
        self.frame.setPos(0, 0, -u*80)

        self.nameEntry = DirectEntry(
            color = (0,0,0,0),
            scale = scale,
            numLines = 1,
            focus = 1,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            parent = self.frame,
        )
        self.nameEntry.setPos(-u*93, 0, -u*7)

        self.mapOptionMenu = DirectOptionMenu(
            text = "options",
            scale = scale, 
            items = [ "Test City", "Battle Arena" ],
            highlightColor = ( 0.65, 0.65, 0.65, 1 ),
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            rolloverSound = hover_snd,
            clickSound = clicked_snd,
            pressEffect = 0,
            parent = self.frame,
        )
        self.mapOptionMenu.setPos(-u*10, 0, -u*7)
        
        button = DirectButton(
            text  = ("Create", "Create", "Create", "disabled"),
            scale = scale,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame,
            rolloverSound = hover_snd,
            clickSound = clicked_snd,
            pressEffect = 0,
            command = command
        )
        button.setPos(u*70, 0, -u*7)
        
        seq2 = Sequence()
        i2 = LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1 )
        seq2.append(i2)
        seq2.start()

class PartyListWindow(DirectObject.DirectObject):

    def __init__(self, command, command2):

        self.command2 = command2

        tex = loader.loadTexture('textures/gui/parties_window.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)
    
        self.frame = DirectFrame( frameTexture = tex, color = (1, 1, 1, 1), frameSize = ( -1, 1, -1, 1 ), scale=0.1 )
        self.frame.setTransparency(True)
        self.frame.setPos(0, 0, u*21)
        
        seq = Sequence()
        i = LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1 )
        seq.append(i)
        seq.append(Func(command))
        seq.start()

    def refresh(self, parties):
    
        for child in self.frame.getChildren():
            child.destroy()

        for i,key in enumerate(parties):
            nameLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['name'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            nameLabel.setPos(-u*93, 0, u*49 - i*u*16)

            creatorLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['creator'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            creatorLabel.setPos(-u*30, 0, u*49 - i*u*16)

            mapLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['map']['name'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            mapLabel.setPos(u*20, 0, u*49 - i*u*16)
            
            joinButton = DirectButton(
                text  = ("Join", "Join", "Join", "Full"),
                command = self.command2,
                extraArgs = [key],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                rolloverSound = hover_snd,
                clickSound = clicked_snd,
                pressEffect = 0,
                parent = self.frame
            )
            joinButton.setPos(u*80, 0, u*49 - i*u*16)

            if parties[key].has_key('player1') and parties[key].has_key('player2'):
                joinButton['state'] = DGG.DISABLED

class Menu(DirectObject.DirectObject):

    def __init__(self, char, movecommand, attackcommand, waitcommand, cancelcommand):

        self.offset = 22
        self.height = 16
        self.index = 0
        self.cancelcommand = cancelcommand

        self.buttons = [
            { 'text': 'Move',   'enabled': char['canmove'], 'pos': (-u*36.5,0,u*(self.offset-self.height*0)), 'command': movecommand   },
            { 'text': 'Attack', 'enabled': char['canact' ], 'pos': (-u*36.5,0,u*(self.offset-self.height*1)), 'command': attackcommand },
            { 'text': 'Wait',   'enabled': True           , 'pos': (-u*36.5,0,u*(self.offset-self.height*2)), 'command': waitcommand   },
            { 'text': 'Status', 'enabled': False          , 'pos': (-u*36.5,0,u*(self.offset-self.height*3)), 'command': cancelcommand },
        ]

        menutexture = loader.loadTexture('textures/gui/menu.png')
        menutexture.setMagfilter(Texture.FTNearest)
        menutexture.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture('textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = menutexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.25, .25, -.5, .5 ),
            pos = (.75, 0, 0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -u*8, u*8, -u*8, u*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (-u*25, 0, u*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (.375,.34375,.28125,1)
        
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept("space", self.onCrossClicked)
        self.accept("b",    self.onCircleClicked)
        self.accept("arrow_down",        lambda: self.updateIndex( 1))
        self.accept("arrow_down-repeat", lambda: self.updateIndex( 1))
        self.accept("arrow_up",          lambda: self.updateIndex(-1))
        self.accept("arrow_up-repeat",   lambda: self.updateIndex(-1))

    def updateIndex(self, direction):
        hover_snd.play()
        next = self.index + direction
        if next == len(self.buttons):
            next = 0
        if next == -1:
            next = len(self.buttons)-1
        self.hand.setPos(self.buttons[next]['pos'])
        self.index = next

    def onCircleClicked(self):
        if self.buttons[self.index]['enabled']:
            clicked_snd.play()
            self.commandAndDestroy(self.buttons[self.index]['command'])

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcommand)

    def commandAndDestroy(self,command):
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(command))
        seq.start()

class MoveCheck(DirectObject.DirectObject):

    def __init__(self, command, cancelcommand):

        self.offset = -10
        self.height = 16
        self.index = 0
        self.cancelcommand = cancelcommand

        self.buttons = [
            { 'text': 'Yes',   'enabled': True, 'pos': (u*45.5,0,u*(self.offset-self.height*0)), 'command': command       },
            { 'text': 'No',    'enabled': True, 'pos': (u*45.5,0,u*(self.offset-self.height*1)), 'command': cancelcommand },
        ]

        tex = loader.loadTexture('textures/gui/move_check.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture('textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -1, 1, -.5, .5 ),
            pos = (0, 0, 0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -u*8, u*8, -u*8, u*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

        messageLabel = DirectLabel(
            color = (0,0,0,0),
            text = 'Are you sure you want to move here?',
            scale = scale,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame,
            pos = (-u*75, 0, u*19)
        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (u*57, 0, u*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (.375,.34375,.28125,1)

        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept("space", self.onCrossClicked)
        self.accept("b",    self.onCircleClicked)
        self.accept("arrow_down",        lambda: self.updateIndex( 1))
        self.accept("arrow_down-repeat", lambda: self.updateIndex( 1))
        self.accept("arrow_up",          lambda: self.updateIndex(-1))
        self.accept("arrow_up-repeat",   lambda: self.updateIndex(-1))

    def updateIndex(self, direction):
        hover_snd.play()
        next = self.index + direction
        if next == len(self.buttons):
            next = 0
        if next == -1:
            next = len(self.buttons)-1
        self.hand.setPos(self.buttons[next]['pos'])
        self.index = next

    def onCircleClicked(self):
        if self.buttons[self.index]['enabled']:
            clicked_snd.play()
            self.commandAndDestroy(self.buttons[self.index]['command'])

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcommand)

    def commandAndDestroy(self,command):
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(command))
        seq.start()

class AttackCheck(DirectObject.DirectObject):

    def __init__(self, command, cancelcommand):

        self.offset = -18
        self.height = 16
        self.index = 0
        self.cancelcommand = cancelcommand

        self.buttons = [
            { 'text': 'Execute', 'enabled': True, 'pos': (-u*8.5,0,u*(self.offset-self.height*0)), 'command': command       },
            { 'text': 'Quit',    'enabled': True, 'pos': (-u*8.5,0,u*(self.offset-self.height*1)), 'command': cancelcommand },
        ]

        tex = loader.loadTexture('textures/gui/attack_check.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture('textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.5, .5, -.5, .5 ),
            pos = (0, 0, 0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -u*8, u*8, -u*8, u*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

# TODO: Fix line height
#        messageLabel = DirectLabel(
#            color = (0,0,0,0),
#            text = 'Executing action.\nOK?',
#            scale = scale,
#            text_font = font,
#            text_fg = (.1875,.15625,.125,1),
#            text_shadow = (.5,.46484375,.40625,1),
#            text_align = TextNode.ALeft,
#            parent = self.frame,
#            pos = (-u*33, 0, u*27)
#        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (u*3, 0, u*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (.375,.34375,.28125,1)

        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept("space", self.onCrossClicked)
        self.accept("b",    self.onCircleClicked)
        self.accept("arrow_down",        lambda: self.updateIndex( 1))
        self.accept("arrow_down-repeat", lambda: self.updateIndex( 1))
        self.accept("arrow_up",          lambda: self.updateIndex(-1))
        self.accept("arrow_up-repeat",   lambda: self.updateIndex(-1))

    def updateIndex(self, direction):
        hover_snd.play()
        next = self.index + direction
        if next == len(self.buttons):
            next = 0
        if next == -1:
            next = len(self.buttons)-1
        self.hand.setPos(self.buttons[next]['pos'])
        self.index = next

    def onCircleClicked(self):
        if self.buttons[self.index]['enabled']:
            clicked_snd.play()
            self.commandAndDestroy(self.buttons[self.index]['command'])

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcommand)

    def commandAndDestroy(self,command):
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(command))
        seq.start()

class Help(DirectObject.DirectObject):

    def __init__(self, message, command):

        self.command = command

        tex = loader.loadTexture('textures/gui/'+message+'.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -1.0, 1.0, -.25, .25 ),
            pos = (0, 0, .25),
            scale = 0.1,
        )
        self.frame.setTransparency(True)
        
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept("b", self.onCircleClicked )

    def onCircleClicked(self):
        clicked_snd.play()
        self.commandAndDestroy(self.command)

    def commandAndDestroy(self, command):
        clicked_snd.play()
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(command))
        seq.start()

class CharCard:

    def __init__(self, char):
        tex = loader.loadTexture('textures/gui/char_card1.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.5, .5, -.25, .25 )
        )
        self.frame.setTransparency(True)
        self.frame.setPos(-2, 0, -u*85)
        
        facetex = loader.loadTexture('textures/sprites/'+char['sprite']+'_face.png')
        facetex.setMagfilter(Texture.FTNearest)
        facetex.setMinfilter(Texture.FTNearest)
        
        self.face = DirectFrame(
            frameTexture = facetex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( 0, u*32, 0, u*64 ),
            parent = self.frame
        )
        self.face.setPos(-u*59, 0, -u*31)
        
        tex2 = loader.loadTexture('textures/gui/char_card2.png')
        tex2.setMagfilter(Texture.FTNearest)
        tex2.setMinfilter(Texture.FTNearest)

        self.frame2 = DirectFrame(
            frameTexture = tex2, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.5, .5, -.25, .25 ),
            parent = self.frame
        )
        self.frame2.setTransparency(True)
        
        i1 = LerpPosInterval(self.frame, 0.2, (-u*55,0,-u*85), (-2,0,-u*85))
        s = Sequence(i1)
        s.start()

    def hide(self):
        if self.frame:
            i1 = LerpPosInterval(self.frame, 0.2, (-2,0,-u*85), (-u*55,0,-u*85))
            i2 = Func( self.frame.destroy )
            s = Sequence(i1,i2)
            s.start()

class CharCard2:

    def __init__(self, char):
        blacktex = loader.loadTexture('textures/gui/black.png')
        blacktex.setMagfilter(Texture.FTNearest)
        blacktex.setMinfilter(Texture.FTNearest)

        self.blackframe = DirectFrame(frameTexture = blacktex, 
                                 frameColor=(1, 1, 1, 1),
                                 frameSize = ( -1, 1, -.5, .5 ))
        self.blackframe.reparentTo(render2d)
        self.blackframe.setTransparency(True)
        self.blackframe.setPos(0, 0, u*-85)

        tex = loader.loadTexture('textures/gui/char_card3.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.5, .5, -.25, .25 )
        )
        self.frame.setTransparency(True)
        self.frame.setPos(2, 0, -u*85)

        self.name = DirectLabel(
            text = char['name'],
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.name.setPos(-u*33, 0, u*12)

        self.name = DirectLabel(
            text = char['job'],
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.name.setPos(-u*33, 0, -u*4)

        teamcolors = ['','blue','red']
        ledtex = loader.loadTexture('textures/gui/char_card_'+teamcolors[int(char['team'])]+'.png')
        ledtex.setMagfilter(Texture.FTNearest)
        ledtex.setMinfilter(Texture.FTNearest)

        self.led = DirectFrame(
            frameTexture = ledtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.0625, .0625, -.0625, .0625 ),
            parent = self.frame
        )
        self.led.setTransparency(True)
        self.led.setPos(-u*49, 0, u*18)

        signs = ['aries','scorpio']
        signtex = loader.loadTexture('textures/gui/'+signs[int(char['sign'])]+'.png')
        signtex.setMagfilter(Texture.FTNearest)
        signtex.setMinfilter(Texture.FTNearest)

        self.sign = DirectFrame(
            frameTexture = signtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.125, .125, -.125, .125 ),
            parent = self.frame
        )
        self.sign.setTransparency(True)
        self.sign.setPos(-u*42, 0, -u*12)

        i1 = LerpScaleInterval(self.blackframe, 0.1, (1,1,1), (1,1,0))
        i2 = LerpColorInterval(self.blackframe, 0.1, (1,1,1,1), (1,1,1,0))
        i3 = LerpPosInterval(  self.frame,      0.2, (u*63,0,-u*85), (2,0,-u*85))
        p1 = Parallel(i1,i2,i3)
        s = Sequence(p1)
        s.start()

    def hide(self):
        if self.frame:
            i1 = LerpScaleInterval(self.blackframe, 0.1, (1,1,0), (1,1,1))
            i2 = LerpColorInterval(self.blackframe, 0.1, (1,1,1,0), (1,1,1,1))
            i3 = LerpPosInterval(  self.frame,      0.2, (2,0,-u*85), (.5,0,-u*85))
            p1 = Parallel(i1,i2,i3)
            i4 = Func( self.blackframe.destroy )
            i5 = Func( self.frame.destroy )
            s = Sequence(p1,i4,i5)
            s.start()

