import pygame as pg
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def check_collision(circle1, circle2):
    distance_squared = (circle1.centerx - circle2.centerx) ** 2 + (circle1.centery - circle2.centery) ** 2
    radius_sum = circle1.radius + circle2.radius
    return distance_squared <= radius_sum ** 2

def load_texture(filename):
    texture_surface = pg.image.load(filename)
    texture_data = pg.image.tostring(texture_surface, "RGBA", True)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture

def drawStaticImage(texture, x, y, scale):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x - 1 * scale, y - 1 * scale, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x + 1 * scale, y - 1 * scale, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x + 1 * scale, y + 1 * scale, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x - 1 * scale, y + 1 * scale, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def drawSlidingBackGround(texture, x, y, scale, scroll_speed):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    texture_offset = (time.time() * scroll_speed) % 1.0

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glTexCoord2f(0.0, 0.0 + texture_offset)
    glVertex3f(x - 1 * scale, y - 3 * scale, 0)
    glTexCoord2f(1.0, 0.0 + texture_offset)
    glVertex3f(x + 1 * scale, y - 3 * scale, 0)
    glTexCoord2f(1.0, 1.0 + texture_offset)
    glVertex3f(x + 1 * scale, y + 3 * scale, 0)
    glTexCoord2f(0.0, 1.0 + texture_offset)
    glVertex3f(x - 1 * scale, y + 3 * scale, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def drawCharacter(texture, x, y, scale):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(x-1 * scale, y-1 * scale, 0)
    glTexCoord2f(1, 0)
    glVertex3f(x+1 * scale, y-1 * scale, 0)
    glTexCoord2f(1, 1)
    glVertex3f(x+1 * scale, y+1 * scale, 0)
    glTexCoord2f(0, 1)
    glVertex3f(x-1 * scale, y+1 * scale, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def drawPlatform(texture, x, y, scale):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(x - 5 * scale, y-1 * scale, 0)
    glTexCoord2f(1, 0)
    glVertex3f(x + 5 * scale, y-1 * scale, 0)
    glTexCoord2f(1, 1)
    glVertex3f(x + 5 * scale, y+1 * scale, 0)
    glTexCoord2f(0, 1)
    glVertex3f(x - 5 * scale, y+1 * scale, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def drawRotatedText(x, y, angle, text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    gradientSurface = pg.Surface(textSurface.get_size(), pg.SRCALPHA)
    rect = gradientSurface.get_rect()
    start_color = (0, 255, 0, 255)
    end_color = (0, 0, 150, 255)
    for y_pos in range(rect.height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (y_pos / rect.height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (y_pos / rect.height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (y_pos / rect.height))
        a = int(start_color[3] + (end_color[3] - start_color[3]) * (y_pos / rect.height))
        pg.draw.line(gradientSurface, (r, g, b, a), (0, y_pos), (rect.width, y_pos))
    textSurface.blit(gradientSurface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    rotatedSurface = pg.transform.rotate(textSurface, angle)
    textData = pg.image.tostring(rotatedSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(rotatedSurface.get_width(), rotatedSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def drawText(x, y, text, font):                                 
    textSurface = font.render(text, True, WHITE, BLACK)
    textSurface.set_colorkey((0,0,0))
    textData = pg.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

class Rect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, radius,centerx, centery):
        self.radius = radius
        self.centerx = centerx
        self.centery = centery
 
class Player:
    isJumping = False
    jump_velocity = 0
    gravity = -0.01

    def __init__(self, x, y, characterScale, characterTexture):
        self.x = x
        self.y = y
        self.scale = characterScale
        self.characterTexture = characterTexture
        self.updateHitbox()

    def updateHitbox(self):
        self.hitbox = Circle(self.scale, self.x, self.y)

    def draw(self):
        drawCharacter(self.characterTexture, self.x, self.y, self.scale)

    def move(self, speedX):
        if -1.6 < self.x + speedX < 1.6:
            self.x += speedX
            self.updateHitbox()

    def jump(self):
        if not self.isJumping:
            print("in jump function")
            jumpMusic = pg.mixer.Sound("jumpMusic.mp3")
            pg.mixer.Channel(1).play(jumpMusic)
            self.isJumping = True
            self.jump_velocity = 0.2
            self.y += 0.3
            print(self.y)
            self.updateHitbox()

    def apply_gravity(self):
        if self.isJumping:
            new_y = self.y + self.jump_velocity
            if new_y > -1.8:
                self.y = new_y
                self.jump_velocity += self.gravity
                self.updateHitbox()
            else:
                self.isJumping = False
                self.jump_velocity = 0
                self.y = -1.8
                self.updateHitbox()

    def checkCollision(self, platforms):
        for platform in platforms:
            if check_collision(self.hitbox, platform.hitbox):
                self.jump_velocity = 0
                self.y = platform.y + platform.hitbox.radius + self.scale * 0.5
                self.isJumping = False
                self.updateHitbox()
                return True
        return False

    def update(self):
        if round(self.y, 1) == -1.8:
            self.isJumping = False
    
        if self.y > -1.8:
            new_y = self.y + (self.jump_velocity / 2)
            self.y = new_y
            self.jump_velocity += self.gravity
            self.updateHitbox()
 
class Platform:

    def __init__(self, x, y, scale, platformTexture):
        self.x = x
        self.y = y
        self.scale = scale
        self.hitbox = Circle(0.14*scale,x,y+0.04*scale)
        self.platformTexture = platformTexture

    def draw(self):
        drawPlatform(self.platformTexture, self.x, self.y, self.scale)

def main():
    screenWidth = 600
    screenHeight = 700
    pg.init()
    pg.font.init()
    mainMenuScreen = True
    winningScreen = False
    gameOverScreen = False
    gameDisplay = (screenWidth, screenHeight)
    gameScreen = pg.display.set_mode(gameDisplay, DOUBLEBUF | OPENGL)
    gluPerspective(45, (gameDisplay[0] / gameDisplay[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    backgroundTexture = load_texture("background.jpg")
    redBlocksBackgroundTexture = load_texture("red_blocks_background.jpg")

    mainFont = pg.font.Font('Super-Creamy.ttf', 32)
    livesFont = pg.font.Font('Kasper Lullaby.otf', 28)
    titleFont = pg.font.Font('Kasper Lullaby.otf', 72)
    titleFont.set_bold(True)

    mainCharacterTexture = load_texture("mainCharacter.png")
    mainCharater = Player(0, -1.8, 0.3, mainCharacterTexture)
    mainCharacterLives = 3

    icyTowerHeadTexture = load_texture("icyTowerHead.png")
    mainMenuOption = 1

    keyDelay = 0
    keyDelayMax = 20
    keyDelayIncrement = 1

    platformTexture = load_texture("platform.png")
    platform1 = Platform(-1, -1, 0.1, platformTexture)
    platform2 = Platform(0, 0, 0.1, platformTexture)
    platform3 = Platform(1, 1, 0.1, platformTexture)
    platform4 = Platform(1, 2, 0.1, platformTexture)
    platform5 = Platform(0, 3, 0.1, platformTexture)
    platform6 = Platform(0, 4, 0.1, platformTexture)
    platforms = [platform1, platform2, platform3, platform4, platform5, platform6]

    mainMusic = pg.mixer.Sound("mainMusic.mp3")
    pg.mixer.Channel(0).play(mainMusic, loops=-1)
    
    cameraSpeed = 0.005
    cameraY = 0

    glPushMatrix()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        if mainMenuScreen:
            keys = pg.key.get_pressed()

            drawStaticImage(redBlocksBackgroundTexture, 0, 0, 2.1)
            drawRotatedText(400, 515, -30,"Icy", titleFont)
            drawRotatedText(325, 425, -30,"Tower", titleFont)
            drawStaticImage(icyTowerHeadTexture, -0.7, 1.0, 0.8)

            drawText(150, 250, "Start game", mainFont)
            drawText(150, 175, "Options", mainFont)
            drawText(150, 100, "Exit", mainFont)

            if keys[pg.K_DOWN] and mainMenuOption < 3:
                if keyDelay == 0:
                    mainMenuOption += 1
                    keyDelay = keyDelayMax
                else:
                    keyDelay -= keyDelayIncrement

            elif keys[pg.K_UP] and mainMenuOption > 1:
                if keyDelay == 0:
                    mainMenuOption -= 1
                    keyDelay = keyDelayMax
                else:
                    keyDelay -= keyDelayIncrement
            else:
                keyDelay = 0

            if mainMenuOption == 1:
                drawStaticImage(icyTowerHeadTexture, -1.1, -0.45, 0.125)
                if keys[pg.K_RETURN]:
                    mainMenuScreen = False
            elif mainMenuOption == 2:
                drawStaticImage(icyTowerHeadTexture, -1.1, -0.9, 0.125)
            elif mainMenuOption == 3:
                drawStaticImage(icyTowerHeadTexture, -1.1, -1.35, 0.125)
                if keys[pg.K_RETURN]:
                    pg.quit()
        
        elif winningScreen:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            keys = pg.key.get_pressed()
            pg.mixer.Channel(0).stop()

            drawText(240, 450, "You Win !", mainFont)
            drawText(240, 400, "With " + str(mainCharacterLives) + " lives", livesFont)
            drawText(200, 350, "To Restart press R", mainFont)

            if keys[pg.K_r]:
                winningScreen = False
                gameOverScreen = False
                mainCharater.x = 0
                mainCharater.y = -1.8
                glTranslatef(0.0, cameraY, 0.0)
                cameraY = 0
                pg.mixer.Channel(0).play(mainMusic, loops=-1)
                mainMenuScreen = True

        elif gameOverScreen:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            keys = pg.key.get_pressed()
            pg.mixer.Channel(0).stop()

            drawText(240, 400, "You Lost !", mainFont)
            drawText(200, 350, "To Restart press R", mainFont)

            if keys[pg.K_r] and mainCharacterLives > 0:
                winningScreen = False
                gameOverScreen = False
                mainCharater.x = 0
                mainCharater.y = -1.8
                glTranslatef(0.0, cameraY, 0.0)
                cameraY = 0
                pg.mixer.Channel(0).play(mainMusic, loops=-1)
                mainMenuScreen = True

        else:
            glTranslatef(0.0, -cameraSpeed, 0.0)
            cameraY += cameraSpeed
            if mainCharater.y + 2.1 < cameraY:
                mainCharacterLives -= 1
                gameOverScreen = True

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            keys = pg.key.get_pressed()

            drawSlidingBackGround(backgroundTexture, 0, 0, 2.2, 0.05)
            
            if keys[pg.K_RIGHT]:
                mainCharater.move(0.04)
            elif keys[pg.K_LEFT]:
                mainCharater.move(-0.04)

            if keys[pg.K_SPACE]:
                mainCharater.jump()
                
            mainCharater.draw()
            mainCharater.checkCollision(platforms)
            mainCharater.apply_gravity()
            mainCharater.update()

            if mainCharater.y > 5:
                winningScreen = True
            
            drawText(30, 660, "Lives: " + str(mainCharacterLives), livesFont)

            for platform in platforms:
                platform.draw()


        pg.display.flip()
        pg.time.Clock().tick(60)

main()
