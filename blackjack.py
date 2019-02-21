import random

card_names = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
suites = ['Clubs', 'Hearts', 'Spades', 'Diamonds']
average_card = sum([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10]) / 13


class Hand:
    def __init__(self):
        self.number_of_cards = 0
        self.drawn_cards = []
        self.total = 0

    def score(self, draw):
        self.drawn_cards.append('{} of {}'.format(card_names[draw['card']], suites[draw['suite']]))
        self.number_of_cards += 1
        s = draw['card'] + 1
        if s == 1:
            if self.total > 11:
                s = 1
            else:
                s = 10
        elif s > 10:
            s = 10
        self.total += s
        return self.total

    def show_cards(self, dealer=False):
        if dealer:
            return ", ".join(self.drawn_cards[1:])
        return ", ".join(self.drawn_cards)


class Deck:
    def __init__(self, deck_size=100, reshuffle_limit=1000):
        self.deck_size = deck_size
        self.reshuffle_limit = reshuffle_limit
        self.cards = [deck_size for i in range(13 * 4)]
        self.draw_count = 0

    def shuffle(self):
        self.cards = [self.deck_size for i in range(13 * 4)]

    def draw(self):
        if self.reshuffle_limit < self.draw_count:
            self.shuffle()

        self.draw_count += 1
        available_cards = [i for i, j in enumerate(self.cards) if j > 0]
        random_draw = random.randint(0, len(available_cards) - 1)
        self.cards[available_cards[random_draw]] -= 1
        suite = available_cards[random_draw] // 13
        card = available_cards[random_draw] % 13
        return {'suite': suite, 'card': card}


class BlackJack:
    def __init__(self, number_of_players=1, deck_size=100, reshuffle_limit=1000):
        self.number_of_players = number_of_players
        self.deck = Deck(deck_size=deck_size, reshuffle_limit=reshuffle_limit)
        self.turn = self.number_of_players - 1
        self.dealer_turn = False
        self.players = []
        self.dealer = None
        self.start_round()

    def start_round(self):
        if self.turn == self.number_of_players - 1:
            self.dealer = Hand()
            self.players = [Hand() for i in range(self.number_of_players)]
            for i in (1, 2):
                self.dealer.score(self.deck.draw())
                for player_hand in self.players:
                    player_hand.score(self.deck.draw())

            self.turn = 0
            self.dealer_turn = False
        else:
            self.dealer = Hand()
            self.dealer.score(self.deck.draw())
            self.dealer.score(self.deck.draw())
            self.turn += 1
            self.dealer_turn = False

    def present_table(self):
        print("-----------------")
        print("Dealer has a hidden card and: {}".format(self.dealer.show_cards(dealer=True)))
        for i, player_hand in enumerate(self.players):
            if i < game.turn:
                print("Player {}'s turn has ended".format(i + 1))
            else:
                print("Player {} has a score of {} with:\n{}"
                      .format(i + 1, player_hand.total, player_hand.show_cards()))
        print("-----------------")


user_input = number_of_players = ''
game = False
while True:
    if game is False:
        message = """Welcome to blackjack! 
Please type in number of players to start or type exit at anytime to stop
"""
        user_input = input(message)
        try:
            number_of_players = int(user_input)
        except Exception as exc:
            print("Could not start game with {} number of players".format(number_of_players))
            continue
        if number_of_players < 1:
            print("Could not start game less than 1 player")
        game = BlackJack(number_of_players=number_of_players, deck_size=100, reshuffle_limit=1000)
        continue

    if user_input == 'exit':
        break

    if game is not False:
        if game.dealer_turn:
            print("It is the dealer's turn")

            c = 0
            while game.dealer.total + average_card < 21:
                c += 1
                game.dealer.score(game.deck.draw())

            print("Dealer drew {} card(s) to get total score {}:\n{}"
                  .format(c, game.dealer.total, game.dealer.show_cards()))
            if game.dealer.total == 21:
                print("Player {} has lost!".format(game.turn + 1))
                game.start_round()
            elif game.dealer.total > 21:
                print("Player {} has won!".format(game.turn + 1))
                game.start_round()
            elif game.dealer.total > game.players[game.turn].total:
                print("Player {} has lost!".format(game.turn + 1))
                game.start_round()
            else:
                print("Player {} has won!".format(game.turn + 1))
                game.start_round()
        else:
            if game.players[game.turn].total == 21:
                print("Player {} has won!".format(game.turn + 1))
                game.start_round()
            elif game.players[game.turn].total > 21:
                print("Player {} has lost!".format(game.turn + 1))
                game.start_round()

            game.present_table()
            print("It is player {}'s turn".format(game.turn + 1))
            message = "Please type in call for a new card or check to continue\n"
            user_input = input(message)
            if user_input == 'check':
                game.dealer_turn = True
            elif user_input == 'call':
                game.players[game.turn].score(game.deck.draw())
                print("Player {} drew one card to get total score {}:\n{}"
                      .format(game.turn + 1, game.players[game.turn].total, game.players[game.turn].show_cards()))
