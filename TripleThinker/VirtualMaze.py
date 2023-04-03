import sys
import openai
import os
import time
from ChatAgent import ChatAgent
import pandas as pd

def run_game():
    with open("mover_prompt.txt", "r") as f:
        mover_start_prompt = f.read()

    mover = ChatAgent(model = 'gpt-4', start_msg = mover_start_prompt, api_key = os.getenv("OPENAI_GPT4_KEY"))
    mover.add_msg("user", mover_start_prompt + " For example, how could you respond to: Available moves: U, D, L")
    mover.add_msg("assistant", "D")
    mover.add_msg("user", "That's correct. Please send confirm to acknowledge these rules. Good luck!")
    mover.add_msg("assistant", "confirm")

    with open("thinker_prompt.txt", "r") as f:
        thinker_start_prompt = f.read()

    thinker = ChatAgent(model = 'gpt-4', start_msg = thinker_start_prompt)
    thinker.add_msg("user", thinker_start_prompt + " For example, how could you respond to: Available moves: U, D, L. There are walls in these directions: R")
    thinker.add_msg("assistant", "Since there are three choices to go in, and I came from above, this is a fork in the road which I should remember. This time I will go down, but when I come back I should go left.")
    thinker.add_msg("user", "That's correct. Please send confirm to acknowledge these rules. Good luck!")
    thinker.add_msg("assistant", "confirm")

    with open("conceptualizer_prompt.txt", "r") as f:
        conceptualizer_start_prompt = f.read()

    conceptualizer = ChatAgent(model = 'gpt-4', start_msg = conceptualizer_start_prompt)
    conceptualizer.add_msg("user", conceptualizer_start_prompt + " For example, how could you respond to: This is your first move, you are in the top left of the rectangular maze. Available moves: D, R. There are walls in these directions: U, L")
    conceptualizer.add_msg("assistant", "WWWWWW\nWPO??W\nWO???W\nW????W\nW????W\nWWWWWW")
    conceptualizer.add_msg("user", "That's correct. Please send confirm to acknowledge these rules. Good luck!")
    conceptualizer.add_msg("assistant", "confirm")

    with open("conceptualizer_prompt.txt", "r") as f:
        conceptualizer_start_prompt = f.read()

    fixer = ChatAgent(model = 'gpt-4', start_msg = conceptualizer_start_prompt)
    fixer.add_msg("user", conceptualizer_start_prompt + " For example, how could you respond to: This is your first move, you are in the top left of the rectangular maze. Available moves: D, R. There are walls in these directions: U, L")
    fixer.add_msg("assistant", "WWWWWW\nWPO??W\nWO???W\nW????W\nW????W\nWWWWWW")
    fixer.add_msg("user", "That's correct. Please send confirm to acknowledge these rules. Good luck!")
    fixer.add_msg("assistant", "confirm")

    # Infinite corridor:
    # maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    maze = [[0, 0, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 1, 0],
            [1, 0, 1, 0]]
    
    mental_model = "WWWWWW\nWP???W\nW????W\nW????W\nW????W\nWWWWWW"

    user_location = [0, 0]
    goal_location = [3, 1]

    moves = [user_location.copy()]
    thoughts = []
    mental_models = [mental_model]
    move = None

    while True:
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
            if(not move):
                old_model = mental_model
                mental_model = conceptualizer.prompt("Use W to designate a wall, use ? to designate unknown, use P to designate where you are located, use O to designate open unexplored paths, and use X to designate paths that you have already taken. This is your first move, you are in the top-left corner of a rectangular maze. Here is your previous mental model: " + mental_model + " Here is your environment feedback: " + game_state + " What is your mental model of the maze?")
                mental_model = fixer.prompt("This is your first move, you are in the top-left corner of a rectangular maze. Here is your previous mental model: " + mental_model + " Here is your environment feedback: " + game_state + " And here is your updated mental model using that feedback: " + mental_model + " Does this new mental model accurately reflect the environment surrounding the player? Does it only have one player (P)? Does it only use the characters W, ?, P, O, X, G? Write a sentence evaluating this model, then fix it again if necessary otherwise just send the same model.")
                thought = thinker.prompt("This is your first move, you are in the top-left of a rectangular maze. Here is your current mental model of the maze: " + old_model + " Here is your environment feedback: " + game_state +  " Please update the unknown blocks (?) around the player (P) in your mental model using this environmental feedback.")
                move = mover.prompt("This is your first move, you are in the top-left of a rectangular maze. Here is your environment feedback: " + game_state + " And here are your thoughts about the situation and what to do: \"" + thought + "\" What will your move be?")
            elif(error_msg != "error"):
                move = mover.prompt("You did not move due to this error: " + error_msg + "Here is your (unchanged) environment feedback: " + game_state + " And here are your thoughts about the situation and what to do: \"" + thought + "\" What will your move be?")
            else:
                old_model = mental_model
                mental_model = conceptualizer.prompt("Use W to designate a wall, use ? to designate unknown, use P to designate where you are located, use O to designate open unexplored paths, and use X to designate paths that you have already taken. Here is your previous mental model: " + mental_model + "Then, you took this move: " + move + " After that move, here is your environmental feedback: " + game_state + " Please update and share your mental model of the maze.")
                mental_model = fixer.prompt("Here is your previous mental model: " + old_model + " Here is your environment feedback: " + game_state + " And here is your updated mental model using that feedback: " + mental_model + "Then, you took this move: " + move + " Does this new mental model accurately reflect the environment after taking that move and receiving that feedback? Does it only have one player (P)? Does it only use the characters W, ?, P, O, X, G? Write a sentence evaluating this model, then fix it again if necessary otherwise just send the same model.")
                thought = thinker.prompt("Your previous move was: " + move + "Here is your new environment feedback: " + game_state + " And here is your current mental model of the maze: " + mental_model + " Please share your thoughts.")
                move = mover.prompt("You moved " + move + ", here is your new environment feedback: " + game_state + " And here are your thoughts about the situation and what to do: \"" + thought + "\" What will your move be?")
            
            print(mental_model)
            time.sleep(1)

            error_msg = ""

            if(move == 'U'):
                if(top_open):
                    user_location[0] = user_location[0]-1
                else:
                    error_msg = "Invalid move up due to wall.  No move executed. "
            elif(move == 'D'):
                if(bottom_open):
                    user_location[0] = user_location[0]+1
                else:
                    error_msg = "Invalid move down due to wall. No move executed. "
            elif(move == 'L'):
                if(left_open):
                    user_location[1] = user_location[1]-1
                else:
                    error_msg = "Invalid move left due to wall. No move executed. "
            elif(move == 'R'):
                if(right_open):
                    user_location[1] = user_location[1]+1
                else:
                    error_msg = "Invalid move right due to wall. No move executed. "
            else:
                error_msg = "Unknown command, please only respond with either U, D, L, or R and no other text. No move executed. "

        moves.append(user_location.copy())
        thoughts.append(thought)
        mental_models.append(mental_model)

        if(user_location == goal_location):
            thoughts.append(thinker.prompt("Congratulations! You have reached the goal."))
            return moves, thoughts, mental_models, maze, goal_location

        if(len(moves) == 20):
            thoughts.append(thinker.prompt("Unfortunately you have run out of time, we will have to end the simulation. Better luck next time!"))
            return moves, thoughts, mental_models, maze, goal_location

games = pd.read_csv('games.csv')
moves, thoughts, mental_models, maze, goal = run_game()
games.loc[len(games)+1] = [moves, thoughts, mental_models, maze, goal]
print('Saving game...')
games.to_csv('games.csv', index=False)