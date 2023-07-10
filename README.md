# MazeGPT

In this project, I have evaluated the ability for a large language model (GPT-4 and GPT-3) to ground itself in a virtual environment. The project repository consists of two folders: SimpleThinker and TripleThinker. 

## SimpleThinker

The SimpleThinker folder contains the code for running the Maze program in a Pygame window. It displays the maze and saves the transcripts to a text file called `Chat_Log.txt`. To run the Maze program in this mode, execute `Maze.py`.

## TripleThinker

The TripleThinker folder contains an enhanced version of the Maze program. When you run `Maze.py` in TripleThinker, it runs in the background and saves a catalog of all the moves in a CSV file called `games.csv`. This version incorporates three chatbots: the thinker, the mover, and the conceptualizer.

The thinker chatbot generates a "thought" about its current situation using the message history of both chatbots. The mover chatbot selects a move based on the thought generated by the thinker. The conceptualizer chatbot builds and maintains a mental model of the maze using ASCII representation, which is passed to the thinker.

## VirtualMaze

The VirtualMaze folder contains the code for preloading previous games and viewing the moves in a Pygame window. To run the VirtualMaze program, execute `VirtualMaze.py`.

## Experiment Results

The first attempt with GPT-3-based chatbots yielded mediocre results. GPT-3 often got stuck in loops and struggled to navigate the maze effectively. However, after upgrading to GPT-4, the chatbot using SimpleThinker managed to navigate simple mazes and reach the goal most of the time.

To further improve model performance, the TripleThinker approach was introduced. Unfortunately, the addition of the conceptualizer did not yield significant improvements due to GPT-4's inability to maintain a consistent map of its environment.

With additional prompt tuning, it is likely that today's models can navigate small 4x4 or even 5x5 mazes in this environment, especially if the conceptualizer improves its ability to maintain a map. This experiment is particularly interesting as large language models were not specifically trained to be grounded in environmental interactions but can still perform reasonably well in this context.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details