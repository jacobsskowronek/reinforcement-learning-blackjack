import math
import random

# Cards have a 1 in 13 chance of being selected
# Card Values: Ace (1), 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack (10), Queen (10), King (10)
def getRandomCard():
    card = random.randint(1, 13)
    if card > 10:
        card = 10
    return card

# A hand is a tuple of the total card value, and whether there is a useable ace
# Accepts a hand, if the ace can be an 11 without busting the hand, it's useable
def getUseableHand(hand):
    val, ace = hand
    return ((ace) and ((val + 10) <= 21))

def totalValue(hand):
    val, ace = hand
    if (getUseableHand(hand)):
        return (val + 10)
    else:
        return val

def addCard(hand):
    card = getRandomCard()
    val, ace = hand
    ace = False
    if (card == 1):
        ace = True
    return (val + card, ace)

#The first is first dealt a single card, this method finishes off his hand
def evalDealer(dealer_hand):
    while (totalValue(dealer_hand) < 17):
        dealer_hand = addCard(dealer_hand)
    return dealer_hand

# State: (player total, useable_ace), (dealer total, useable ace), game status; e.g. ((15, True), (9, False), 1)
# stay or hit => dec == 0 or 1
def play(state, dec):
    #evaluate
    player_hand = state[0]
    dealer_hand = state[1]

    status = 1

    if dec == 0: # action stay
        # Evaluate game, dealer plays
        dealer_hand = evalDealer(dealer_hand)

        player_total = totalValue(player_hand)
        dealer_total = totalValue(dealer_hand)
        if (dealer_total > 21):
            status = 2 # Player wins
        elif (dealer_total == player_total):
            status = 3 # Draw
        elif (dealer_total < player_total):
            status = 2 # Player wins
        elif (player_total < dealer_total):
            status = 4 # Player loses

    elif dec == 1:
        # If hit, add new card to player's hand
        player_hand = addCard(player_hand)
        d_hand = evalDealer(dealer_hand)
        player_total = totalValue(player_hand)
        if (player_total == 21):
            if (totalValue(d_hand) == 21):
                status = 3 # Draw
            else:
                status = 2 # Player wins
        elif (player_total > 21):
            status = 4 # Player loses
        elif (player_total < 21):
            # Game continues
            status = 1

    state = (player_hand, dealer_hand, status)

    return state


def initGame():
    status = 1
    player_hand = addCard((0, False))
    player_hand = addCard(player_hand)
    dealer_hand = addCard((0, False))
    # Check if player wins from first hand
    if totalValue(player_hand) == 21:
        if totalValue(dealer_hand) == 21:
            status = 3 # Draw
        else:
            status = 2 # Player wins

    state = (player_hand, dealer_hand, status)
    return state


















