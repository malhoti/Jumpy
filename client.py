from platform import platform
import pygame as pg
import socket

from pygame import time
from platforms import Platform, Spike
from network import Network
from player import Player
from button import Button
import pickle
from settings import *
from solo import Solo
import time



class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        
        
        self.send_more_platforms = False
        self.font_name = pg.font.match_font(font)
        self.p1ready = True
        
        self.player1lost = False
        self.player2lost = False
        


    def new(self):
        
        self.network = Network()
        self.starting_info = self.network.getP() # get the information sent from the server
        self.player = self.starting_info[0]
       
        print("You are player", int(self.player) +1)
        if int(self.player) == 0:
            
            self.player1 = Player(screen_width*0.1,int((7*screen_height)/8),self,green)
            self.player2 = Player(0,screen_height+150,self,red)
        else:
            self.player1 = Player(screen_width*0.9,(7*screen_height)/8,self,red)
            self.player2 = Player(screen_width*0.1,int((7*screen_height)/8),self,green)

        
        platformPos = self.starting_info[1]

        self.totalSprites = pg.sprite.Group() # making sprite groups 
        self.platforms = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        

        self.spike = Spike(0,screen_height*1.25,screen_width,screen_height)
        self.totalSprites.add(self.player1)
        self.totalSprites.add(self.player2)
        self.totalSprites.add(self.spike)
    
        self.spikes.add(self.spike)

        self.score = 0
        

        for i in range(len(platformPos)):

            p = Platform(*platformPos[i])       # *platformPos[i] is the same as plafrom[0],plafrom[1],plafrom[2],plafrom[3]
            self.totalSprites.add(p)
            self.platforms.add(p)
        
        self.show_lobby()

    def run(self):
        self.run = True
        while self.run:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()


    def events(self):
         # his makes you unready so that when sent to the server, it makes you already unready for when the game restarts so it doesnt have to do the check
        
        # Checks if anyone has won or lost first, this is so that if it is the case, then the client can send one last message to the server to let it know that this client lost or won
        if self.player1.rect.bottom >= self.spike.rect.top:
            print("you lost")
            self.player1lost = True

        self.info_to_send=[int(self.player1.position.x), int(self.player1.position.y),self.player1.pushdown,self.p1ready,self.player1lost],self.send_more_platforms
        info_recv = self.network.send((self.info_to_send))  #when you send player1, the network sends player 2 to this client, and viceversa for player2 
        print(info_recv)
        self.send_more_platforms = False 

        
        # changing player 2 attributes when the server sent its details
        try:
            player2Pos = info_recv[0]
            self.player2.position.x = player2Pos[0]
            self.player2.position.y = player2Pos[1] +(self.player1.pushdown-player2Pos[2])
            platformPos = info_recv[1]
            self.player2lost = player2Pos[4]


            for i in range(len(platformPos)):  # 
            
                if not platformPos[i]:
                    pass
                else:
                    p = Platform(platformPos[i][0],platformPos[i][1],platformPos[i][2],platformPos[i][3])      
                    self.totalSprites.add(p)
                    self.platforms.add(p)
        except:
            self.player2lost = True
        


       
        
        self.player2.update()


        if self.player1lost:
            
            self.network.send("endgame")
            self.show_go_screen()

        if self.player2lost:
            #self.p1ready = False
            
            
            self.network.send("endgame")
            self.show_victory_screen()

        for event in pg.event.get():
            if event.type == pg.QUIT:  # if they quit in-game the other person wins
                print('i discoonnected')
                
                self.network.send("endgame")
                
                if self.run:
                    self.run = False
               
            if event.type == pg.KEYDOWN:    
               if event.key == pg.K_SPACE:
                  
                   self.player1.jump()
        
    def update(self):
        self.player1.move()
        
        # what this does, is it only checks collisions whilst falling, not whilst jumping
        if self.player1.velocity.y>= 0 :  
            hits = pg.sprite.spritecollide(self.player1, self.platforms, False)
            if hits :
                if self.player1.position.y < hits[0].rect.bottom:
                    self.player1.position.y = hits[0].rect.top
                    self.player1.velocity.y = 0

        # the spike will slowly get faster and faster!!
        for spike in self.spikes:
            spike.rect.y -= (1)

        #this is going to act like a camera shift when the player reaches around the top of the screen
        #and delete platforms that go off the screen

        #going up
        
        if self.player1.rect.top <= screen_height/4:
            self.player1.pushdown +=  round(abs(self.player1.velocity.y))
            self.player1.position.y += round(abs(self.player1.velocity.y))
            
            for spike in self.spikes:
                spike.rect.y +=  round(abs(self.player1.velocity.y)) 
           
            for platform in self.platforms:
                platform.rect.y += round(abs(self.player1.velocity.y))

        # checks collsions for the platforms     
        hits = pg.sprite.pygame.sprite.spritecollide(spike, self.platforms, False)
        if hits:
            if self.spike.rect.top<hits[0].rect.top:
                hits[0].kill()
                self.score += 1

        # going down
        if self.player1.velocity.y>=0:
            if self.player1.rect.bottom >(7*screen_height)/8:
                self.player1.pushdown -= round(abs(self.player1.velocity.y))
                self.player1.position.y -= round(abs(self.player1.velocity.y))
                
                for spike in self.spikes:
                    spike.rect.y -=  round(abs(self.player1.velocity.y)) 
            
                for platform in self.platforms:
                    platform.rect.y -= round(abs(self.player1.velocity.y))
        
        # make new platforms 

        # this checks wether if there is a platform 1/8 above the screen, if there arent make a new platform, if there are above the 1/8 of screen dont send more platforms
        empty_above = False
        count = 0
        for platform in self.platforms:
            
            if platform.rect.y <screen_height/8 : 
                count += 1

        if count  == 0:
            empty_above = True

        while self.player1.rect.y <screen_height/4 and empty_above: #and len(self.platforms) <10:
            self.send_more_platforms = True
            break
        
        
    def show_menu(self):
        self.screen.fill(bgcolour)
        self.draw_text(TITLE, int(screen_width*0.30) , black,screen_width/2,screen_height/4)
        self.draw_text("USE ARROW KEYS TO MOVE",int(screen_width*0.05),red,screen_width/2,screen_height/2)
        self.solo_button = Button(3*screen_width/8,6*screen_height/8,"SOLO",green,dimmed_green,int(screen_width*0.05),screen_width*0.2,screen_height*0.075,self)
        self.multiplayer_button = Button(5*screen_width/8,6*screen_height/8,"MULTIPLAYER",green,dimmed_green,int(screen_width*0.035),screen_width*0.2,screen_height*0.075,self)
        self.quit_button = Button(4*screen_width/8,7*screen_height/8,"QUIT",red,dimmed_red,int(screen_width*0.05),screen_width*0.2,screen_height*0.075,self)

        self.buttons = []

        self.buttons.append(self.solo_button)
        self.buttons.append(self.multiplayer_button)
        self.buttons.append(self.quit_button)
        #pg.time.delay(500)#adding delay because if you spam a key it can gltich the game
       # if play_button:
       #     self.new()
        self.wait_for_click(self.buttons)

        self.buttons.clear()
        if self.solo_button.pressed :
            return 'solo'
        if self.multiplayer_button.pressed:
            return 'multiplayer'
        if self.quit_button.pressed:
            self.run = False
            quit()
        

    def show_lobby(self):

        self.lobbychecking = True
        self.screen.fill(bgcolour)
        self.draw_text("WAITING IN LOBBY...",70,black,screen_width/2,screen_height/2)
        self.cancel_button = Button(screen_width/2,7*screen_height/8,"CANCEL",red,dimmed_red,20,screen_width*0.2,screen_height*0.1,self)

        
        while self.lobbychecking:
            self.cancel_button.draw()
            self.wait_for_player2()

        

            if self.cancel_button.pressed:
                print("clicked")

                self.network.send("endgame")
                self.lobbychecking = False
                self.show_menu()
                

            

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.lobbychecking = False
                    self.run = False
            pg.display.flip()
        

    def wait_for_click(self,buttons):
        waiting = True
        while waiting:
            
            self.clock.tick(fps)
            for button in buttons:
                button.draw()
            #self.play_button.draw()
           
            
                if button.pressed:
                    waiting = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting = False
                        self.run = False
                        quit()
            
            pg.display.flip()

                
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.run = False
                    quit()
                if event.type == pg.KEYUP:
                    waiting = False


    def wait_for_player2(self):
        self.p1ready = True
        
        
        self.info_to_send=[int(self.player1.position.x), int(self.player1.position.y),self.player1.pushdown,self.p1ready,self.player1lost],self.send_more_platforms
        
        info_recv = self.network.send((self.info_to_send))
        
        
        try:
            if info_recv[0][3]:
                print("other player joined")
                self.lobbychecking = False
                self.run()
        except Exception as e:
            pass
        
        self.clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                self.run = False
            
    
            
    def show_go_screen(self):   
        self.screen.fill(red)
        self.draw_text("YOU LOST", 70, black,screen_width/2,screen_height/4)
        self.draw_text(("Press a key..."+str(self.player)),16,black,screen_width/2,screen_height/2)
        pg.display.flip()
        pg.time.delay(1000)# adding delay so the player has time to see if they lost or not
        self.wait_for_key()
        self.run = False
        
        
    def show_victory_screen(self):
        self.screen.fill(green)
        self.draw_text("YOU WON", 70, black,screen_width/2,screen_height/4)
        self.draw_text(("Press a key..."+str(self.player)),16,black,screen_width/2,screen_height/2)
        
        pg.display.flip()
        pg.time.delay(1000)
        self.wait_for_key()
        self.run = False
        
        
        
    def draw(self):
        
        self.screen.fill(white)
        self.totalSprites.draw(self.screen)
        self.spike.draw(self.screen)
        self.draw_text(str(self.score), 22, red,screen_width-50,30)
        pg.display.update() # updates the whole screen, try to limit the times you update screen as this is the most intensive code. slowing the animation by a lot

    def draw_text(self, text, size, colour, x,y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect=text_surface.get_rect()
        
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)


while True:
    game = Game()
    print("new game")
    game_mode = game.show_menu()
    if game_mode == 'solo':
        solo = Solo()
        solo.new()

    else:
        game.new()
       
    

pg.quit()  