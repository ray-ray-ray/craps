"""
Player object to hold the money and betting strategy.
"""
__author__ = 'rcourtney'

import bet


class Player(object):
    """
    Player tracks money and has a betting strategy.
    """
    def __init__(self, money=0):
        """
        Create a player

        :param money: starting amount of money
        :return: None
        """
        super(Player, self).__init__()
        self.money = money

    def make_bets(self, table):
        """
        Implement the betting strategy in this method.

        :param table: table.Table
        :return: None
        """
        raise NotImplementedError


class PassPlayer(Player):
    """
    This player only bets the pass line.
    """
    def make_bets(self, table):
        """
        Bet Pass line only.

        :param table: table.Table
        :return: None
        """
        if table.point is None:
            table.pass_bet(bet.Bet(table.minimum, self, table))