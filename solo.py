from platform import platform
import pygame as pg

from pygame import time
from platforms import Platform, Spike

from player import Player
from button import Button

from settings import *
import time
import random
from os import path


class Solo:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(font)
        self.load_data()
    
    def load_data(self):
        try:
            self.directory = path.dirname(__file__)
            with open(path.join(self.directory,HIGHSCORE_FILE),'r') as f:
                try:
                    self.highscore = int(f.read())
                except:
                    self.highscore = 0
            f.close()
        except:
            with open(HIGHSCORE_FILE,'w') as f:
                self.highscore = 0
            f.close()
     
    def new(self):
        self.score = 0
        self.spike_speed = 1
        self.start_time = time.time()

        self.platform_width = int(screen_width*0.11)
        self.platform_height = int(screen_width*0.05)
        
        self.player = Player(screen_width/2,screen_height-100,self,green)
       
        self.totalSprites = pg.sprite.Group() # making sprite groups 
        self.platforms = pg.sprite.Group()
        self.spikes = pg.sprite.Group()


        self.spike = Spike(0,screen_height+200,screen_width,screen_height)

        self.totalSprites.add(self.player)
        self.totalSprites.add(self.spike)
        self.spikes.add(self.spike)
        

        start_plat=[[0,int((7*screen_height)/8),screen_width,200]]
        for i in range(START_plat_num-1):
                start_plat.append(self.make_platform(True,i))
              
        for platform in start_plat:
            platform = Platform(*platform)
            self.platforms.add(platform)
            self.totalSprites.add(platform)

   
        self.run()

    def run(self):
        self.run = True
        while self.run:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()


    def events(self):
        if self.player.rect.bottom >= self.spike.rect.top:
            print("you lost")
            self.show_end_screen()
       

        for event in pg.event.get():
            if event.type == pg.QUIT:  # if they quit in-game the other person wins
            
                if self.run:
                    self.run = False
               
            if event.type == pg.KEYDOWN:    
               if event.key == pg.K_UP:
                  
                   self.player.jump()
        
    def update(self):
        self.player.move()
        
        # what this does, is it only checks collisions whilst falling, not whilst jumping
        if self.player.velocity.y>= 0 :  
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits :
                if self.player.position.y < hits[0].rect.bottom:
                    self.player.position.y = hits[0].rect.top
                    self.player.velocity.y = 0

        # the spike will slowly get faster and faster!!
        for spike in self.spikes:
            if self.spike_speed <=4 :
                self.end_time = time.time()
                elapsed_time = self.end_time - self.start_time
                
                if int(elapsed_time) >= 18: 
                    self.start_time = self.end_time
                    self.spike_speed += 1
            
            spike.rect.y -= (self.spike_speed)

        #this is going to act like a camera shift when the player reaches around the top of the screen
        #and delete platforms that go off the screen

        #going up
        
        if self.player.rect.top <= screen_height/4:
            self.player.position.y += round(abs(self.player.velocity.y))
            for spike in self.spikes:
                spike.rect.y +=  round(abs(self.player.velocity.y))
            for platform in self.platforms:
                platform.rect.y += round(abs(self.player.velocity.y))
                
                    
        for platform in self.platforms:
                
                if platform.rect.top >= self.spike.rect.top:
                    platform.kill()
                    self.score += 1
        # going down
        if self.player.velocity.y>=0:
            if self.player.rect.bottom >(7*screen_height)/8:
                self.player.position.y -= round(abs(self.player.velocity.y))
                for spike in self.spikes:
                    spike.rect.y -=  round(abs(self.player.velocity.y)) 
                for platform in self.platforms:
                    platform.rect.y -= round(abs(self.player.velocity.y))
        
        # make new platforms 

        # this checks wether if there is a platform 1/8 above the screen, if there arent make a new platform, if there are above the 1/8 of screen dont send more platforms
        empty_above = False
        count = 0
        
        for platform in self.platforms:
            
            if platform.rect.y <screen_height/8 : 
                count += 1

        if count  == 0:
            empty_above = True

        while self.player.rect.y <screen_height/4 and empty_above: #and len(self.platforms) <10:
            start_plat=[]
            start_plat.append(self.make_platform(False,0))
              
            for platform in start_plat:
                platform = Platform(*platform)
                self.platforms.add(platform)
                self.totalSprites.add(platform)
                
            break
        
    def make_platform(self,onscreen,i):
        if onscreen:
            #int (screen_height*0.025)
            platform = [random.randint(0,screen_width-self.platform_width),int(i*(screen_height/START_plat_num)),self.platform_width,self.platform_height] 

        else:
            try:
                yrange =  random.randint(int(-screen_height*0.06875),int(-screen_height*0.05)) # make platform out of screen
                platform= [random.randint(0,screen_width-self.platform_width), yrange,self.platform_width,self.platform_height] 
            except:
                pass

        return platform




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


    
            
    
            
    def show_end_screen(self):   
        self.screen.fill(bgcolour)
        self.draw_text("GAME OVER", int(screen_width *0.1), black,screen_width/2,screen_height/4)
        self.draw_text("Your Score:"+str(self.score),int(screen_width*0.1),black,screen_width/2,5*screen_height/8)
        self.draw_text(("Press a key"),int(screen_width*0.05),black,screen_width/2,screen_height/2)
        if self.score > self.highscore:
            
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE",int(screen_width*0.1),black,screen_width/2,6*screen_height/8)
            with open(path.join(self.directory, HIGHSCORE_FILE), 'w') as f: # saving score on file
                f.write(str(self.score))
            f.close()
        else:
            self.draw_text("Highscore:" + str(self.highscore),int(screen_width*0.1),black,screen_width/2,6*screen_height/8)

        pg.display.flip()
        pg.time.delay(1000)# adding delay so the player has time to see if they lost or not
        self.wait_for_key()
        self.run = False
        
        

        
    def draw(self):
        
        self.screen.fill(white)
        self.totalSprites.draw(self.screen)
        self.spikes.draw(self.screen)
        self.draw_text(str(self.score), 22, red,screen_width-50,30)
        pg.display.update() # updates the whole screen, try to limit the times you update screen as this is the most intensive code. slowing the animation by a lot

    def draw_text(self, text, size, colour, x,y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect=text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)



       
    

pg.quit()  