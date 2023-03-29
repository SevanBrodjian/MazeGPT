import pygame
import sys
import openai
import os
import time

openai.api_key = os.getenv("OPENAI_GPT4_KEY")

output = open("Chat_Log.txt", "w")
output.write("\n--------------------------------------------------------------------------------------------------------------\n")

player_name = "GPT-4"
with open("start_prompt.txt", "r") as f:
    start_prompt = f.read()

messages=[
        {"role": "user", "content": start_prompt + " For example, how could you respond to: Available moves: U, D, L".replace('\n', '')},
        {"role": "assistant", "content": "D"},
        {"role": "user", "content": "That's correct. Please send confirm to acknowledge these rules. Good luck!"},
        {"role": "assistant", "content": "confirm"}
    ]

# Infinite corridor:
# maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

maze = [[0, 0, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0]]

user_location = [0, 0]
goal_location = [3, 1]

screen_width = 500
screen_height = 500
block_x = screen_width/len(maze[0])
block_y = screen_height/len(maze)
border = 10 # Border around blocks (walls and player)

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("MazeGPT")

wall = pygame.Surface([block_x-border, block_y-border])
wall.fill([25, 25, 25])

user = pygame.Surface([block_x-border, block_y-border])
user.fill([200, 25, 25])
 
goal = pygame.Surface([block_x-border, block_y-border])
goal.fill([25, 200, 25])

def get_user_input(game_state):
    response = prompt_and_add(game_state)
    if("U" in response and "D" not in response and "L" not in response and "R" not in response):
        response = "U"
    if("D" in response and "U" not in response and "L" not in response and "R" not in response):
        response = "D"
    if("L" in response and "D" not in response and "U" not in response and "R" not in response):
        response = "L"
    if("R" in response and "D" not in response and "L" not in response and "U" not in response):
        response = "R"
    return response

def alert_user(message):
    prompt_and_add(message)

def prompt_and_add(msg):
    # msg = "You are in a 2D maze and can navigate by sending \"U\", \"D\", \"L\", \"R\" " + msg
    new_message = {"role":"user", "content":msg}
    messages.append(new_message)
    output.write("SYSTEM: " + messages[-1]['content'] + "\n")

    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)["choices"][0]["message"]["content"]
    messages.append({"role":"assistant", "content":response})
    output.write(player_name + ": " + messages[-1]['content'] + "\n")

    return response

pygame.init()

while True:
    # Set the background to white
    screen.fill([255, 255, 255])

    # Draw walls and user
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if(user_location == [i, j]):
                screen.blit(user, [j*block_x+border/2, i*block_y+border/2])
            elif(goal_location == [i, j]):
                screen.blit(goal, [j*block_x+border/2, i*block_y+border/2])
            elif(maze[i][j] == 1):
                screen.blit(wall, [j*block_x+border/2, i*block_y+border/2])

    pygame.display.update()

    if(user_location == goal_location):
        alert_user("Congratulations! You have reached the goal.")
        output.close()
        quit()

    goal_msg = ""
    if([user_location[0]-1, user_location[1]] == goal_location):
        goal_msg = "You see the goal is one block above you. "
    if([user_location[0]+1, user_location[1]] == goal_location):
        goal_msg = "You see the goal is one block beneath you. "
    if([user_location[0], user_location[1]-1] == goal_location):
        goal_msg = "You see the goal is one block to your left. "
    if([user_location[0], user_location[1]+1] == goal_location):
        goal_msg = "You see the goal is one block to your right. "

    top_open = (user_location[0] > 0) and (maze[user_location[0]-1][user_location[1]] == 0)
    bottom_open = (user_location[0] < len(maze)-1) and (maze[user_location[0]+1][user_location[1]] == 0)
    left_open = (user_location[1] > 0) and (maze[user_location[0]][user_location[1]-1] == 0)
    right_open = (user_location[1] < len(maze[0])-1) and (maze[user_location[0]][user_location[1]+1] == 0)

    game_state = goal_msg + "Available Moves: " + ("U" if top_open else "") + (" D" if bottom_open else "") + (" L" if left_open else "") + (" R" if right_open else "")
    game_state = game_state + ". There are walls in these directions: " + ("" if top_open else "U") + ("" if bottom_open else " D") + ("" if left_open else " L") + ("" if right_open else " R")
    game_state = game_state.strip()
    

    error_msg = "error"
    while(error_msg != ""):
        print("Thinking...")
        thought = get_user_input(game_state + " First, briefly explain your thoughts to make a more informed next move(s), saving a model of the world if necessary")
        move = get_user_input((error_msg if error_msg != "error" else "") + "What will your move be?")
        print(thought + '\n' + move)
        time.sleep(4)

        error_msg = ""

        if(move == 'U'):
            if(top_open):
                user_location[0] = user_location[0]-1
            else:
                error_msg = "Invalid move up.  No move executed. "
        elif(move == 'D'):
            if(bottom_open):
                user_location[0] = user_location[0]+1
            else:
                error_msg = "Invalid move down. No move executed. "
        elif(move == 'L'):
            if(left_open):
                user_location[1] = user_location[1]-1
            else:
                error_msg = "Invalid move left. No move executed. "
        elif(move == 'R'):
            if(right_open):
                user_location[1] = user_location[1]+1
            else:
                error_msg = "Invalid move right. No move executed. "
        else:
            error_msg = "Unknown command, please only respond with either U, D, L, or R and no other text. No move executed. "

        # if(error_msg != ""):
        #     alert_user(error_msg)

    pygame.display.update()