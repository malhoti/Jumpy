import pygame 
from settings import *
vec = pygame.math.Vector2 # vectors for easier handling when creating positions

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,game,colour):
        pygame.sprite.Sprite.__init__(self)
        # self.x = x
        # self.y = y
        # self.width = width
        # self.height = height
        self.colour = colour
        self.game = game 

        self.image = pygame.Surface((40, 70))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.position = vec(x,y)
        #self.rect.midbottom = self.position 
        
        self.velocity = vec(0,0)
        self.acceleration = vec(0,0)
        self.pushdown = 0
        self.jumping = False
    
       
        
        

    def move(self):
        self.acceleration = vec(0,PLAYER_gravity)  # if keys arent being pressed put acceleration to 0 as its not moving, PLAYER_gravity affect the y axis, so it adds gravity constantly to the player
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.acceleration.x = -PLAYER_acceleration
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = PLAYER_acceleration
        
        self.update()

       
    # we seperate the update and moving function apart beacuse, if moving and updating the position of the players are in one function, then one client can control both players movements and be synchrnoized.
    # which is why when we update the client code, we call move for player1, but only update for player2 so that player 2 cant move only when a second client joins    
    def update(self):  

        self.falling = False

        # applying friction in movement
        self.acceleration.x += self.velocity.x * PLAYER_friction
        self.velocity += self.acceleration
        self.position += self.acceleration*0.5 + self.velocity
        
             
       # switching to other side of screen if it hits the edge
        if self.position.x > screen_width:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = screen_width
        if self.velocity.y <0 :
            self.jumping = True
        self.rect.midbottom = self.position # sets the mid bottom of the rect to these coordinate the position of rectangle
        
#self.rect.x += 1 
    #self.rect.x -= 1    

    def jump(self):
        #jump allowed only if standing on a platform
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        
        if hits:
            self.velocity.y =-PLAYER_jump

    
       
    