"""
Bets
"""
__author__ = 'rcourtney'


class Bet(object):
    """
    Track bets
    """
    def __init__(self, amount, player, table):
        """
        Create a bet.

        :param amount: amount of money
        :param player: player.Player
        :param table: table.Table
        :return: None
        """
        #
        # Verify the money and take it from the player.
        #
        if amount > player.money:
            raise NotEnoughMoney
        if amount < table.minimum:
            raise MinimumBetRequired
        self.amount = amount
        player.money -= amount

        self.player = player
        self.table = table


class NotEnoughMoney(Exception):
    """
    Can't bet more than you have
    """
    pass


class MinimumBetRequired(Exception):
    """
    Gotta bet the table minimum
    """
    pass