import random

class Blackjack:
    def __init__(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
    
    def create_deck(self):
        deck = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                deck.append((suit, value))
        return deck
    
    def deal_card(self):
        return self.deck.pop()
    
    def deal_hands(self):
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]

    def hand_total(self, hand):
        total = 0
        aces = 0
        for card in hand:
            if card[1] == "J" or card[1] == "Q" or card[1] == "K":
                total += 10
            elif card[1] == "A":
                total += 11
                aces += 1
            else:
                total += int(card[1])
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total
    
    def after_hit_game_update(self):
        if self.hand_total(self.player_hand) > 21:
            return "bust"
        elif self.hand_total(self.player_hand) == 21:
            return "blackjack"
        else:
            return "continue"
        
    def player_turn(self, move):
        if move == "hit":
            self.player_hand.append(self.deal_card())
        return self.after_hit_game_update()

        
    def dealer_turn(self):
        while self.hand_total(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())
        return self.hand_total(self.dealer_hand)
    
    def game_result(self):
        self.dealer_turn()
        print(self.dealer_hand, self.hand_total(self.dealer_hand))
        player_value = self.hand_total(self.player_hand)
        dealer_value = self.hand_total(self.dealer_hand)
        if player_value > 21:
            return "L"
        elif player_value > dealer_value or dealer_value > 21:
            return "W"
        elif player_value == dealer_value:
            return "T"
        else:
            return "L"

game = Blackjack()
game.deal_hands()

def main():
    print("Dealer shows:", game.dealer_hand[:1])

    status = "continue"
    while status == "continue":
        print(game.player_hand, game.hand_total(game.player_hand))
        action = input("Enter an action (hit/stand): ")
        status = game.player_turn(action)
        
        if action == "stand":
            break


    print(game.game_result())

if __name__ == "__main__":
    main()
    