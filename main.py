import sys
import random
import pygame
# Initialize pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CHARACTER_SPEED = 10  # Increased speed for faster movement
FONT_SIZE = 40
MENU_OPTIONS = ["Start Game", "Options", "Load Game", "Multiplayer", "Inventory", "Trade", "Exit"]  # Added "Trade" option
SUBMENU_OPTIONS = ["More Fields", "More Animals", "More Items"]
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
FIELD_COLOR = (0, 255, 0)
POTATO_COLOR = (165, 42, 42)

# Load music
pygame.mixer.music.load('Music.mp3')  # Music for menu
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)

# Load images
map_image = pygame.image.load('Map.jpg')  # Replace with your actual map image file path
character_image = pygame.image.load('character.png')  # Correct path to farmer_male.png

# Scale images (if necessary)
map_image = pygame.transform.scale(map_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
character_image = pygame.transform.scale(character_image, (50, 50))  # Adjust size as needed

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Farming Game')  # Corrected set_caption

# Font for menu
font = pygame.font.Font(None, FONT_SIZE)

# Initial position of the character
character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Inventory
inventory = {
    "fields": {
        "plains": 1,
        "forest": 1,
        "hills": 0
    },
    "animals": {
        "cows": 1,
        "chickens": 2,
        "sheep": 0
    },
    "items": {
        "tractor": 1,
        "fruits": 5,
        "vegetables": 8,
        "potatoes": 0,
        "tomatoes": 0,  # New item to store tomatoes
        "cucumbers": 0  # New item to store cucumbers
    },
    "money": 100
}

# Prices for trading
prices = {
    "fields": {
        "plains": 100,
        "forest": 150,
        "hills": 200
    },
    "items": {
        "fruits": 5,
        "vegetables": 8,
        "potatoes": 3,
        "tomatoes": 4,
        "cucumbers": 2
    }
}

# Game states
menu_selected = 0  # Initialize menu_selected
submenu_selected = 0
in_menu = True
in_submenu = False
in_inventory = False
in_mini_game = False  # Track if the player is in the potato mini-game
in_trade = False  # New state for trading

# Potato field area (the area on the map where the player can start the mini-game)
potato_field_rect = pygame.Rect(200, 200, 100, 100)

# Inventory button on map
inventory_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 130, 40)

# Menu button on map
menu_button_rect = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 50, 130, 40)

# Exit button in inventory
exit_inventory_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT - 100, 130, 40)

# Exit button in mini-game
exit_mini_game_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT - 100, 130, 40)

# Potatoes in the mini-game
potatoes = []

# Add crop selection options (with "Exit")
CROP_OPTIONS = ["Potatoes", "Tomatoes", "Cucumbers", "Exit"]  # Added "Exit" option
crop_selected = 0  # Initialize selected crop to the first one

# Draw the main menu
def draw_menu():
    screen.fill(BLACK)
    for i, option in enumerate(MENU_OPTIONS):
        if i == menu_selected:
            label = font.render(option, True, WHITE)
        else:
            label = font.render(option, True, GRAY)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 200 + i * 60))

# Draw the submenu
def draw_submenu():
    screen.fill(BLACK)
    for i, option in enumerate(SUBMENU_OPTIONS):
        if i == submenu_selected:
            label = font.render(option, True, WHITE)
        else:
            label = font.render(option, True, GRAY)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 200 + i * 60))

# Draw the inventory
def draw_inventory():
    screen.fill(BLACK)
    
    # Display different categories of the inventory
    inventory_text = [
        f"Fields - Plains: {inventory['fields']['plains']}",
        f"Fields - Forest: {inventory['fields']['forest']}",
        f"Fields - Hills: {inventory['fields']['hills']}",
        f"Animals - Cows: {inventory['animals']['cows']}",
        f"Animals - Chickens: {inventory['animals']['chickens']}",
        f"Animals - Sheep: {inventory['animals']['sheep']}",
        f"Items - Tractor: {inventory['items']['tractor']}",
        f"Items - Fruits: {inventory['items']['fruits']}",
        f"Items - Vegetables: {inventory['items']['vegetables']}",
        f"Items - Potatoes: {inventory['items']['potatoes']}",
        f"Items - Tomatoes: {inventory['items']['tomatoes']}",
        f"Items - Cucumbers: {inventory['items']['cucumbers']}",
        f"Money: ${inventory['money']}"
    ]
    
    for i, text in enumerate(inventory_text):
        label = font.render(text, True, WHITE)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 100 + i * 40))

    # Draw exit button
    pygame.draw.rect(screen, GRAY, exit_inventory_button_rect)
    exit_label = font.render("Return", True, WHITE)
    screen.blit(exit_label, (exit_inventory_button_rect.x + (exit_inventory_button_rect.width - exit_label.get_width()) // 2,
                             exit_inventory_button_rect.y + (exit_inventory_button_rect.height - exit_label.get_height()) // 2))

# Draw the potato field on the map
def draw_potato_field():
    pygame.draw.rect(screen, FIELD_COLOR, potato_field_rect)

# Function to randomly increase fields, animals, or items
def increase_resources(choice):
    if choice == "fields":
        field_type = random.choice(["plains", "forest", "hills"])
        additional_fields = random.randint(1, 3)  # Randomly add between 1 and 3 fields
        inventory['fields'][field_type] += additional_fields
        print(f"Received {additional_fields} more {field_type} fields!")
    elif choice == "animals":
        animal_type = random.choice(["cows", "chickens", "sheep"])
        additional_animals = random.randint(1, 5)  # Randomly add between 1 and 5 animals
        inventory['animals'][animal_type] += additional_animals
        print(f"Received {additional_animals} more {animal_type}!")
    elif choice == "items":
        item_type = random.choice(["tractor", "fruits", "vegetables"])
        additional_items = random.randint(1, 10)  # Randomly add between 1 and 10 items
        inventory['items'][item_type] += additional_items
        print(f"Received {additional_items} more {item_type}!")

# Draw inventory button on map
def draw_inventory_button():
    pygame.draw.rect(screen, GRAY, inventory_button_rect)
    label = font.render("Inventory", True, WHITE)
    screen.blit(label, (inventory_button_rect.x + (inventory_button_rect.width - label.get_width()) // 2,
                        inventory_button_rect.y + (inventory_button_rect.height - label.get_height()) // 2))

# Draw menu button on map
def draw_menu_button():
    pygame.draw.rect(screen, GRAY, menu_button_rect)
    label = font.render("Menu", True, WHITE)
    screen.blit(label, (menu_button_rect.x + (menu_button_rect.width - label.get_width()) // 2,
                        menu_button_rect.y + (menu_button_rect.height - label.get_height()) // 2))

# Start the mini-game (generate crops based on selection)
def start_mini_game():
    global potatoes
    potatoes = []
    for _ in range(5):  # Spawn 5 crops (potatoes, tomatoes, or cucumbers)
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        potatoes.append(pygame.Rect(x, y, 20, 20))  # Each crop is a 20x20 square

# Draw the mini-game (crop collecting)
potato_field_image = pygame.image.load('potato_field.jpg')
tomato_field_image=pygame.image.load('pszenica_field.jpg')
Cocembers_field_image=pygame.image.load('Pomidory1.jpg')
# Draw the mini-game (crop collecting)
potao_image=pygame.image.load("Pomidór.png")
tomato_image=pygame.image.load("ziemniór.png")
cucember=pygame.image.load("ogór.png")

def draw_mini_game():
    screen.blit(potato_field_image, (0, 0))
    # Set the color based on the selected crop
    if CROP_OPTIONS[crop_selected] == "Potatoes":
        screen.blit(potato_field_image, (0, 0))
        crop_color = (255, 0, 0)
    elif CROP_OPTIONS[crop_selected] == "Tomatoes":
        screen.blit(tomato_field_image, (0, 0))
        crop_color = (255, 0, 0)  # Red for tomatoes
    elif CROP_OPTIONS[crop_selected] == "Cucumbers":
        screen.blit(Cocembers_field_image, (0, 0))
        crop_color = (0, 255, 0)  # Green for cucumbers

    for potato in potatoes:
        pygame.draw.rect(screen, crop_color, potato)

    # Draw exit button in mini-game
    pygame.draw.rect(screen, GRAY, exit_mini_game_button_rect)
    exit_label = font.render("Exit", True, WHITE)
    screen.blit(exit_label, (exit_mini_game_button_rect.x + (exit_mini_game_button_rect.width - exit_label.get_width()) // 2,
                             exit_mini_game_button_rect.y + (exit_mini_game_button_rect.height - exit_label.get_height()) // 2))

# Add crop selection menu (with "Exit" option)
def draw_crop_selection():
    screen.fill(BLACK)
    for i, option in enumerate(CROP_OPTIONS):
        if i == crop_selected:
            label = font.render(option, True, WHITE)
        else:
            label = font.render(option, True, GRAY)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 200 + i * 60))

# Switch music when starting the game
def switch_to_game_music():
    pygame.mixer.music.stop()  # Stop menu music
    pygame.mixer.music.load('Drum.mp3')  # Load game music
    pygame.mixer.music.play(-1)  # Play game music in a loop

# New function to draw the trading interface
def draw_trade():
    screen.fill(BLACK)
    title = font.render("Trading", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    y_offset = 150
    for category in ["fields", "items"]:
        for item, price in prices[category].items():
            item_text = f"{item.capitalize()}: Buy ${price} / Sell ${price // 2}"
            label = font.render(item_text, True, WHITE)
            screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, y_offset))
            y_offset += 40

    money_text = f"Your money: ${inventory['money']}"
    money_label = font.render(money_text, True, WHITE)
    screen.blit(money_label, (SCREEN_WIDTH // 2 - money_label.get_width() // 2, y_offset + 40))

    exit_label = font.render("Press ESC to exit", True, GRAY)
    screen.blit(exit_label, (SCREEN_WIDTH // 2 - exit_label.get_width() // 2, SCREEN_HEIGHT - 50))

# Function to handle buying items
def buy_item(category, item):
    if inventory['money'] >= prices[category][item]:
        inventory['money'] -= prices[category][item]
        if category == "fields":
            inventory['fields'][item] += 1
        else:
            inventory['items'][item] += 1
        print(f"Bought 1 {item} for ${prices[category][item]}")
    else:
        print("Not enough money!")

# Function to handle selling items
def sell_item(category, item):
    if category == "fields" and inventory['fields'][item] > 0:
        inventory['fields'][item] -= 1
        inventory['money'] += prices[category][item] // 2
        print(f"Sold 1 {item} for ${prices[category][item] // 2}")
    elif category == "items" and inventory['items'][item] > 0:
        inventory['items'][item] -= 1
        inventory['money'] += prices[category][item] // 2
        print(f"Sold 1 {item} for ${prices[category][item] // 2}")
    else:
        print(f"Not enough {item} to sell!")

# Main game loop
running = True
crop_selection_active = False  # New flag for crop selection menu

# Play menu music
pygame.mixer.music.play(-1)  # Play menu music in a loop

# Main game loop (continued)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_selected = (menu_selected - 1) % len(MENU_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    menu_selected = (menu_selected + 1) % len(MENU_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if menu_selected == 0:  # Start Game
                        in_menu = False
                        in_submenu = True  # Switch to submenu
                        switch_to_game_music()  # Switch to game music
                    elif menu_selected == 5:  # Trade
                        in_menu = False
                        in_trade = True
                    elif menu_selected == 6:  # Exit
                        running = False
        elif in_submenu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    submenu_selected = (submenu_selected - 1) % len(SUBMENU_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    submenu_selected = (submenu_selected + 1) % len(SUBMENU_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if submenu_selected == 0:  # More Fields
                        increase_resources("fields")
                        in_submenu = False  # Exit submenu and start the game
                    elif submenu_selected == 1:  # More Animals
                        increase_resources("animals")
                        in_submenu = False  # Exit submenu and start the game
                    elif submenu_selected == 2:  # More Items
                        increase_resources("items")
                        in_submenu = False  # Exit submenu and start the game
        elif in_trade:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_trade = False
                    in_menu = True
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    index = event.key - pygame.K_1
                    if index < len(prices['fields']):
                        item = list(prices['fields'].keys())[index]
                        buy_item('fields', item)
                elif event.key in [pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                    index = event.key - pygame.K_6
                    if index < len(prices['items']):
                        item = list(prices['items'].keys())[index]
                        buy_item('items', item)
                elif event.key in [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t]:
                    index = event.key - pygame.K_q
                    if index < len(prices['fields']):
                        item = list(prices['fields'].keys())[index]
                        sell_item('fields', item)
                elif event.key in [pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p]:
                    index = event.key - pygame.K_y
                    if index < len(prices['items']):
                        item = list(prices['items'].keys())[index]
                        sell_item('items', item)
        elif crop_selection_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    crop_selected = (crop_selected - 1) % len(CROP_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    crop_selected = (crop_selected + 1) % len(CROP_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if crop_selected == len(CROP_OPTIONS) - 1:  # "Exit" option selected
                        crop_selection_active = False  # Exit crop selection menu without starting mini-game
                    else:
                        crop_selection_active = False  # Exit crop selection menu and start mini-game
                        in_mini_game = True
                        start_mini_game()
        elif in_inventory:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_inventory_button_rect.collidepoint(event.pos):  # Check if exit button is clicked
                    in_inventory = False  # Exit inventory and return to game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Escape to return to game
                    in_inventory = False
        elif in_mini_game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_mini_game_button_rect.collidepoint(event.pos):  # Exit mini-game button clicked
                    in_mini_game = False  # Exit mini-game and return to map
                    potatoes = []  # Clear potatoes when exiting
                else:
                    # Handle crop collection
                    for potato in potatoes[:]:  # Use a copy of the list to safely remove items
                        if potato.collidepoint(event.pos):
                            potatoes.remove(potato)
                            if CROP_OPTIONS[crop_selected] == "Potatoes":
                                inventory['items']['potatoes'] += 1  # Add potato to inventory
                                print("Collected a potato!")
                            elif CROP_OPTIONS[crop_selected] == "Tomatoes":
                                inventory['items']['tomatoes'] += 1  # Add tomato to inventory
                                print("Collected a tomato!")
                            elif CROP_OPTIONS[crop_selected] == "Cucumbers":
                                inventory['items']['cucumbers'] += 1  # Add cucumber to inventory
                                print("Collected a cucumber!")
                if len(potatoes) == 0:
                    in_mini_game = False  # Exit mini-game when all crops are collected
        else:
            # Check if user clicked on inventory button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inventory_button_rect.collidepoint(event.pos):
                    in_inventory = True  # Switch to inventory view
                elif menu_button_rect.collidepoint(event.pos):
                    in_menu = True  # Return to menu

            # Check if character entered the potato field to start the crop selection
            if potato_field_rect.collidepoint(character_x, character_y) and not crop_selection_active and not in_mini_game:
                crop_selection_active = True  # Open crop selection menu

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
            character_x = max(0, min(SCREEN_WIDTH - character_image.get_width(), character_x))
            character_y = max(0, min(SCREEN_HEIGHT - character_image.get_height(), character_y))

    # Drawing logic
    if in_menu:
        draw_menu()
    elif in_submenu:
        draw_submenu()
    elif in_trade:
        draw_trade()
    elif crop_selection_active:
        draw_crop_selection()
    elif in_inventory:
        draw_inventory()
    elif in_mini_game:
        draw_mini_game()
    else:
        # Draw map and character
        screen.fill(BLACK)  # Clear the screen
        screen.blit(map_image, (0, 0))
        screen.blit(character_image, (character_x, character_y))
        draw_inventory_button()
        draw_menu_button()
        draw_potato_field()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit pygame
pygame.quit()
sys.exit()