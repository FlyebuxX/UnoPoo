# ======================================================================================================================
# === CLASS
# ======================================================================================================================


class CardManager:
    """
    Class which manages a move
    """

    def __init__(self, card: tuple, game):
        self.card = card
        self.type = card[0]
        self.value = card[1]
        self.game = game

    def manage_card(self) -> None:
        """
        Method that analyzes the card to call the adapted method
        """
        if self.type == '+2' or self.type == '+4':
            self.plus_value(int(self.type[-1]))
        elif self.type == 'skip':
            self.skip_turn()
        elif self.type == 'change_color':
            NEW_COLOR = input("Choose a new color : green - yellow - red - blue")
            self.change_color(NEW_COLOR)
        elif self.type == 'reverse':
            self.reverse_game()
        else:
            self.add_card_basic()

    def update_current_index(self, nb: int) -> None:

        self.game.current_index -= len(self.game.players)
        self.game.current_index += nb

        if self.game.current_index < - len(self.game.players):  # if the index is invalid
            self.game.current_index = self.game.current_index % len(self.game.players)

    def update_current_card(self) -> None:
        self.game.current_card = self.card

    def update_player(self) -> None:
        self.game.decks[self.game.pseudos[self.game.current_index]].remove(self.card)

    def plus_value(self, value: int) -> None:

        # action for the player
        self.update_player()

        # action on the board
        for i in range(value):  # value is 2 or 4
            card_to_add = self.game.pick.pop(0)  # adding a new card to the next player
            if self.game.current_index + 1 == len(self.game.players):  # if it is about the last player
                self.game.players[0].deck.append(card_to_add)
            else:
                self.game.decks[self.game.pseudos[self.game.current_index + 1]].append(card_to_add)

        if value == 4:  # if it is about a +4 card
            new_color = input("Choose a new color : green - yellow - red - blue")
            self.type, self.value = new_color, new_color
            self.card = (self.type, self.value)

        # each case
        self.update_current_index(1)
        self.update_current_card()

    def skip_turn(self) -> None:

        # action for the player
        self.update_player()

        # each case
        self.update_current_card()

    def change_color(self, new_color: str) -> None:

        # action for the player
        self.update_player()

        # action on the board
        self.type, self.value = new_color, new_color
        self.card = (self.type, self.value)

        # each case
        self.update_current_index(1)
        self.update_current_card()

    def reverse_game(self) -> None:

        # action for the player
        self.update_player()

        # action on the board
        self.game.players.reverse()

        # each case
        self.update_current_card()

    def add_card_basic(self) -> None:

        # action for the player
        self.update_player()

        # each case
        self.update_current_index(1)
        self.update_current_card()
