import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self,x,y,text,colour,dimmed_colour,size,width,height,Game):
        pg.sprite.Sprite.__init__(self)
        self.pressed = False
        self.image = pg.Surface((width,height))
        self.colour = colour
        self.draw_colour = colour
        self.dimmed_colour = dimmed_colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.size = size
        self.game = Game
        self.text  = text
        self.font = pg.font.Font(None,self.size)
        self.text_surf = self.font.render(self.text,True,(0,0,0)) #this gives all options
        
        self.text_rect = self.text_surf.get_rect()

        

    def draw(self):
        self.rect.center = (self.x,self.y)
        self.text_rect.center = (self.x,self.y)
        pg.draw.rect(self.game.screen,self.draw_colour,self.rect,border_radius= 12)
        self.game.screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.draw_colour = self.dimmed_colour
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                   

                    self.pressed = False
            
            return False
                    
        else:
            self.draw_colour = self.colour
        
        
            