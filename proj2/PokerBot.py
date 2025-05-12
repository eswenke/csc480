"""
RULES ***
Players: 
    - 2 (your bot vs. one opponent).
No Betting: 
    - Decisions are limited to “fold” or “stay.”
Card Dealing Phases:
    - Pre-Flop: Each player receives 2 private cards (hole cards).
    - Flop: 3 community cards are revealed.
    - Turn: 1 additional community card is revealed.
    - River: 1 final community card is revealed.
Decision Points: 
    - Before each phase bot has 10 seconds to decide whether to fold or stay.
Hidden Information:
    - Your bot can see its own hole cards and any revealed community cards.
    - The opponent's hole cards remain hidden unless both players stay until the River.
Win Condition: 
    - If neither player folds, the highest-ranking hand wins

REQUIREMENTS ***
    - Implement Monte Carlo Tree Search (MCTS)
    - Estimate winning probability at each decision point
    - For each decision:
        - Random Rollouts:
            - Similute possible opponent cards (just in their hand)
            - Simulate random community cards
            - Play out the showdown randomly
        - Select Policy:
            - Use UCB1 to guide exploration during simulations
            - Track wins vs. losses
            - Calculate Win probability as wins/simulations
        - Decision Rule:
            - Stay (check) if win probability is greater than or equal to 50%
            - Fold if less than 50%
        - Complete all simulations and decision making within 10 seconds at each decision point

TECHNICAL DETAILS ***
    - Represent each hand as a tuple ('2', 'S') for 2 of spades, ('A', 'H') for Ace of Hearts, etc.
    - Community cards are a list of 3, 4, or 5 cards
    - Deck Management:
        - Implement shuffling and drawing mechanics
        - Ensure no duplicate cards are drawn
        - Simulate from the remaining deck correctly
    - Hand Evaluation:
        - Implement a function to evaluate hand rankings
    - Maximize the number of simulations done within the 10 seconds
    - Implement all components from scratch (deck, evaluation, rollout, etc.)

"""
from ast import Tuple
import random


DECK = [
    (2, 'H'), (2, 'D'), (2, 'C'), (2, 'S'),
    (3, 'H'), (3, 'D'), (3, 'C'), (3, 'S'),
    (4, 'H'), (4, 'D'), (4, 'C'), (4, 'S'),
    (5, 'H'), (5, 'D'), (5, 'C'), (5, 'S'),
    (6, 'H'), (6, 'D'), (6, 'C'), (6, 'S'),
    (7, 'H'), (7, 'D'), (7, 'C'), (7, 'S'),
    (8, 'H'), (8, 'D'), (8, 'C'), (8, 'S'),
    (9, 'H'), (9, 'D'), (9, 'C'), (9, 'S'),
    (10, 'H'), (10, 'D'), (10, 'C'), (10, 'S'),
    (11, 'H'), (11, 'D'), (11, 'C'), (11, 'S'),
    (12, 'H'), (12, 'D'), (12, 'C'), (12, 'S'),
    (13, 'H'), (13, 'D'), (13, 'C'), (13, 'S'),
    (14, 'H'), (14, 'D'), (14, 'C'), (14, 'S'),
]

HAND_RANKS = {
    "High Card": 1,
    "Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}

def ucb1(wins, simulations, total_simulations, c=1.41):
    """
    Calculates the Upper Confidence Bound 1 (UCB1) value for node selection in MCTS.
    Balances exploration and exploitation during the selection phase.
    """
    pass

def draw_cards(deck, num_cards):
    """
    Draws a specified number of cards from the deck.
    Returns the drawn cards and the remaining deck.
    """
    pass

def evaluate_hand(hole_cards, community_cards):
    """
    Evaluates the best 5-card poker hand from the given hole cards and community cards.
    Returns the hand rank and the best 5-card combination.
    """
    hearts = []
    spades = []
    clubs = []
    diamonds = []
    flush = []
    straight = []
    four_oak = []
    three_oak = []
    pair1 = []
    pair2 = []
    best_hand = []
    rank = 1
    numbers = {}
    
    # first start by combining the hold and community cards
    combined_hand = hole_cards + community_cards

    combined_hand.sort()

    for tuple in combined_hand:
        # dictionary for pairs, 3 oak, 4 oak
        if tuple[0] not in numbers:
            numbers[tuple[0]] = [tuple]
        else:
            numbers[tuple[0]].append(tuple)

            if len(numbers[tuple[0]]) == 2:
                # build pairs first
                if len(pair2) == 0 or tuple[0] > pair2[0][0]:
                    pair2 = numbers[tuple[0]]
                elif len(pair1) == 0 or tuple[0] > pair1[0][0]:
                    pair1 = numbers[tuple[0]]
                
                # ensures that pair 1 is the highest pair 
                if len(pair2) > 0 and len(pair1) > 0 and pair2[0][0] > pair2[0][0]:
                    pair1, pair2 = pair2, pair1
            
            if len(numbers[tuple[0]]) == 3:
                if len(three_oak) == 0 or tuple[0] > three_oak[0][0]:
                    three_oak = numbers[tuple[0]]
                
                # erase pair if 3 oak created from that pair
                if tuple[0] == pair1[0][0]:
                    pair1 = []
                elif tuple[0] == pair2[0][0]:
                    pair2 = []

            if len(numbers[tuple[0]]) == 4:
                if len(four_oak) == 0 or tuple[0] > four_oak[0][0]:
                    four_oak = numbers[tuple[0]]
                
                # erase three_oak because we created 4
                three_oak = []

        # gather lists of same suit from combined hand
        if tuple[1] == 'H':
            hearts.append(tuple)
        elif tuple[1] == 'D':
            diamonds.append(tuple)
        elif tuple[1] == 'S':
            spades.append(tuple)
        elif tuple[1] == 'C':
            clubs.append(tuple)

    # check for straight
    values = sorted(set(tuple[0] for tuple in combined_hand))

    if set([2, 3, 4, 5, 14]).issubset(values):
        # account for low ace straight
        straight = set([2, 3, 4, 5, 14])

    for i in range(len(values)):
        # begin potential straight
        current_straight = [values[i]]

        # check from here for the rest of the straight
        for j in range(i + 1, len(values)):
            if values[j] == current_straight[i] + 1:
                # add to current straight
                current_straight.append(values[j])
                if (len(current_straight) >= 5):
                    straight = current_straight
            else:
                # begin next potential straight
                break

    # put actual tuples in straight
    new_straight = []
    for tuple in combined_hand:
        if tuple[0] in straight:
            new_straight.append(tuple)
            straight.remove(tuple[0])
    new_straight = new_straight[-5:]

    # check if royal flush or straight flush
    if len(new_straight) >= 5:
        if len(hearts) >= 5:
            flush = sorted(hearts)[-5:]
        elif len(diamonds) >= 5:
            flush = sorted(diamonds)[-5:]
        elif len(clubs) >= 5:
            flush = sorted(clubs)[-5:]
        elif len(spades) >= 5:
            flush = sorted(spades)[-5:]

        if len(flush) > 0 and new_straight[-1][0] == flush[-1][0]:
            if new_straight[-1][0] == 14:
                best_hand = new_straight
                rank = HAND_RANKS['Royal Flush']
                return best_hand, rank
            else:
                best_hand = new_straight
                rank = HAND_RANKS['Straight Flush']
                return best_hand, rank
        
    # check if 4 oak
    if len(four_oak) > 0:
        best_hand = four_oak + get_high_cards(combined_hand, four_oak)
        rank = HAND_RANKS['Four of a Kind']

        assert(len(best_hand) == 5)

        return best_hand, rank

    # check if full house
    if len(three_oak) > 0:
        rank - HAND_RANKS['Full House']
        
        if len(pair1) > 0:
            best_hand = three_oak + pair1
        if len(pair2) > 0:
            best_hand = three_oak + pair1

        return best_hand, rank

    # check if flush
    if len(flush) > 0:
        best_hand = flush
        rank = HAND_RANKS['Flush']

        return best_hand, rank

    # check if straight
    if len(new_straight) > 0:
        best_hand = new_straight
        rank = HAND_RANKS['Straight']

        return best_hand, rank
            
    # check if 3 oak
    if len(three_oak) > 0:
        best_hand = three_oak + get_high_cards(combined_hand, three_oak)
        rank = HAND_RANKS['Three of a Kind']

        assert(len(best_hand) == 5)

        return best_hand, rank

    # check if two pair
    if len(pair1) > 0 and len(pair2) > 0:
        best_hand = pair1 + pair2 + get_high_cards(combined_hand, pair1 + pair2)
        rank = HAND_RANKS['Two Pair']

        return best_hand, rank

    # check if pair (will be pair2)
    if len(pair2) > 0:
        best_hand = pair2 + get_high_cards(combined_hand, pair2)
        rank = HAND_RANKS['Pair']
        
        return best_hand, rank

    best_hand = get_high_cards(combined_hand, [])
    rank = HAND_RANKS['High Card']

    return best_hand, rank

def get_high_cards(combined_hand, best_hand):
    # retrieve next best cards in a hand
    cards = []

    num_cards = 5 - len(best_hand)
    cards_left = [card for card in combined_hand if card not in best_hand]
    cards_left = cards_left[::-1]

    # loop the num of cards left
    for i in range(num_cards):
        cards.append(cards_left[i])

    return cards

def mcts(hole_cards, community_cards, remaining_deck, time_limit=10):

    """
    Main Monte Carlo Tree Search function that decides whether to fold or stay.
    Uses UCB1 for node selection and simulates potential outcomes.
    Returns the decision (fold/stay) and the estimated win probability.
    """
    pass


def rollout(node, remaining_deck):
    """
    Performs a random simulation from the current game state to the end.
    Simulates opponent's cards and remaining community cards randomly.
    Returns the outcome (win/loss) of the simulation.
    """
    pass


def selection(node):
    """
    Selects the most promising node in the tree using UCB1 formula.
    Balances between exploration and exploitation.
    Returns the selected node for further expansion or simulation.
    """
    pass


def expansion(node, remaining_deck):
    """
    Creates new child nodes for the selected node.
    Represents possible future game states.
    Returns the newly created child node.
    """
    pass


def backpropagation(node, result):
    """
    Updates node statistics (wins, simulations) after a simulation.
    Propagates the result up the tree to the root node.
    """
    pass


def main():
    """
    Main function that handles the game flow.
    Manages the poker rounds, decision points, and interfaces with the game environment.
    """

    # start with a shuffled deck
    deck = DECK.copy()
    random.shuffle(deck)


