# ======================================================================================================================
# === IMPORTS
# ======================================================================================================================


from Uno_Game import Game
# ======================================================================================================================
# === CLASS
# ======================================================================================================================


class CardManager(Game):
    """
    Class which manages a move
    """

    def __init__(self, card: tuple, player_index: int):
        self.type = card[0]
        self.value = card[1]
        self.card = card
        self.player_index = player_index

    def manage_card(self) -> None:
        """
        Method that analyze the card to call the adapted method
        """
        if self.type == '+2' or self.type == '+4':
            self.plus_value(self.value)
        elif self.type == 'skip':
            self.skip_turn()
        elif self.type == 'change_color':
            self.change_color(self.value)
        elif self.type == 'reverse':
            self.reverse()
        else:
            self.add_card_basic()

    def update_current_index(self) -> None:
        self.current_index -= len(self.players) + 1

    def plus_value(self, value: int) -> None:

        # action for the player
        self.players[self.player_index].deck.remove(self.card)

        # action on the board
        for i in range(value):  # value is 2 or 4
            card_to_add = self.pick.pop(0)  # adding a new card to the next player
            if self.current_index + 1 == len(self.players):  # if it is about the last player
                self.players[0].deck.append(card_to_add)
            else:
                self.players[self.current_index + 1].deck.append(card_to_add)

        # each case
        self.update_current_index()

    def skip_turn(self) -> None:
        pass

    def change_color(self,  new_color: str) -> None:
        pass

    def reverse(self) -> None:
        pass

    def add_card_basic(self) -> None:
        pass
