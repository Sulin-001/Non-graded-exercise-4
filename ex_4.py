import random
import time

# Define the attributes for the cards
Name_list = ["Diablo", "Medusa", "Jester", "Troll", "Specter", "Mist", "Savage", "Marauder", "Wimp", "Sorcerer"]
Health_list = [100, 100, 120, 150, 100, 100, 100, 100, 110, 100]
Attack_list = [90, 70, 60, 40, 70, 75, 90, 85, 40, 70]
Defense_list = [60, 70, 90, 94, 70, 65, 50, 50, 85, 55]

# Zipping the lists into card_deck
card_deck = list(zip(Name_list, Health_list, Attack_list, Defense_list))

# Shuffle the deck
random.shuffle(card_deck)

# Split the deck between player and opponent
deck_size = 5
player_deck = card_deck[:deck_size]
opponent_deck = card_deck[deck_size:deck_size*2]

# Initialize game state variables
selected_player_card_index = None
player_deck_size = deck_size
opponent_deck_size = deck_size
game_over = False

def display_card(card):
    if card is None:
        return "Empty"
    name, health, attack, defense = card
    return f"{name}: Health: {health}, Attack: {attack}, Defense: {defense}"

def attack_card(attacker, defender):
    if attacker is None or defender is None:
        return defender

    defender_name, defender_health, defender_attack, defender_defense = defender
    attacker_name, attacker_health, attacker_attack, attacker_defense = attacker

    if defender_defense > 0:
        if defender_defense >= attacker_attack:
            defender_defense -= attacker_attack
        else:
            remaining_attack = attacker_attack - defender_defense
            defender_defense = 0
            defender_health -= remaining_attack
    else:
        defender_health -= attacker_attack

    return defender_name, defender_health, defender_attack, defender_defense

def print_decks():
    print("\nYour deck:")
    for i, card in enumerate(player_deck):
        print(f"{i+1}. {display_card(card)}")
    print("\nOpponent's deck:")
    for i, card in enumerate(opponent_deck):
        print(f"{i+1}. {display_card(card)}")

def select_player_card():
    global selected_player_card_index
    while selected_player_card_index is None:
        try:
            print("\nSelect a card to attack (1-5): ")
            selected_player_card_index = int(input()) - 1
            if selected_player_card_index < 0 or selected_player_card_index >= len(player_deck) or player_deck[selected_player_card_index] is None:
                print("Invalid selection or card already defeated. Try again.")
                selected_player_card_index = None
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

def select_opponent_card():
    global selected_player_card_index
    while selected_player_card_index is not None:
        try:
            print("\nSelect an opponent card to attack (1-5): ")
            opponent_card_index = int(input()) - 1
            if opponent_card_index < 0 or opponent_card_index >= len(opponent_deck) or opponent_deck[opponent_card_index] is None:
                print("Invalid selection or card already defeated. Try again.")
            else:
                player_card = player_deck[selected_player_card_index]
                opponent_card = opponent_deck[opponent_card_index]
                updated_opponent_card = attack_card(player_card, opponent_card)
                opponent_deck[opponent_card_index] = updated_opponent_card

                if updated_opponent_card[1] <= 0:
                    print(f"\nYou defeated {updated_opponent_card[0]}!")
                    opponent_deck[opponent_card_index] = None
                else:
                    print(f"\nAfter your attack: {display_card(updated_opponent_card)}")

                selected_player_card_index = None
                check_game_over()
                if not game_over:
                    opponent_attack()
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

def opponent_attack():
    global player_deck, opponent_deck
    if not player_deck or not opponent_deck:
        return

    opponent_card = random.choice([card for card in opponent_deck if card is not None])
    player_card = random.choice([card for card in player_deck if card is not None])

    updated_player_card = attack_card(opponent_card, player_card)
    player_deck[player_deck.index(player_card)] = updated_player_card

    if updated_player_card[1] <= 0:
        print(f"\nOpponent defeated your {updated_player_card[0]}!")
        player_deck[player_deck.index(updated_player_card)] = None

    print(f"\nAfter opponent's attack: {display_card(updated_player_card)}")
    check_game_over()

def check_game_over():
    global game_over

    player_defeated = sum(1 for card in player_deck if card is None)
    opponent_defeated = sum(1 for card in opponent_deck if card is None)

    if player_defeated >= player_deck_size:
        if not game_over:  
            print("You lost all your cards! Game Over!")
            game_over = True
        return True
    elif opponent_defeated >= opponent_deck_size:
        if not game_over:  
            print("You defeated all opponent cards! Victory!")
            game_over = True
        return True
    return False

# Game loop
while not game_over:
    print_decks()
    select_player_card()
    select_opponent_card()

