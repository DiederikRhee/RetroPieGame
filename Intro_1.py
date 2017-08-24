import pygame
import os
import random
import time
from enum import Enum

pygame.init()

display_width = 1366
display_height = 768

black  = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Space Shooter')

gameFileLocation = os.path.dirname(os.path.realpath(__file__))

setFPS = 60
class SpaceShip(object):
    def __init__(self):
        self.PlayerImg = pygame.image.load(gameFileLocation+ '/sprites/Space_Ship.png')
        self.x = (display_width/2) - (self.PlayerImg.get_width()/2)
        self.y = display_height - self.PlayerImg.get_height() - 25
        self.speed = (400/setFPS)
        self.shoot = False
        self.score = 0
        self.bullets = 10
        self.highscore = read_from_file_and_find_highscore(gameFileLocation + "/results.txt")[1]
    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]: # right key
            if ((self.x + self.speed + self.PlayerImg.get_width()) < display_width):
                self.x += self.speed # move right
        elif key[pygame.K_LEFT]: # left key
            if ((self.x - self.speed) > 0):
                self.x -= self.speed # move left
        if key[pygame.K_UP]: # up key
            if ((self.y - self.speed) > (display_height/2)):
                self.y -= self.speed # move right
        elif key[pygame.K_DOWN]: # down key
            if ((self.y + self.speed + self.PlayerImg.get_height()) < (display_height - 10)):
                self.y += self.speed # move down
    def draw(self, surface): 
        myfont = pygame.font.SysFont(None, 50)
        HighScoreLabel = myfont.render("Highscore: " + str(self.highscore), 1, (255,255,255))
        ScoreLabel = myfont.render("Score: " + str(self.score), 1, (255,255,255))
        BulletsLabel = myfont.render("Bullets: " + str(self.bullets), 1, (255,255,255))
        surface.blit(HighScoreLabel, (10, 10))
        surface.blit(ScoreLabel, (310, 10))
        surface.blit(BulletsLabel, (510, 10))
        surface.blit(self.PlayerImg, (self.x, self.y))
    def GetPosition(self):
        return (self.x, self.y)
    def get_Rect(self):
        return pygame.Rect(self.x, self.y, self.PlayerImg.get_width(), self.PlayerImg.get_height())
    def IncreaseScore(self):
        self.score += 1
        if (self.score > self.highscore):
            self.highscore = self.score
            readedHighScore = self.highscore
    def get_Score(self):
        return self.score
    def DecreaseBullets(self):
        if(self.bullets<=0):
            return False
        self.bullets -= 1
        return True
    def AddBullets(self, number):
        self.bullets += number
    
class PlayerBullet(object):
    def __init__(self, x, y):
        self.effect = pygame.mixer.Sound(gameFileLocation + '/sounds/PlayerShoot.wav')
        self.effect.play()
        self.BulletImg = pygame.image.load(gameFileLocation + '/sprites/Player_Bullet.png')
        self.x = x + 37
        self.y = y
        self.speed = (440/setFPS)
    def calculateNewPos(self):
        self.y -= self.speed
        return self.y
    def draw(self, surface):
        surface.blit(self.BulletImg, (self.x, self.y))
    def get_Rect(self):
        return pygame.Rect(self.x, self.y, self.BulletImg.get_width(), self.BulletImg.get_height())
    
class Star(object):
    def __init__(self):
        self.x = random.randint(0, display_width - 10)
        self.y = -20
        self.speed = (100/setFPS)
        self.StarImg = pygame.image.load(gameFileLocation + '/sprites/Star_' + str(random.randint(1,5))+ '.png')
    def calculateNewPos(self):
        self.y += self.speed
        return self.y    
    def draw(self, surface):
        surface.blit(self.StarImg, (self.x, self.y))
        return
class Background(object):
    def __init__(self):
        self.music = pygame.mixer.Sound(gameFileLocation + '/music/Background_Loop.ogg')
        self.music.play(-1)
        self.Stars = []
        self.x = 0
        self.y = 0
        self.counter = 0
        self.newStar = random.randint(15,25)
    def draw(self, surface):
        surface.fill(black)
        self.counter += 1
        if (self.counter == self.newStar):
            self.counter = 0
            self.newStar = random.randint(2,13)
            self.Stars.append(Star())
        for star in self.Stars:
            if (star.calculateNewPos() > display_height):
                self.Stars.remove(star)
            else:
                star.draw(surface)
    def StopMusic(self):
        self.music.stop()
class Ammo(object):
    def __init__(self):
        self.AmmoImg = pygame.image.load(gameFileLocation + '/sprites/Ammo.png')
        self.x = random.randint(0, display_width - self.AmmoImg.get_width())
        self.y = -20
        self.speed = (240/setFPS)
    def draw(self, surface):
        surface.blit(self.AmmoImg, (self.x, self.y))
    def calculateNewPos(self):
        self.y += self.speed
        return self.y
    def get_Rect(self):
        return pygame.Rect(self.x, self.y, self.AmmoImg.get_width(), self.AmmoImg.get_height())

class Enemy(object):
    def __init__(self):
        self.EnemyImg = pygame.image.load(gameFileLocation + '/sprites/Enemy.png')
        self.effect = pygame.mixer.Sound(gameFileLocation + '/sounds/EnemyKilled.wav')
        self.x = random.randint(0, display_width - self.EnemyImg.get_width())
        self.y = -20
        self.speed = (240/setFPS)
    def draw(self, surface):
        surface.blit(self.EnemyImg, (self.x, self.y))
    def calculateNewPos(self):
        self.y += self.speed
        return self.y
    def get_Rect(self):
        return pygame.Rect(self.x, self.y, self.EnemyImg.get_width(), self.EnemyImg.get_height())
    def killed(self):
        self.effect.play()
        
class ARCADE_CONTROL(Enum):
    LEFT = 276
    RIGHT = 275
    UP = 273
    DOWN = 274  
    SHOOT = 306 # LEFTCTRL
    EXIT = 49  # 1

class FPSMeasure:
    def __init__(self):
        self.lastTime = time.time()
        self.counter = 0
        self.currentFPS = setFPS
        self.freqency = 20
    def showFPS(self, surface):
        self.counter +=1
        if (self.counter ==self.freqency):
            self.counter = 0
            newTime = time.time()
            seconds = newTime-self.lastTime
            self.lastTime = newTime
            self.currentFPS = (self.freqency/seconds)
        myfont = pygame.font.SysFont(None, 50)
        FPSLabel = myfont.render("FPS: " + "{0:.2f}".format(self.currentFPS), 1, (255,255,255))
        surface.blit(FPSLabel, (710, 10))    

def message_display(screen, player):
    myfont = pygame.font.SysFont(None, 100)
    write_to_file(gameFileLocation + "/results.txt", "Diederik", player.get_Score())
    # render text
    label = myfont.render("GAME OVER", 1, (255,255,255))
    labelHS = myfont.render("NEW HIGHSCORE!", 1, (255,0,0))
    screen.blit(label, (50, 50))
    if (player.get_Score() >= read_from_file_and_find_highscore(gameFileLocation + "/results.txt")[1]):
        screen.blit(labelHS, (50, 150))
    pygame.display.update()
    time.sleep(3)
    gameloop()
    
def read_from_file_and_find_highscore(file_name):
    file = open(file_name, 'r')
    lines=file.readlines()
    file.close
       
    high_score = 0
    
    for line in lines:
        name, score = line.strip().split(",")
        score = int(score)

        if score > high_score:
            high_score = score
            high_name = name

    return high_name, high_score


def write_to_file(file_name, your_name, points):
    score_file = open(file_name, 'a')
    print (your_name+",", points, file=score_file)
    score_file.close()
    


def gameloop():
    gamelevel = 1
    crashed = False
    bg = Background()      
    player = SpaceShip()
    player_Bullets = []
    enemies = []
    ammos = []
    fpsHandler = FPSMeasure()


    for i in range (0,display_height):
        bg.draw(gameDisplay)
        
    clock = pygame.time.Clock()
    frameNumber = 0  
    while not crashed:
        frameNumber += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                keynumber = event.key
                if(keynumber == ARCADE_CONTROL.EXIT.value):
                    crashed = True
                if(keynumber == ARCADE_CONTROL.SHOOT.value):
                    if(player.DecreaseBullets()):
                        playerPosition = player.GetPosition()
                        newBullet = PlayerBullet(playerPosition[0], playerPosition[1])
                        player_Bullets.append(newBullet)
                        
        if ((frameNumber%(setFPS/4))== 0):
            newEnemy = Enemy()
            enemies.append(newEnemy)
        if ((frameNumber%(setFPS*3))== 0):
            newAmmo = Ammo()
            ammos.append(newAmmo)
            
        player.handle_keys() 
        bg.draw(gameDisplay)
        player.draw(gameDisplay)
        for enemy in enemies:
            if enemy.get_Rect().colliderect(player.get_Rect()):
                crashed = True
                bg.StopMusic()
                message_display(gameDisplay, player);
            if (enemy.calculateNewPos() > display_height):
                enemies.remove(enemy)
            else:
                enemy.draw(gameDisplay)
                
        for playerbullet in player_Bullets:
            removeBullet = False
            for enemy in enemies:
                if enemy.get_Rect().colliderect(playerbullet.get_Rect()):
                   enemies.remove(enemy)
                   enemy.killed()
                   player.IncreaseScore()
                   removeBullet = True
            for ammo in ammos:
                if ammo.get_Rect().colliderect(playerbullet.get_Rect()):
                    ammos.remove(ammo)
                    removeBullet = True   
            if ((playerbullet.calculateNewPos() < 0) or (removeBullet)):
                player_Bullets.remove(playerbullet)
            else:
                playerbullet.draw(gameDisplay)
                
        for ammo in ammos:
            if ammo.get_Rect().colliderect(player.get_Rect()):
                ammos.remove(ammo)
                player.AddBullets(15)
            for enemy in enemies:
                if enemy.get_Rect().colliderect(ammo.get_Rect()):
                   enemies.remove(enemy)
            if (ammo.calculateNewPos() > display_height):
                ammos.remove(ammo)
            else:
                ammo.draw(gameDisplay)
                
        fpsHandler.showFPS(gameDisplay)   
        pygame.display.update()
        clock.tick(setFPS)
    pygame.quit()
    quit()

gameloop()
