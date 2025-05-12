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
import random
import math
import time


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

class Node:
    """
    Node class for Monte Carlo Tree Search.
    Represents a state in the game tree.
    """
    def __init__(self, hole_cards, community_cards, remaining_deck, parent=None):
        self.hole_cards = hole_cards
        self.community_cards = community_cards.copy() if community_cards else []
        self.remaining_deck = remaining_deck.copy() if remaining_deck else []
        self.parent = parent
        self.children = []
        self.wins = 0
        self.simulations = 0
    
    def add_child(self, hole_cards, community_cards, remaining_deck):
        """
        Creates and adds a child node to this node.
        Returns the newly created child node.
        """
        child = Node(hole_cards, community_cards, remaining_deck, self)
        self.children.append(child)
        return child
    
    def update(self, result):
        """
        Updates node statistics based on simulation result.
        """
        self.simulations += 1
        if result == 1:  # win
            self.wins += 1
    
    def get_ucb(self, total_simulations, c=1.41):
        """
        Calculates the UCB1 value for this node.
        """
        return ucb1(self.wins, self.simulations, total_simulations, c)

def ucb1(wins, simulations, total_simulations, c=1.41):
    """
    Calculates the Upper Confidence Bound 1 (UCB1) value for node selection in MCTS.
    Balances exploration and exploitation during the selection phase.
    """
    # avoid division by zero
    if simulations == 0:
        return float('inf')  # inf value ensures parent nodes are explored first
    
    # exploitation term: win rate
    exploitation = wins / simulations
    
    # exploration term: confidence bound
    exploration = c * math.sqrt(math.log(total_simulations) / simulations)
    
    return exploitation + exploration

def draw_cards(deck, num_cards):
    """
    Draws a specified number of cards from the deck.
    Returns the drawn cards and the remaining deck.
    """
    drawn_cards = []
    remaining_deck = deck.copy()

    for _ in range(num_cards):
        card = remaining_deck.pop(0)
        drawn_cards.append(card)

    return drawn_cards, remaining_deck

def deal_community_cards(deck, phase, existing_community_cards=None):
    """
    Deals community cards based on the current phase.
    """
    if existing_community_cards is None:
        existing_community_cards = []
    
    remaining_deck = deck.copy()
    new_community_cards = existing_community_cards.copy()
    
    # number of cards to deal based on phase
    if phase == 'pre-flop':
        # no community cards yet
        pass
    elif phase == 'flop' and len(existing_community_cards) == 0:
        # deal 3 cards for the flop
        flop_cards, remaining_deck = draw_cards(remaining_deck, 3)
        new_community_cards.extend(flop_cards)
    elif phase == 'turn' and len(existing_community_cards) == 3:
        # deal 1 card for the turn
        turn_card, remaining_deck = draw_cards(remaining_deck, 1)
        new_community_cards.extend(turn_card)
    elif phase == 'river' and len(existing_community_cards) == 4:
        # deal 1 card for the river
        river_card, remaining_deck = draw_cards(remaining_deck, 1)
        new_community_cards.extend(river_card)
    
    return new_community_cards, remaining_deck

def evaluate_hand(hole_cards, community_cards):
    """
    Evaluates the best 5-card poker hand from the given hole cards and community cards.
    Returns the best 5-card combination and the hand rank (1-10, with 10 being the best).
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
                if len(pair1) > 0 and tuple[0] == pair1[0][0]:
                    pair1 = []
                elif len(pair2) > 0 and tuple[0] == pair2[0][0]:
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
            # Check if this card is consecutive with the last card in our current straight
            if values[j] == current_straight[-1] + 1:
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
        rank = HAND_RANKS['Full House']
        
        if len(pair1) > 0:
            best_hand = three_oak + pair1
        elif len(pair2) > 0:
            best_hand = three_oak + pair2

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
    wins = 0
    ties = 0
    losses = 0
    total_simulations = 0
    
    start_time = time.time()
    
    # create root node
    root = Node(hole_cards, community_cards, remaining_deck)
    
    # run simulations until time limit is reached
    while time.time() - start_time < time_limit:
        # selection
        selected_node = selection(root)
        
        # expansion
        if selected_node.simulations > 0:
            selected_node = expansion(selected_node)
        
        # rollout
        result = rollout(selected_node)
        
        # backpropagation
        backpropagation(selected_node, result)
        
        # update overall statistics
        if result == 1:  # Win
            wins += 1
        elif result == 0.5:  # Tie
            ties += 1
        else:  # Loss
            losses += 1
        total_simulations += 1
    
    # calculate win probability (counting ties as half-wins)
    win_probability = (wins + (ties * 0.5)) / total_simulations if total_simulations > 0 else 0
    
    # Print detailed statistics
    print(f"Simulations: {total_simulations}")
    print(f"Wins: {wins} ({wins/total_simulations*100:.1f}%)")
    print(f"Ties: {ties} ({ties/total_simulations*100:.1f}%)")
    print(f"Losses: {losses} ({losses/total_simulations*100:.1f}%)")
    
    # make decision based on win probability
    decision = "stay" if win_probability >= 0.5 else "fold"
    
    return decision, win_probability

def selection(node):
    """
    Selects the most promising node in the tree using UCB1 formula.
    Balances between exploration and exploitation.
    Returns the selected node for further expansion or simulation.
    """
    current = node
    
    # iteratively select the best node until we reach a leaf or unvisited node
    while len(current.children) > 0 and current.simulations > 0:
        # find child with highest UCB1 value
        best_ucb = -float('inf')
        best_child = None
        
        for child in current.children:
            # calculate UCB1 value using the node's method
            ucb_value = child.get_ucb(current.simulations)
            
            # update best child if this one has a higher UCB1 value
            if ucb_value > best_ucb:
                best_ucb = ucb_value
                best_child = child
        
        # if we couldn't find a best child (shouldn't happen), break
        if best_child is None:
            break
            
        current = best_child
    
    return current

def rollout(node):
    """
    Performs a random simulation from the current game state to the end.
    """
    sim_deck = node.remaining_deck.copy()
    random.shuffle(sim_deck)
    

    sim_community = node.community_cards.copy()
    hole_cards = node.hole_cards.copy()
    
    # make sure hole/community cards are not in the simulation deck
    sim_deck = [card for card in sim_deck if card not in hole_cards]
    sim_deck = [card for card in sim_deck if card not in sim_community]
    
    # deal opponent's cards from the remaining deck
    opponent_cards, sim_deck = draw_cards(sim_deck, 2)
    
    # deal remaining community cards (if needed)
    cards_needed = 5 - len(sim_community)
    if cards_needed > 0:
        additional_cards, sim_deck = draw_cards(sim_deck, cards_needed)
    else:
        additional_cards = []
    
    # add the additional cards to the community cards
    full_community = sim_community + additional_cards
    
    # evaluate both hands
    my_best_hand, my_hand_rank = evaluate_hand(hole_cards, full_community)
    opp_best_hand, opp_hand_rank = evaluate_hand(opponent_cards, full_community)
    
    # compare hands (higher rank wins)
    if my_hand_rank > opp_hand_rank:
        return 1  # win
    elif my_hand_rank < opp_hand_rank:
        return 0  # loss
    else:
        # if same rank, compare all cards in descending order
        my_values = sorted([card[0] for card in my_best_hand], reverse=True)
        opp_values = sorted([card[0] for card in opp_best_hand], reverse=True)
        
        for my_val, opp_val in zip(my_values, opp_values):
            if my_val > opp_val:
                return 1  # win
            elif my_val < opp_val:
                return 0  # loss
        
        # if we get here, it's a true tie
        return 0.5 

def expansion(node):
    """
    Creates new child nodes for the selected node.
    Represents possible future game states.
    Returns the newly created child node.
    """
    # create a child node with a slightly different state to avoid cycles
    # we'll create a copy of the remaining deck and shuffle it to represent a different possible world
    remaining_deck = node.remaining_deck.copy()
    
    child = node.add_child(node.hole_cards, node.community_cards, remaining_deck)
    
    return child

def backpropagation(node, result):
    """
    Updates node statistics (wins, simulations) after a simulation.
    Propagates the result up the tree to the root node.
    """
    # iteratively update all nodes from the current node up to the root
    current = node
    while current is not None:
        # update current node using the node's update method
        current.update(result)
        # move to parent
        current = current.parent


def main():
    phases = ['pre-flop', 'flop', 'turn', 'river']
    
    # start with a shuffled deck
    deck = DECK.copy()
    random.shuffle(deck)
    
    # deal hole cards (2 cards for the player)
    hole_cards, deck = draw_cards(deck, 2)
    print(f"Your hole cards: {hole_cards}")
    
    community_cards = []
    
    # game loop through phases
    for phase in phases:
        print(f"\n--- {phase.upper()} ---")
        
        # deal community cards for this phase
        community_cards, deck = deal_community_cards(deck, phase, community_cards)
        
        if community_cards:
            print(f"Community cards: {community_cards}")
        
        # make decision using MCTS
        decision, win_probability = mcts(hole_cards, community_cards, deck)
        
        print(f"Win probability: {win_probability:.2f}")
        print(f"Decision: {decision}")
        
        # if decision is to fold, end the game
        if decision == "fold":
            print("You folded. Game over.")
            return
        
        # update the deck by removing the known cards for the next phase
        deck = [card for card in deck if card not in community_cards]
    
    print("\nGame complete! You stayed until the end.")
    print(f"Final win probability: {win_probability:.2f}")


def test_rollout():
    """Test function to debug the rollout and hand evaluation"""
    # create a test deck
    test_deck = DECK.copy()
    random.shuffle(test_deck)
    
    # create a test node with some hole cards
    hole_cards = [(14, 'S'), (14, 'D')] 
    print(f"My hole cards: {hole_cards}")
    
    # remove hole cards from deck
    test_deck = [card for card in test_deck if card not in hole_cards]
    
    # create some community cards
    community_cards = random.sample(DECK, 3)
    print(f"Community cards: {community_cards}")
    
    # remove community cards from deck
    test_deck = [card for card in test_deck if card not in community_cards]
    
    # create a test node
    test_node = Node(hole_cards, community_cards, test_deck)
    
    wins = 0
    ties = 0
    losses = 0
    for _ in range(1000):
        result = rollout(test_node)
        if result == 1:
            wins += 1
        elif result == 0.5:
            ties += 1
        else:
            losses += 1
    
    print(f"Rollout results:")
    print(f"Wins: {wins} ({wins/1000*100:.1f}%)")
    print(f"Ties: {ties} ({ties/1000*100:.1f}%)")
    print(f"Losses: {losses} ({losses/1000*100:.1f}%)")
    print(f"Win probability: {(wins + ties*0.5)/1000:.4f}")
    
    # Test a specific hand evaluation
    # my_hand, my_rank = evaluate_hand(hole_cards, community_cards)
    # print(f"My hand: {my_hand}, rank: {my_rank}")
    
    # Test opponent with worse hand
    # opp_cards = [(2, 'H'), (3, 'H')]
    # opp_hand, opp_rank = evaluate_hand(opp_cards, community_cards)
    # print(f"Opponent hand: {opp_hand}, rank: {opp_rank}")
    
    # Compare
    # print(f"My rank > Opponent rank: {my_rank > opp_rank}")

if __name__ == "__main__":
    # test_rollout()
    main()
