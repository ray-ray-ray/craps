"""
Player object to hold the money and betting strategy.
"""
__author__ = 'rcourtney'

import bet
import table


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

    def make_bets(self, tbl):
        """
        Implement the betting strategy in this method.

        :param tbl: table.Table
        :return: None
        """
        raise NotImplementedError


class PassPlayer(Player):
    """
    This player only bets the pass line.
    """
    def make_bets(self, tbl):
        """
        Bet Pass line only.

        :param tbl: table.Table
        :return: None
        """
        if tbl.point is None:
            tbl.pass_bet(bet.Bet(tbl.minimum, self, tbl))


class ComePlayer(PassPlayer):
    """
    This player always bets the Pass line and Come.
    """
    def make_bets(self, tbl):
        """
        Bet Come once a point is set.

        :param tbl: table.Table
        :return: None
        """
        super(ComePlayer, self).make_bets(tbl)
        if tbl.point is not None:
            tbl.come_bet(bet.Bet(tbl.minimum, self, tbl))


class PlacePlayer(Player):
    """
    This player only makes place 6 and 8 bets.
    """
    def __init__(self, *args, **kwargs):
        super(PlacePlayer, self).__init__(*args, **kwargs)
        self.six = False
        self.eight = False
        self.point_on = False

    def make_bets(self, tbl):
        """
        Make 6 and 8 place bets when they don't exist and when the point is on.

        :param tbl: table.Table
        :return: None
        """
        #
        # Minimum place bet based on the 6 odds
        #
        place_amount = tbl.minimum + table.ODDS['place'][6][1] - (
            tbl.minimum % table.ODDS['place'][6][1])

        #
        # If the point was on for the last roll, update the state of the bets.
        #
        if self.point_on:
            if tbl.dice_total == 6:
                self.six = False
            elif tbl.dice_total == 8:
                self.eight = False
            elif tbl.dice_total == 7:
                self.six = False
                self.eight = False

        #
        # No bets when the point is off.
        #
        if tbl.point is None:
            self.point_on = False
        else:
            #
            # When the point is on, make sure you have 6 and 8 bets.
            #
            self.point_on = True
            if not self.six and (self.money >= place_amount):
                tbl.place_bet(6, bet.Bet(place_amount, self, tbl))
                self.six = True
            if not self.eight and (self.money >= place_amount):
                tbl.place_bet(8, bet.Bet(place_amount, self, tbl))
                self.eight = True