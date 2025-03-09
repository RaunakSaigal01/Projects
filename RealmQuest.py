import pygame
import random
import sys

pygame.init() #initialisation of pygame

screen_width=1000 #Pixels
screen_height=500

enemies=[]
player_bullets=[]

score=0
player_lives=3
font=pygame.font.Font(None,36)
game_over_font=pygame.font.Font(None,100)

speed_increase_rate=0

background_image=pygame.image.load(r"C:\Users\Hp\OneDrive\Desktop\python-game\background.png") #loading an image from the current directory in a variable
background_image=pygame.transform.scale(background_image,(screen_width,screen_height)) #setting the scale of the image to be as big as the screen

bg_x=0

class Character:
    def __init__(self,x,y): #constructor function
        self.x=x
        self.y=y
        self.image=pygame.image.load(r"C:\Users\Hp\OneDrive\Desktop\python-game\player1.png")
        self.image=pygame.transform.scale(self.image,(100,100))
        self.rect=self.image.get_rect() #creating a rectangle outside the image same dimensions as the image(hitbox)
        self.rect.center=(x,y)
        self.run_animation_count=0
        self.image_list=[r"C:\Users\Hp\OneDrive\Desktop\python-game\player1.png",r"C:\Users\Hp\OneDrive\Desktop\python-game\player2.png",r"C:\Users\Hp\OneDrive\Desktop\python-game\player3.png",r"C:\Users\Hp\OneDrive\Desktop\python-game\player4.png"] #loading addresses of all the images to be used
        self.is_jump=False #tellin whether the player is jumping or not
        self.jump_count=15
        self.bullet_image=r"C:\Users\Hp\OneDrive\Desktop\python-game\bullet.png"

    def draw(self):
        self.rect.center=(self.x,self.y)
        screen.blit(self.image,self.rect)
    def run_animation_player(self):
        if not self.is_jump: #creating a function to animate the movement of the player by using multiple images
            self.image=pygame.image.load(self.image_list[int(self.run_animation_count)]) #list indexing should be an integer
            self.image=pygame.transform.scale(self.image,(100,100))
            self.run_animation_count+=0.5 #controlling the speed of animation 
            self.run_animation_count=self.run_animation_count%4 #list index cannot be greater than 3 as there are only 4 elements in it
    def jump(self):
        if(self.jump_count>-15):
            n=1
            if(self.jump_count<0):
                n=-1
            self.y-=((self.jump_count**2)/10)*n
            self.jump_count-=1
        else:
            self.is_jump=False
            self.jump_count=15
            self.y=386
    def shoot(self):
        bullet=Bullet(self.x+5,self.y-18,self.bullet_image)
        player_bullets.append(bullet)


class Enemy:
    def __init__(self,x,y): #constructor function
        self.x=x
        self.y=y
        self.image=pygame.image.load(r"C:\Users\Hp\OneDrive\Desktop\python-game\enemy1.png")
        self.image=pygame.transform.scale(self.image,(75,75))
        self.rect=self.image.get_rect() #creating a rectangle outside the image same dimensions as the image(hitbox)
        self.rect.center=(x,y)
        self.run_animation_count=0
        self.image_list=[r"C:\Users\Hp\OneDrive\Desktop\python-game\enemy1.png",r"C:\Users\Hp\OneDrive\Desktop\python-game\enemy2.png",r"C:\Users\Hp\OneDrive\Desktop\python-game\enemy3.png"] #loading addresses of all the images to be used
        self.is_jump=False #tellin whether the player is jumping or not
        self.jump_count=15

    def draw(self):
        self.rect.center=(self.x,self.y)
        screen.blit(self.image,self.rect)
    def run_animation_enemy(self): #creating a function to animate the movement of the player by using multiple images
        self.image=pygame.image.load(self.image_list[int(self.run_animation_count)]) #list indexing should be an integer
        self.image=pygame.transform.scale(self.image,(75,75))
        self.run_animation_count+=0.5 #controlling the speed of animation 
        self.run_animation_count=self.run_animation_count%3 


class Bullet:
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.image=pygame.image.load(image)
        self.image=pygame.transform.scale(self.image,(15,15))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
    def draw(self):
        self.rect.center=(self.x,self.y)
        screen.blit(self.image,self.rect)
    def move(self,vel):
        self.x+=vel #postion of bullet increases with velocity

    def off_screen(self):
        return(self.x<=0 or self.x>screen_width)


screen=pygame.display.set_mode((screen_width,screen_height)) #make the variable 'screen' where we can enter our dimensions of the display
pygame.display.set_caption("Realm Quest") #Setting the Title 

player=Character(100,386)
enemy=Enemy
bullet=Bullet
running = True
clock=pygame.time.Clock() #Making clock object to perform any time related functions in game
last_enemy_spawn_time=pygame.time.get_ticks()

while running:
    score+=1
    for event in pygame.event.get(): #returns all the events that are going on in the game (returns list)
        if event.type==pygame.QUIT: #Quit is true when we click on the cross button
            running=False
        if event.type==pygame.KEYDOWN:
            if (event.key==pygame.K_SPACE) or (event.key==pygame.K_UP):
                player.is_jump=True
            if event.key==pygame.K_0:
                player.shoot()
    speed_increase_rate=speed_increase_rate+0.01 #increasing the speed of the image everytime the loop is completed
    bg_x=bg_x-(10+speed_increase_rate) #decreasing the x coordinate to show that image is moving towards the left
    if bg_x < -screen_width: #making an infinite loop 
        bg_x=0 
    screen.blit(background_image,(bg_x,0)) #used for printing anything on the screen
    screen.blit(background_image,(screen_width+bg_x,0)) #using second image to create a loop like motion 
    current_time=pygame.time.get_ticks()
    if current_time-last_enemy_spawn_time>=1500: #milliseconds
        if random.randint(0,100)<3:
            enemy_x=screen_width+900
            enemy_y=396
            enemy=Enemy(enemy_x,enemy_y)
            enemies.append(enemy)
            last_enemy_spawn_time=current_time
    for enemy in enemies:
        enemy.x-=(15+speed_increase_rate)
        enemy.draw()
        enemy.run_animation_enemy()
        #collision 1
        if enemy.rect.colliderect(player.rect):
            speed_increase_rate=0
            score-=150
            player_lives-=1
            enemies.remove(enemy)
        #collision 2
        for bullet in player_bullets:
            if pygame.Rect.colliderect(enemy.rect,bullet.rect):
                player_bullets.remove(bullet)
                enemies.remove(enemy)

    for bullet in player_bullets:
        if(bullet.off_screen()):
            player_bullets.remove(bullet)
        else:
            bullet.draw()
            bullet.move(10)

    if player_lives<=0:
        game_over_text=game_over_font.render("GAME OVER",True,(200,0,200))
        screen.blit(game_over_text,(screen_width//2-150,screen_height//2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit
        sys.exit()
    live_text=font.render(f'Lives:{player_lives}',True,(250,0,0)) #printing the player lives (0,0,0) is black R,G,B
    screen.blit(live_text,(screen_width-120,10))
    score_text=font.render(f'Score:{score}',True,(0,250,0)) #printing the player lives (0,0,0) is black R,G,B
    screen.blit(score_text,(20,10))
    if (player.is_jump):
        player.jump()
    player.draw() #printing player on the screen with given characteristics
    player.run_animation_player()
    pygame.display.update() #for updating the changes in the game we call this
    clock.tick(30) #setting the upper limit of fps (loop will run 30 times in a second max)
pygame.quit()