import pygame
import os
import math
import time

WIDTH = 2000
HEIGHT = 1200
cwd = os.getcwd()
assets = os.path.join(cwd, "..", "assets")
image_sheet = os.path.join(assets, "hidef_dino.png")

HDPI = { "CACTUS_LARGE" : { "x": 652, "y": 2 },
         "CACTUS_SMALL": { "x": 446, "y": 2 },
         "CLOUD": { "x": 166, "y": 2 },
         "HORIZON": { "x": 2, "y": 104 },
         "MOON" : { "x": 954, "y": 2 },
         "PTERODACTYL" : { "x": 260, "y": 2 },
         "RESTART" : { "x": 2, "y": 2 },
         "TEXT_SPRITE" : { "x": 1294, "y": 2 },
         "TREX" : { "x": 1678, "y": 2 },
         "STAR" : { "x": 1276, "y": 2 }}

x = HDPI["HORIZON"]["x"]
y = HDPI["HORIZON"]["y"]
SPEED = 6
background_width = 2400
background_height = 24
BLACK = (0,0,0)

class SpriteSheet():
    sprite_sheet = None
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename).convert()
    def getImage(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height) )
        image.set_colorkey(BLACK)
        return image

class Dino():
    trex = {}
    jumping = False
    ducking = False
    groundYPos = 0
    yPos = 0
    jumpVelocity = 0.0
    reachedMinHeight = False
    speedDrop = False
    jumpCount = 0
    jumpspotX = 0
    runningFrameIndex = 0
    currentFrameCount = 0
    jumpVelocity = 0.0
    config = {"WIDTH"  : 88,
              "WIDTH_DUCK" : 118,
              "HEIGHT" : 94,
              "HEIGHT_DUCK" : 60,
              "START_X_POS" : 50,
              "MAX_JUMP_HEIGHT" : 300,
              "MIN_JUMP_HEIGHT" : 300,
              "SPRITE_WIDTH" : 262,
              "DROP_VELOCITY" : 6.0,
              "GRAVITY" : 0.6,
              "INITIAL_JUMP_VELOCITY" : -15.0,
              "STATE": "RUNNING"
    }
    animationFrames = {"WAITING" : {"FRAMES" : [44, 0], "MS_PER_FRAME": 1000/3},
                       "RUNNING" : {"FRAMES" : [88, 132], "MS_PER_FRAME": 1000/12},
                       "CRASHED" : {"FRAMES" : [220], "MS_PER_FRAME": 1000/60},
                       "JUMPING" : {"FRAMES" : [0], "MS_PER_FRAME": 1000/60},
                       "DUCKING" : {"FRAMES" : [264,323], "MS_PER_FRAME": 1000/8}}

    def __init__(self, sprite_sheet, sprite_info):
        self.sprite_sheet = sprite_sheet
        self.collided = False
        self.frameState = "RUNNING"
        self.startingX = 0
        #Creating Idle entry
        self.trex["IDLE"] = {"x" : sprite_info["TREX"]["x"]}
        self.trex["IDLE"]["y"] = sprite_info["TREX"]["y"]
        #Creating Ducking entry
        self.trex["DUCKING"] = {0 : {"x" : self.trex["IDLE"]["x"] + self.config["WIDTH"] * 6}}
        self.trex["DUCKING"][0]["y"] = sprite_info["TREX"]["y"] + (self.config["HEIGHT"] - self.config["HEIGHT_DUCK"])
        self.trex["DUCKING"][1] = {"x" : self.trex["DUCKING"][0]["x"] + self.config["WIDTH_DUCK"]}
        self.trex["DUCKING"][1]["y"] = sprite_info["TREX"]["y"] + (self.config["HEIGHT"] - self.config["HEIGHT_DUCK"])
        #Creating running entry
        self.trex["RUNNING"] = {0 : {"x" : self.trex["IDLE"]["x"] + self.config["WIDTH"] * 2}}
        self.trex["RUNNING"][0]["y"] = sprite_info["TREX"]["y"]
        self.trex["RUNNING"][1] = {"x" :  self.trex["IDLE"]["x"] + self.config["WIDTH"] * 3}
        self.trex["RUNNING"][1]["y"] = sprite_info["TREX"]["y"]
        #Creating Collide entry
        self.trex["COLLIDE"] = {"x" : self.trex["IDLE"]["x"] + self.config["WIDTH"] * 5}
        self.trex["COLLIDE"]["y"] = sprite_info["TREX"]["y"]
        #Getting the Image
        self.trex["IDLE"]["IMAGE"] = sprite_sheet.getImage(self.trex["IDLE"]["x"], self.trex["IDLE"]["y"],
                                                           self.config["WIDTH"], self.config["HEIGHT"])
        self.trex["RUNNING"][0]["IMAGE"] = sprite_sheet.getImage(self.trex["RUNNING"][0]["x"],
                                                                 self.trex["RUNNING"][0]["y"],
                                                                 self.config["WIDTH"], self.config["HEIGHT"])
        self.trex["RUNNING"][1]["IMAGE"] = sprite_sheet.getImage(self.trex["RUNNING"][1]["x"],
                                                                 self.trex["RUNNING"][1]["y"],
                                                                 self.config["WIDTH"], self.config["HEIGHT"])
        self.trex["COLLIDE"]["IMAGE"] = sprite_sheet.getImage(self.trex["COLLIDE"]["x"],
                                                              self.trex["COLLIDE"]["y"],
                                                              self.config["WIDTH"], self.config["HEIGHT"])
        self.trex["DUCKING"][0]["IMAGE"] =sprite_sheet.getImage(self.trex["DUCKING"][0]["x"],
                                                                self.trex["DUCKING"][0]["y"],
                                                                self.config["WIDTH_DUCK"], self.config["HEIGHT_DUCK"])
        self.trex["DUCKING"][1]["IMAGE"] =sprite_sheet.getImage(self.trex["DUCKING"][1]["x"],
                                                                self.trex["DUCKING"][1]["y"],
                                                                self.config["WIDTH_DUCK"], self.config["HEIGHT_DUCK"])
    def collide(self, xObj, yObj):
        xCollide = False
        yCollide = False
        dinoMaxX = self.startingX + self.config["WIDTH"]
        dinoMinX = self.startingX
        dinoMaxY = self.getYPos()
        dinoMinY = dinoMaxY - self.config["HEIGHT"]
        objMinX = xObj[0]
        objMaxX = xObj[1]
        objMinY = yObj[0]
        objMaxY = yObj[1]

        if dinoMaxX >= objMinX and dinoMaxX < objMaxX:
            xCollide = True
        elif dinoMinX >= objMinX and dinoMinX < objMinX:
            xCollide = True
        if dinoMaxY >= objMaxY:
            yCollide = True
        if xCollide and yCollide:
            self.collided = True
        return self.collided
    def setFPS(self, FPS):
        self.msPerFrame = int(1000 / FPS)
    def setXPos(self, x):
        self.startingX = x
    def setJumping(self, jumping):
        self.jumping = jumping
    def setCollide(self, collide):
        self.collide = collide
    def isJumping(self):
        return self.jumping
    def getFrame(self):
        if self.collided:
            return self.trex["COLLIDE"]["IMAGE"]
        elif self.jumping:
            return self.trex["IDLE"]["IMAGE"]
        else:
            self.currentFrameCount += 1
            self.currentFrameCount %= self.msPerFrame
            if self.currentFrameCount == 0:
                self.runningFrameIndex += 1
                self.runningFrameIndex %= 2
            return self.trex["RUNNING"][self.runningFrameIndex]["IMAGE"]
    def setGroundYPos(self, yPos):
        self.groundYPos = yPos
    def getYPos(self):
        if self.yPos <= self.groundYPos - self.config["MAX_JUMP_HEIGHT"] and self.config["STATE"] == "JUMPING":
            self.jumpVelocity = self.config["DROP_VELOCITY"]
            self.config["STATE"] = "FALLING"
        elif self.yPos >= self.groundYPos and self.config["STATE"] == "FALLING":
            self.jumping = False
            self.config["STATE"] = "RUNNING"
            self.jumpVelocity = 0
            self.yPos = self.groundYPos
        elif self.config["STATE"] == "RUNNING" and self.jumping:
            self.config["STATE"] = "JUMPING"
            self.yPos = self.groundYPos
            self.jumpVelocity = self.config["INITIAL_JUMP_VELOCITY"]

        if self.config["STATE"] == "JUMPING" and self.jumpVelocity >= 0:
            self.jumpVelocity = self.config["DROP_VELOCITY"]
            self.config["STATE"] = "FALLING"
        elif self.config["STATE"] != "RUNNING":
            self.yPos += self.jumpVelocity
            self.jumpVelocity += self.config["GRAVITY"]
        else:
            self.yPos = self.groundYPos
            self.jumpVelocity = 0

        return self.yPos

class Cloud():
    cloud = {"WIDTH": 84, "HEIGHT": 27}
    def __init__(self, sprite_sheet, sprite_info):
        self.cloud["x"] = sprite_info["CLOUD"]["x"]
        self.cloud["y"] = sprite_info["CLOUD"]["y"]
        self.sprite_sheet = sprite_sheet
    def getCloud(self):
        return self.sprite_sheet.getImage(self.cloud["x"], self.cloud["y"],
                                          self.cloud["WIDTH"], self.cloud["HEIGHT"])
#    def randomCloud(self):
#        random.randrang

class Cactus():
    cactus = {}
    def __init__(self, sprite_sheet, sprite_info):
        self.sprite_sheet = sprite_sheet
        self.cactus["LARGE"] = {"x" : sprite_info["CACTUS_LARGE"]["x"]}
        self.cactus["LARGE"]["y"] = sprite_info["CACTUS_LARGE"]["y"]
        self.cactus["SMALL"] = {"x" : sprite_info["CACTUS_SMALL"]["x"]}
        self.cactus["SMALL"]["y"] = sprite_info["CACTUS_SMALL"]["y"]
        self.cactus["LARGE"]["HEIGHT"] = 100
        self.cactus["LARGE"]["WIDTH"] = 49
        self.cactus["LARGE"]["IMAGE"] = self.sprite_sheet.getImage(self.cactus["LARGE"]["x"],
                                                                   self.cactus["LARGE"]["y"],
                                                                   self.cactus["LARGE"]["WIDTH"],
                                                                   self.cactus["LARGE"]["HEIGHT"])
        self.cactus["SMALL"]["HEIGHT"] = 70
        self.cactus["SMALL"]["WIDTH"] = 34
        self.cactus["SMALL"]["IMAGE"] = self.sprite_sheet.getImage(self.cactus["SMALL"]["x"],
                                                                   self.cactus["SMALL"]["y"],
                                                                   self.cactus["SMALL"]["WIDTH"],
                                                                   self.cactus["SMALL"]["HEIGHT"])
    def setGroundPosition(self, groundYPos):
        self.cactus["GROUND"] = {"y" : groundYPos}
    def updateCactus(self, window, x):
        window.blit(self.getCactus("LARGE"), (x, self.cactus["GROUND"]["y"]))
    def getCactus(self, size):
        return self.cactus[size]["IMAGE"]
    def getHeight(self):
        return self.cactus["LARGE"]["HEIGHT"]
    def getWidth(self):
        return self.cactus["LARGE"]["WIDTH"]
class Horizon():
    config = {}
    offset = 100
    speed = 1
    def __init__(self, sprite_sheet, sprite_info, width, height):
        self.sprite_sheet = sprite_sheet
        self.config["WINDOW"] = {"HEIGHT" : height}
        self.config["WINDOW"]["WIDTH"] = width
        self.config["HORIZON"] = {"x" : sprite_info["HORIZON"]["x"]}
        self.config["HORIZON"]["y"] = sprite_info["HORIZON"]["y"]
        self.config["HORIZON"]["WIDTH"] = 2400
        self.config["HORIZON"]["HEIGHT"] = 24
        self.rel_x = self.config["HORIZON"]["WIDTH"]
        self.config["HORIZON"]["IMAGE"] = self.sprite_sheet.getImage(self.config["HORIZON"]["x"],
                                                                     self.config["HORIZON"]["y"],
                                                                     self.config["HORIZON"]["WIDTH"],
                                                                     self.config["HORIZON"]["HEIGHT"])
    def setSpeed(self, speed):
        self.speed = speed
    def getHorizon(self, window):
        delta = self.rel_x - self.config["HORIZON"]["WIDTH"]
        window.blit(self.config["HORIZON"]["IMAGE"],
                    (delta, self.config["WINDOW"]["HEIGHT"] - self.config["HORIZON"]["HEIGHT"] - self.offset))
        if delta < self.config["HORIZON"]["WIDTH"]:
            window.blit(self.config["HORIZON"]["IMAGE"],
                        (self.rel_x, self.config["WINDOW"]["HEIGHT"] - self.config["HORIZON"]["HEIGHT"] -
                         self.offset))
        return self.rel_x
    def updateHorizon(self, window):
        delta = self.rel_x - self.config["HORIZON"]["WIDTH"]
        window.blit(self.config["HORIZON"]["IMAGE"],
                    (delta, self.config["WINDOW"]["HEIGHT"] - self.config["HORIZON"]["HEIGHT"] - self.offset))
        if delta < self.config["HORIZON"]["WIDTH"]:
            window.blit(self.config["HORIZON"]["IMAGE"],
                        (self.rel_x, self.config["WINDOW"]["HEIGHT"] - self.config["HORIZON"]["HEIGHT"] -
                         self.offset))
        self.rel_x -= self.speed
        self.rel_x %= self.config["HORIZON"]["WIDTH"]
        return self.rel_x

def game_window(width, height):
    pygame.init()
    if width <= 0 or height <= 0:
        raise Exception("Invalid width and height")
    win = pygame.display.set_mode((width,height))
    win.fill( (247,247,247))
    return win



##########################################################
FPS = 60
groundYPos = HEIGHT - background_height - 160
msPerFrame = math.ceil(1000 / FPS)
window = game_window(WIDTH, HEIGHT)
sprite_sheet = SpriteSheet(image_sheet)
initial_x = HDPI["HORIZON"]["x"]
initial_y = HDPI["HORIZON"]["y"]
dinoXPos = 10
initial_horizon_image = sprite_sheet.getImage(initial_x, initial_y, background_width, background_height)
window.blit(initial_horizon_image, (0, HEIGHT - background_height - 100))
cloud = Cloud(sprite_sheet, HDPI)
yPos = 0
cactus = Cactus(sprite_sheet, HDPI)
cactus.setGroundPosition(groundYPos)
dino = Dino(sprite_sheet, HDPI)
dino.setFPS(FPS)
dino.setXPos(dinoXPos)
dino.setGroundYPos(groundYPos)
horizon = Horizon(sprite_sheet, HDPI, WIDTH, HEIGHT)
horizon.setSpeed(6)
run = True
new_x = initial_x
new_background_width = 0
clock = pygame.time.Clock()
old_time = pygame.time.get_ticks()
duck = False
collided = False

while run:
    new_time = pygame.time.get_ticks()
    waited = new_time - old_time
    old_time = new_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_UP] or  keys[pygame.K_SPACE]:
        if not dino.isJumping():
            dino.setJumping(True)
    if keys[pygame.K_DOWN]:
        duck = True
        print("Duck")
    if keys[pygame.K_F5]:
        showMenu = True

    window.fill( (247,247,247))
    if collided:
        currentX = horizon.getHorizon(window)
        yPos = groundYPos
        window.blit(dino.getFrame(), (dinoXPos, yPos))
    else:
        currentX = horizon.updateHorizon(window)
        if dino.isJumping():
            yPos = dino.getYPos()
        else:
            yPos = groundYPos
        collided = dino.collide((currentX, currentX + cactus.getWidth()),
                                (groundYPos - cactus.getHeight(), groundYPos))
        window.blit(dino.getFrame(), (10, yPos))
    cactus.updateCactus(window, currentX)
    window.blit(cloud.getCloud(), (300, 200))
    pygame.display.update()
#    pygame.time.delay(msPerFrame)
    if waited < 60:
        time.sleep(1.0/(120 - waited))

pygame.quit()
