# reinforcement-learning-blackjack
An epsilon-greedy reinforcement learning program that plays Backjack and gets better the more it plays.

Was created following this tutorial on Monte Carlo Methods of reinforcement learning: http://outlace.com/Reinforcement-Learning-Part-2/

The program plays the game of blackjack a number of times, set by the number of epochs.  It displays a graph of its performance once it has finished.  It uses an epsilon-greedy policy, where currently, the chance of the program performing a random action is 0.1.

The game itself is blackjack.py, which is imported into reinforcement_learning_blackjack_player.py, where it is run.
