from blackjack import Blackjack
import numpy as np

class QLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((33, 12, 2, 2)) #player_sum, dealer_card, usable_ace, action

    def choose_action(self, player_sum, dealer_card, usable_ace):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(["hit", "stand"])
        else:
            return "hit" if self.q_table[player_sum, dealer_card, usable_ace, 0] > self.q_table[player_sum, dealer_card, usable_ace, 1] else "stand"
        
    def update_table(self, player_sum, dealer_card, usable_ace, action, reward, new_player_sum, new_dealer_card, new_usable_ace):
        if action == "hit":
            action_idx = 0
        else:
            action_idx = 1
        self.q_table[player_sum, dealer_card, usable_ace, action_idx] += self.alpha * (reward + self.gamma * np.max(self.q_table[new_player_sum, new_dealer_card, new_usable_ace]) - self.q_table[player_sum, dealer_card, usable_ace, action_idx])

    @staticmethod
    def has_usable_ace(hand):
        value, ace = 0, False
        for card in hand:
            card_number = card[1]
            value += min(10, int(card_number) if card_number not in ['J', 'Q', 'K', 'A'] else 11)
            ace |= (card_number == 'A')
        return int(ace and value + 10 <= 21)
    
    def train(self, episodes):
        one_percent = round(episodes / 100)

        for ep in range(episodes):
            game = Blackjack()
            game.deal_hands()

            if ep % one_percent == 0:
                progress = (ep/episodes) * 100
                print(f"Training progress: {progress:.2f}%")

            
            dealer_card = int(game.dealer_hand[0][1]) if game.dealer_hand[0][1] not in ['J', 'Q', 'K', 'A'] else (10 if game.dealer_hand[0][1] != 'A' else 11)
            status = "continue"

            while status == "continue":
                player_sum = game.hand_total(game.player_hand)
                usable_ace = self.has_usable_ace(game.player_hand)
                action = self.choose_action(player_sum, dealer_card, usable_ace)
                status = game.player_turn(action)
                new_player_sum = game.hand_total(game.player_hand)
                new_usable_ace = self.has_usable_ace(game.player_hand)

                reward = 0  # Intermediate reward, only final matters

                if status == "blackjack":
                    reward = 1
                elif status == "bust":
                    reward = -1

                if reward != 0:
                    self.update_table(player_sum, dealer_card, usable_ace, action, reward, new_player_sum, dealer_card, new_usable_ace)

                if action == "stand":
                    break

            final_result = game.game_result()
            final_reward = 1 if final_result == "W" else (-1 if final_result == "L" else 0)
            self.update_table(player_sum, dealer_card, usable_ace, action, final_reward, new_player_sum, dealer_card, new_usable_ace)

    def play(self):
        game = Blackjack()
        game.deal_hands()

        print("Dealer shows:", game.dealer_hand[:1])

        status = "continue"
        print(game.player_hand, game.hand_total(game.player_hand))
        while status == "continue":
            player_sum = game.hand_total(game.player_hand)
            usable_ace = self.has_usable_ace(game.player_hand)
            dealer_card = int(game.dealer_hand[0][1]) if game.dealer_hand[0][1] not in ['J', 'Q', 'K', 'A'] else (10 if game.dealer_hand[0][1] != 'A' else 11)
            action = "hit" if self.q_table[player_sum, dealer_card, usable_ace, 0] > self.q_table[player_sum, dealer_card, usable_ace, 1] else "stand"
            status = game.player_turn(action)
            
            if action == "stand":
                break
                
            print(game.player_hand, game.hand_total(game.player_hand))
        

        if status == "continue":
            print("Dealer has:", game.dealer_hand, game.hand_total(game.dealer_hand))
            game.dealer_turn()

        final_result = game.game_result()
        return final_result


# Train the agent
agent = QLearning()
agent.train(5000000)

test_games = 1000000
wins = 0
losses = 0
draws = 0

for _ in range(test_games):
    print("-----")
    result = agent.play()
    print(result)
    if result == "W":
        wins += 1
    elif result == "L":
        losses += 1
    else:
        draws += 1

print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
print(f"Win rate: {wins/(wins + losses)*100:.2f}%")

