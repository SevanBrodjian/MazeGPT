import pygame
import pandas as pd
import ast

games = pd.read_csv('games.csv')
games = games.applymap(lambda x: ast.literal_eval(x))
game_num = -1

maze = games.iloc[game_num]['maze']
moves = games.iloc[game_num]['moves']
user_location = moves[0]
goal_location = games.iloc[game_num]['goal']
thoughts = games.iloc[game_num]['thoughts']
mental_models = games.iloc[game_num]['mental_models']
print(thoughts[0])
print(mental_models[0])
index = 0

x_blocks = len(maze[0])
y_blocks = len(maze)
screen_width = 100*x_blocks
screen_height = 100*y_blocks
block_x = screen_width/x_blocks
block_y = screen_height/y_blocks
border = 10 # Border around blocks (walls and player)

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("MazeGPT")

wall = pygame.Surface([block_x-border, block_y-border])
wall.fill([25, 25, 25])

user = pygame.Surface([block_x-border, block_y-border])
user.fill([200, 25, 25])
 
goal = pygame.Surface([block_x-border, block_y-border])
goal.fill([25, 200, 25])

pygame.init()
running = True
key_pressed = False

while running:
    # Set the background to white
    screen.fill([255, 255, 255])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not key_pressed:
                index = min(len(moves)-1, index + 1)
                thought = thoughts[index]
                user_location = moves[index]
                mental_model = mental_models[index]
                print(thought)
                print(mental_model)
                key_pressed = True
            if event.key == pygame.K_LEFT and not key_pressed:
                index = max(0, index - 1)
                thought = thoughts[index]
                user_location = moves[index]
                mental_model = mental_models[index]
                print(thought)
                print(mental_model)
                key_pressed = True
        elif event.type == pygame.KEYUP:
            key_pressed = False

    # Draw walls and user
    for i in range(y_blocks):
        for j in range(x_blocks):
            if(user_location == [i, j]):
                screen.blit(user, [j*block_x+border/2, i*block_y+border/2])
            elif(goal_location == [i, j]):
                screen.blit(goal, [j*block_x+border/2, i*block_y+border/2])
            elif(maze[i][j] == 1):
                screen.blit(wall, [j*block_x+border/2, i*block_y+border/2])

    pygame.display.update()

pygame.quit()