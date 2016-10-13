import numpy as np
from blackjack import *

# Create a list of all possible states
def createStateSpace():
    states = []
    for card in range(1, 11):
        for value in range(11, 22):
            states.append((value, False, card))
            states.append((value, True, card))
    return states

# Create a dictionary of all possible state action pairs, with default Q-value of 0
# Q-value lookup table
def createQValueLookupTable(states):
    averageTable = {} # Stores {(state, action) : average}
    for state in states:
        averageTable[(state, 0)] = 0.0
        averageTable[(state, 1)] = 0.0
    return averageTable

# Create dictionary to store how many times a state action pair has been encountered
def createStateActionCount(states):
    countTable = {} # Stores {(state, action) : count}
    for state in states:
        countTable[(state, 0)] = 0
        countTable[(state, 1)] = 0
    return countTable

def updateQTable(average_table, stateActionCount, currentEpochInfo):
    for key in currentEpochInfo:
        average_table[key] = average_table[key] + (1.0 / stateActionCount[key]) * (currentEpochInfo[key] - average_table[key])
    # print(averageTable)
    return average_table

def calculateReward(state):
    outcome = state[2]
    return 3 - outcome

def getAverageRewardForState(state, average_table):
    # print(state)
    hit = average_table[(state, 1)]
    stay = average_table[(state, 0)]
    return np.array([hit, stay])

def chooseAction(state, average_table):
    return np.argmax(getAverageRewardForState(state, average_table)) # Return 0 or 1 depending on max average reward

def getCustomizedState(state):
    playerHand, dealerHand, status = state
    playerValue, playerHasAce = playerHand
    return (playerValue, playerHasAce, dealerHand[0])

if __name__ == "__main__":
    epochs = 1000000
    epsilon = 0.1 # Chance of performing random action regardless of higher average reward

    # Stores every state
    stateSpace = createStateSpace()
    # Stores the table {(state, action) : average reward}
    averageTable = createQValueLookupTable(stateSpace)
    # Stores the table {(state, action) : count} for calculating new averages
    stateActionCount = createStateActionCount(stateSpace)

    for i in range(0, epochs + 1):
        # Create a new game
        gameState = initGame()

        # playerHand = (valueOfHand, hasAce)
        # dealerHand = (valueOfHand, hasAce)
        # status = 1, 2, 3, or 4
        playerHand, dealerHand, status = gameState

        # Keep hitting if player hand is less than 11
        while playerHand[0] < 11:
            playerHand = addCard(playerHand)
            gameState = (playerHand, dealerHand, status)


        customizedState = getCustomizedState(gameState)

        currentEpochInfo = {}
        while gameState[2] == 1:
            # Epsilon greedy action selection
            if (random.random() < epsilon):
                action = random.randint(0, 1)
            else:
                action = chooseAction(customizedState, averageTable)
            stateActionPair = ((customizedState, action))

            currentEpochInfo[stateActionPair] = 0
            stateActionCount[stateActionPair] += 1

            gameState = play(gameState, action)

            customizedState = getCustomizedState(gameState)

        # Game is completed, assign rewards to state action pairs that took place
        for key in currentEpochInfo:
            currentEpochInfo[key] = calculateReward(gameState)

        averageTable = updateQTable(averageTable, stateActionCount, currentEpochInfo)


        if (i % 10000 == 0):
            print(str((i / float(epochs)) * 100) + "% of Epochs finished")








    # # 3d plot of state-value space where no useable Aces are present
    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D
    # from matplotlib import cm
    #
    # fig = plt.figure(figsize=(8, 6))
    # ax = fig.add_subplot(111, projection='3d', )
    #
    # ax.set_xlabel('Dealer card')
    # ax.set_ylabel('Player sum')
    # ax.set_zlabel('State-Value')
    #
    # x, y, z = [], [], []
    # for key in stateSpace:
    #     if (not key[1] and key[0] > 11 and key[2] < 21):
    #         y.append(key[0])
    #         x.append(key[2])
    #         state_value = max([averageTable[(key, 0)], averageTable[(key, 1)]])
    #         z.append(state_value)
    # ax.azim = 230
    # ax.plot_trisurf(x, y, z, linewidth=.02, cmap=cm.jet)
    #
    # fig.show()
    # plt.show()

















