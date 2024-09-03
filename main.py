import pygame
import sys

pygame.init()

SCREEN_WIDTH,SCREEN_HEIGHT =800,600
CHARACTER_SPEED=5
FONT_SIZE=40
MENU_OPTIONS=["START GAME","OPTIONS","LOAD GAME","EXIT"]
BLACK=(0,0,0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


map_image=pygame.image.load("Map.jpg")
Character_image=pygame.image.load("character.png")

map_image=pygame.transform.scale(map_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
Character_image=pygame.transform.scale(Character_image,(50,50))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Farming Game')

# Initial position of the character
character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

font=pygame.font.Font(None,FONT_SIZE)

Menu_Selected=0
in_menu=True

#draw menu function
def draw_menu():
    screen.fill(BLACK)
    for i ,options in enumerate(MENU_OPTIONS):
        if i==Menu_Selected:
            label=font.render(options,True,WHITE)
        else:
            label=font.render(options,True,GRAY)
        screen.blit(label,(SCREEN_WIDTH//-label.get_width() // 2,200+i*60))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_menu:
           if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Menu_Selected = (Menu_Selected - 1) % len(MENU_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    Menu_Selected= (Menu_Selected + 1) % len(MENU_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if Menu_Selected == 0:  # Start Game
                        in_menu = False
                    elif Menu_Selected == 1:  # Options
                        print("Options selected")  # Placeholder for options functionality
                    elif Menu_Selected == 2:  # Load Game
                        print("Load Game selected")  # Placeholder for load game functionality
                    elif Menu_Selected == 3:  # Multiplayer
                        print("Multiplayer selected")  # Placeholder for multiplayer functionality
                    elif Menu_Selected == 4:  # Exit
                        running = False

    if in_menu:
        draw_menu()
    else:
    # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= CHARACTER_SPEED
        if keys[pygame.K_RIGHT]:
            character_x += CHARACTER_SPEED
        if keys[pygame.K_UP]:
            character_y -= CHARACTER_SPEED
        if keys[pygame.K_DOWN]:
            character_y += CHARACTER_SPEED

        # Prevent the character from moving out of bounds
        character_x = max(0, min(SCREEN_WIDTH - Character_image.get_width(), character_x))
        character_y = max(0, min(SCREEN_HEIGHT - Character_image.get_height(), character_y))

        # Draw everything
        screen.blit(map_image, (0, 0))
        screen.blit(Character_image, (character_x, character_y))

    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Quit pygame
pygame.quit()
sys.exit()