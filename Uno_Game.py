# ======================================================================================================================
# === IMPORTS
# ======================================================================================================================


import random
from Player import Player
from Card_Manager import CardManager
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
        self.pick = []
        self.decks = {}
        self.current_card = ()
        self.trash = []
        self.current_index = 0
        self.rotation = 1  # if positive, direction of the hands of the clock

    @staticmethod
    def no_winner() -> bool:
        """
        Test whether a player has won or not
        :return: bool
        """
        return 0 in [len(value) for value in game.decks.values()]

    @staticmethod
    def get_players_pseudos() -> list:
        players = []
        for i in range(int(nb_player)):
            player_name = input("Player " + str(i + 1) + " type your pseudo :")
            players.append(player_name)
        return players

    def init_pick(self) -> None:

        pick_to_add = []
        colors = ['red', 'green', 'yellow', 'blue']

        for color in colors:
            for card_color in range(2):  # 2 items from card 1 to card 9
                for number in range(1, 10):
                    pick_to_add.append((number, color))
                pick_to_add.append(('+2', color))  # adding a +2 card into the pick
                pick_to_add.append(('reverse', color))  # adding a reverse card
                pick_to_add.append(('skip', color))  # adding a skip card
            pick_to_add.append((0, color))  # only one card 0

        for extra_card in range(4):
            pick_to_add.append(('change_color', '_'))
            pick_to_add.append(('+4', '_'))

        random.shuffle(pick_to_add)  # shuffling
        self.pick = pick_to_add

    def corresponding_play_move(self, card: tuple) -> bool:
        """
        Test whether the card can be played or not
        """
        if card[0] == self.current_card[len(self.current_card) - 1][0] \
                or card[1] == self.current_card[len(self.current_card) - 1][1] \
                or len(card) == 1:
            return True
        return False

    def is_playable(self, move: int) -> bool:
        """
        Method that checks whether the player has got any card to play or not
        :param move:
        :return:
        """
        for item in self.decks[self.players[move].pseudo]:
            if self.corresponding_play_move(item):
                return True
        return False

    def create_profiles(self, pseudos_players: list) -> None:
        """
        Method that creates a profile for each player
        """
        for i in range(self.nb_players):
            player = Player(pseudos_players[i])
            self.players.append(player)

    def cards_distribution(self) -> None:
        for player in self.players:
            for i in range(7):  # each player has got 7 cards
                random_index = random.randint(1, len(self.pick))  # choice of a random card among the pick
                player.deck.append(self.pick.pop(random_index))
            self.decks[player.pseudo] = player.deck  # adding the deck of the player in a global decks list

        # first card of the game
        self.current_card = self.pick.pop(random.randint(0, len(self.pick)))

    def player_move(self, player_index: int):
        card_to_play = False
        while not card_to_play:
            card_index = input("Which card do you want to play ? (enter its index, first card is index 1)")
            if int(card_index) <= len(self.players[player_index].deck) \
                    and self.corresponding_play_move(self.players[player_index].deck[card_index]):
                card_to_play = True
            else:
                print("Invalid card")

            card = self.decks[player_index][card_index]
            card_move = CardManager(card, player_index)
            card_move.manage_card()

    def game(self) -> None:
        while not self.no_winner():
            print("{}, it is your turn to play".format(self.players[self.current_index].pseudo))
            print("-----------------------------------------------------------------")
            print("Current card : {}".format(self.current_card))
            print("Here is your deck : \n {}".format(self.players[self.current_index].deck))
            print("-----------------------------------------------------------------")
            if self.is_playable(self.current_index):
                self.player_move(self.current_index)


# ======================================================================================================================
# === MAIN
# ======================================================================================================================

invalid_nb = True
while invalid_nb:
    nb_player = input("How many players are you :")
    if nb_player.isdigit() and int(nb_player) > 1:
        invalid_nb = False
    else:
        print("Invalid number of players")

game = Game(int(nb_player))
pseudos = game.get_players_pseudos()
game.create_profiles(pseudos)
game.init_pick()
game.cards_distribution()
game.game()
