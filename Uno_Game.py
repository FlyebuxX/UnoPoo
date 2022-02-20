# ======================================================================================================================
# === IMPORTS
# ======================================================================================================================


import random
from CardManager import CardManager
from Player import Player
# ======================================================================================================================
# === CLASS
# ======================================================================================================================


class Game:
    """
    Class which defines a new game
    """

    def __init__(self, nb_players: int) -> None:
        self.nb_players = nb_players
        self.players = []
        self.pseudos = []
        self.pick = []
        self.decks = {}
        self.current_card = ()
        self.current_index = 0

    @staticmethod
    def no_winner() -> bool:
        """
        Test whether a player has won or not
        :return: bool
        """
        return 0 in [len(value) for value in game.decks.values()]

    def get_players_pseudos(self):
        self.pseudos = [input("Player " + str(i + 1) + " type your pseudo :") for i in range(self.nb_players)]

    def init_pick(self) -> None:

        game_pick = []
        colors = ['red', 'green', 'yellow', 'blue']

        for color in colors:
            for card_color in range(2):  # 2 occurrences from card 1 to card 9
                for number in range(1, 10):
                    game_pick.append((number, color))
                game_pick.append(('+2', color))  # adding a +2 card into the pick
                game_pick.append(('reverse', color))  # adding a reverse card
                game_pick.append(('skip', color))  # adding a skip card
            game_pick.append((0, color))  # only one card 0 for each color

        for extra_card in range(4):
            game_pick.append(('change_color', '_'))
            game_pick.append(('+4', '_'))

        random.shuffle(game_pick)  # shuffling
        self.pick = game_pick

    def corresponding_play_move(self, card: tuple) -> bool:
        """
        Test whether the card can be played or not
        """

        # if same value / same color / +4 or change_color card
        if card[0] == self.current_card[0] or card[1] == self.current_card[1] or card[1] == "_":
            return True
        return False

    def is_playable(self) -> bool:
        """
        Method that checks whether the player has got at least one card to play
        :return:
        """
        for item in self.decks[self.pseudos[self.current_index]]:
            if self.corresponding_play_move(item) \
                    or len([value for value in self.decks[self.pseudos[self.current_index]] if value[1] == "_"]) > 0:
                return True
        return False

    def create_profiles(self) -> None:
        """
        Method that creates a profile for each player
        """
        for i in range(self.nb_players):
            new_player = Player(self.pseudos[i])
            self.players.append(new_player)

    def cards_distribution(self) -> None:
        for player in self.players:
            for i in range(7):  # each player has got 7 cards
                player.deck.append(self.pick.pop(0))
            self.decks[player.pseudo] = player.deck  # adding the deck of the player in a global decks list

        # first card of the game
        self.current_card = self.pick.pop(random.randint(0, len(self.pick) - 1))

    def player_move(self) -> None:
        valid_card = False
        card = ()
        while not valid_card:
            print("Cards which can be played:")
            for card in self.decks[self.pseudos[self.current_index]]:
                if self.corresponding_play_move(card):
                    print(self.decks[self.pseudos[self.current_index]].index(card), "- ", card)
            card_index = input("Which card do you want to play ? (enter its index, first card is inde)x 0)")
            if int(card_index) <= len(self.decks[self.pseudos[self.current_index]]) - 1 \
                    and self.corresponding_play_move(self.decks[self.pseudos[self.current_index]][int(card_index)]):
                valid_card = True
                card = self.decks[self.pseudos[self.current_index]][int(card_index)]
            else:
                print("Invalid card")

        card_move = CardManager(card, self)
        card_move.manage_card()

    def launcher(self) -> None:
        while not self.no_winner():
            print("\n\n\n", self.pseudos[self.current_index], ", it is your turn to play")
            print("-----------------------------------------------------------------")
            print("\nCurrent card :", self.current_card)
            print("\nHere is your deck : \n", self.decks[self.pseudos[self.current_index]])
            print("-----------------------------------------------------------------\n\n\n")
            if self.is_playable():
                self.player_move()
            else:
                print(self.decks[self.pseudos[self.current_index]], 'you don\'t have any card to play: +1 card')
                new_card = self.pick.pop(0)
                self.decks[self.pseudos[self.current_index]].append(new_card)

                self.current_index -= len(game.players)
                self.current_index += 1

                if self.current_index < - len(self.players):  # if the index is invalid
                    self.current_index = self.current_index % len(self.players)

        winner = [key for key, values in game.decks.items() if len(values) == 0][0]
        print('\nCongratulations, ', winner, ', you\'ve just won the game !')


# ======================================================================================================================
# === MAIN
# ======================================================================================================================


try:
    game = Game(int(input('How many players are you ?')))
    game.get_players_pseudos()
    game.create_profiles()
    game.init_pick()
    game.cards_distribution()
    game.launcher()

except ValueError:
    print('Invalid value for the number of players.')
