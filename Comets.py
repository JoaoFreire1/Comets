
import pygame
import math
import random

pygame.init()

sw = 800
sh = 600
#Tamanho do ecrã em pixeis

Background = pygame.image.load('Projetc02_Images/Galaxy_Background.jpg')
Player_Spaceship = pygame.image.load('Projetc02_Images/Player_Spaceship.png')
PowerUp = pygame.image.load('Projetc02_Images/PowerUp.png')
AsteroidL = pygame.image.load('Projetc02_Images/AsteroidL.png')
AsteroidM = pygame.image.load('Projetc02_Images/AsteroidM.png')
AsteroidS = pygame.image.load('Projetc02_Images/AsteroidS.png')

pygame.display.set_caption('Comets')
Win = pygame.display.set_mode((sw, sh))

Timer = pygame.time.Clock()
#Temporizador do jogo

GameOver = False
#GameOver começa por estar falso

Life = 1
#Vida do Jogador que começa como Positiva

Score = 0
#Contador de Pontos que começa a 0's

class Player(object):
    def __init__(self):
        self.img = Player_Spaceship
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2
        self.y = sh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine *self.h//2)
        self.vx = 0
        self.vy = 0

    def draw(self):
        #Win.blit(self.img, [self.x, self.y, self.w, self.h])
        Win.blit(self.rotatedSurf, self.rotatedRect)

    def TurnLeft(self):
        self.angle += 3
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def TurnRight(self):
        self.angle -= 3
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def MoveForward(self):
        self.x += self.vx
        self.y += self.vy
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def CheckLocation(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x <0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0
    
    def Accelerate(self):
        self.vx += self.cosine * 0.1
        self.vy += self.sine * -0.1

#Classe Player com movimento e deteção de localização
             
class Bullets(object):
    def __init__(self):
        self.point = Player.head
        self.x, self.y = self.point
        self.w = 3
        self.h = 7
        self.c = Player.cosine
        self.s = Player.sine 
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self):
        pygame.draw.rect(Win, (255,255,255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True

#Classe Balas com Movimento implementado, duração e limites de ecrã

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = AsteroidS
        elif self.rank == 2:
            self.image = AsteroidM
        else:
            self.image = AsteroidL
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self):
        Win.blit(self.image, (self.x, self.y))

def redrawGameWindow():
    Win.blit(Background, (0,0))
    font = pygame.font.SysFont('arial', 60)
    GameOverText = font.render('GameOver', 1, (255, 10, 10)) 
    ScoreText = font.render('Score ' + str(Score), 1, (255, 255, 255))


    Player.draw()
    for b in PlayerBullets:
        b.draw()
    for a in Asteroids:
        a.draw()

    if GameOver:
        Win.blit(GameOverText, (sw//2- GameOverText.get_width()//2, sh//2 - GameOverText.get_height()//2))

    Win.blit(ScoreText, (sw- ScoreText.get_width() - 25, 25))
    pygame.display.update()

Player = Player()
PlayerBullets = []
Asteroids = []
Count = 0
Buttons = ["Play", "Quit"]
SelectedButton = 0
InMenu = True
#Listas de Objetos


run = True
while run :
    
    Timer.tick(60)
    keys = pygame.key.get_pressed()

    if (InMenu):
        Win.blit(Background, (0,0))
        font = pygame.font.SysFont('arial', 60)
        titlefont = pygame.font.SysFont('arial', 120)
        TitleText = titlefont.render('Comets', 1, (255, 10, 10))
        Win.blit(TitleText, (sw//2 - TitleText.get_width()//2, 60 - TitleText.get_height()//2))

        if SelectedButton == 0:
            PlayText = font.render('Play', 1, (255, 10, 10))
            Win.blit(PlayText, (sw//2 - PlayText.get_width()//2, sh//2 - (PlayText.get_height()//2) - 60))

            QuitText = font.render('Quit', 1, (10, 10, 255))
            Win.blit(QuitText, (sw//2- QuitText.get_width()//2, sh//2 - (QuitText.get_height()//2) + 60))
        else:
            PlayText = font.render('Play', 1, (10, 10, 255))
            Win.blit(PlayText, (sw//2 - PlayText.get_width()//2, sh//2 - (PlayText.get_height()//2) - 60))

            QuitText = font.render('Quit', 1, (255, 10, 10))
            Win.blit(QuitText, (sw//2- QuitText.get_width()//2, sh//2 - (QuitText.get_height()//2) + 60))

        if keys[pygame. K_UP]:
            SelectedButton += 1
        if SelectedButton > 1:
            SelectedButton = 0

        if keys[pygame. K_SPACE]:
            if SelectedButton == 0:
                InMenu = False
            else:
                run = False
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    else:
        Count += 1
        if not GameOver:
            if Count % 50 == 0:
                ran = random.choice([1,1,1,2,2,3])
                Asteroids.append(Asteroid(ran))

            Player.CheckLocation()

            for b in PlayerBullets:
                b.move()
                if b.checkOffScreen():
                    PlayerBullets.pop(PlayerBullets.index(b))
                
            for a in Asteroids:
                a.x += a.xv
                a.y += a.yv

                if (Player.x - (Player.w)/2 >= a.x and Player.x - (Player.w)/2 <= a.x + a.w) or (Player.x + (Player.w)/2 >= a.x and Player.x + (Player.w)/2 <= a.x + a.w):
                    if (Player.y - (Player.h)/2 >= a.y and Player.y - (Player.h)/2 <= a.y + a.h) or (Player.y + (Player.h)/2 >= a.y and Player.y + (Player.h)/2 <= a.y + a.h):
                        Life -= 1
                        Asteroids.pop(Asteroids.index(a))
                        break
                    #Verificação se o Asteroide acerta no jogador

                for b in PlayerBullets:
                    if (b.x >= a.x and b.x <= a.x + a.w) or (b.x  + b.w >= a.x and b.x + b.w <= a.x + a.w):
                        if (b.y >= a.y and b.y <= a.y + a.h) or (b.y + b.h >= a.y and b.y * b.h <= a.y + a.h):
                            Asteroids.pop(Asteroids.index(a))
                            PlayerBullets.pop(PlayerBullets.index(b))
                #Colisão de Balas definida através da deteção de x e y das balas assim como dos asteroides
                            if a.rank == 3:
                                Score += 10
                                na1 = Asteroid(2)
                                na2 = Asteroid(2)
                                na3 = Asteroid(2)
                                na1.x = a.x  
                                na2.x = a.x 
                                na3.x = a.x
                                na1.y = a.y 
                                na2.y = a.y
                                na3.y = a.y
                                Asteroids.append(na1)
                                Asteroids.append(na2)
                                Asteroids.append(na3)
                            elif a.rank == 2:
                                Score += 20
                                na1 = Asteroid(1)
                                na2 = Asteroid(1)
                                na3 = Asteroid(1)
                                na4 = Asteroid(1)
                                na5 = Asteroid(1)
                                na1.x = a.x  
                                na2.x = a.x 
                                na3.x = a.x
                                na4.x = a.x 
                                na5.x = a.x
                                na1.y = a.y 
                                na2.y = a.y
                                na3.y = a.y
                                na4.y = a.y
                                na5.y = a.y
                                Asteroids.append(na1)
                                Asteroids.append(na2)
                                Asteroids.append(na3)
                                Asteroids.append(na4)
                                Asteroids.append(na5)
                            else:
                                Score += 30
                            #Quando o jogador destroi um cometa tres ou cinco de tamanhos inferiores aparecem, "append"


            if Life <= 0:
                GameOver = True

            if keys[pygame. K_LEFT]:
                Player.TurnLeft()
            if keys[pygame. K_RIGHT]:
                Player.TurnRight()
            if keys[pygame.K_UP]:
                Player.Accelerate()

            Player.MoveForward()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not GameOver:
                        PlayerBullets.append(Bullets())
                    else:
                        GameOver = False
                        Life = 1
                        Score = 0
                        Asteroids.clear()
                        Player.x = sw//2
                        Player.y = sh//2
                        Player.angle = 0
                        Player.vx = 0
                        Player.vy = 0

        #Loops de Jogo principal    
        redrawGameWindow()

pygame.quit()
#Sair do Jogo
