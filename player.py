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


class ComePlayer(PassPlayer):
    """
    This player always bets the Pass line and Come.
    """
    def make_bets(self, table):
        """
        Bet Come once a point is set.

        :param table: table.Table
        :return: None
        """
        super(ComePlayer, self).make_bets(table)
        if table.point is not None:
            table.come_bet(bet.Bet(table.minimum, self, table))