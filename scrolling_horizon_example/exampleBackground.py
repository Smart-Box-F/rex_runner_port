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

def game_window(width, height):
    if width <= 0 or height <= 0:
        raise Exception("Invalid width and height")
    win = pygame.display.set_mode((width,height))
    win.fill( (247,247,247))
    return win

window = game_window(WIDTH, HEIGHT)
sprite_sheet = SpriteSheet(image_sheet)
initial_x = HDPI["HORIZON"]["x"]
initial_y = HDPI["HORIZON"]["y"]
initial_horizon_image = sprite_sheet.getImage(initial_x, initial_y, background_width, background_height)
window.blit(initial_horizon_image, (0, HEIGHT - background_height - 100))
run = True
new_x = initial_x
new_background_width = 0
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
    pygame.display.flip()
    new_x += 10
    new_x = new_x % background_width
    pygame.time.delay(5)


pygame.quit()
