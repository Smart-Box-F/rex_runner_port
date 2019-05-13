


import pygame

WIDTH = 2400
HEIGHT = 1200
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
image_sheet = "hidef_dino.png"







x = HDPI["HORIZON"]["x"]
y = HDPI["HORIZON"]["y"]
background_width = 2400
background_height = 24
#dino_height =
#dino_width = 
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
#    msPerFrame = 1000 / FPS
    trex = {}
    jumping = False
    ducking = False
    jumpVelocity = 0
    reachedMinHeight = False
    speedDrop = False
    jumpCount = 0
    jumpspotX = 0
    config = {"WIDTH"  : 88,
              "WIDTH_DUCK" : 118,
              "HEIGHT" : 94,
              "HEIGHT_DUCK" : 60,
              "START_X_POS" : 50,
              "MAX_JUMP_HEIGHT" : 30,
              "MIN_JUMP_HEIGHT" : 30,
              "SPRITE_WIDTH" : 262,
              "DROP_VELOCITY" : -5,
    }
    animationFrames = {"WAITING" : {"FRAMES" : [44, 0], "MS_PER_FRAME": 1000/3},
                       "RUNNING" : {"FRAMES" : [88, 132], "MS_PER_FRAME": 1000/12},
                       "CRASHED" : {"FRAMES" : [220], "MS_PER_FRAME": 1000/60},
                       "JUMPING" : {"FRAMES" : [0], "MS_PER_FRAME": 1000/60},
                       "DUCKING" : {"FRAMES" : [264,323], "MS_PER_FRAME": 1000/8}}

    def __init__(self, sprite_sheet, sprite_info):
        self.sprite_sheet = sprite_sheet
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
    def getIdleImage(self):
        return self.trex["IDLE"]["IMAGE"]

class Cloud():
    cloud = {"WIDTH": 84,
             "HEIGHT": 27}
    def __init__(self, sprite_sheet, sprite_info):
        self.cloud["x"] = sprite_info["CLOUD"]["x"]
        self.cloud["y"] = sprite_info["CLOUD"]["y"]
        self.sprite_sheet = sprite_sheet
    def getCloud(self):
        return self.sprite_sheet.getImage(self.cloud["x"], self.cloud["y"],
                                          self.cloud["WIDTH"], self.cloud["HEIGHT"])
#    def randomCloud(self):
#        random.randrang


def game_window(width, height):
    if width <= 0 or height <= 0:
        raise Exception("Invalid width and height")
    win = pygame.display.set_mode((width,height))
    win.fill( (247,247,247))
    return win
##########################################################
FPS = 60
msPerFrame = int(1000 / FPS)
window = game_window(WIDTH, HEIGHT)
sprite_sheet = SpriteSheet(image_sheet)
initial_x = HDPI["HORIZON"]["x"]
initial_y = HDPI["HORIZON"]["y"]
initial_horizon_image = sprite_sheet.getImage(initial_x, initial_y, background_width, background_height)
window.blit(initial_horizon_image, (0, HEIGHT - background_height - 100))
cloud = Cloud(sprite_sheet, HDPI)
dino = Dino(sprite_sheet, HDPI)
run = True
new_x = initial_x
new_background_width = 0
frameCount = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        run = False

#    print(new_x)
    window.fill( (247,247,247))
    new_horizon_image = sprite_sheet.getImage(new_x, initial_y, background_width - new_x, background_height)
    new_horizon_image2 = sprite_sheet.getImage(initial_x, initial_y, new_x, background_height)
    window.blit(new_horizon_image, (0, HEIGHT - background_height - 100))
    window.blit(new_horizon_image2, (background_width - new_x, HEIGHT - background_height - 100))
    window.blit(cloud.getCloud(), (300, 200))
    window.blit(dino.getIdleImage(), (10, HEIGHT - background_height - 160))
    pygame.display.flip()
    new_x += 10
    new_x = new_x % background_width
    pygame.time.delay(msPerFrame)
    frameCount+=1


pygame.quit()
