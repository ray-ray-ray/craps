"""
Test for the player object.
"""
__author__ = 'rcourtney'

import nose.tools
import player
import table
import unittest


def odds_payout(amount, bet_name, point=None):
    """
    Calculate the payout for a bet (not including the initial amount of the bet)

    :param amount: initial bet amount
    :param bet_name: e.g., pass, come, odds, etc.
    :param point: specify point when the bet requires it
    :return: payout amount
    """
    if point is None:
        return (amount * table.ODDS[bet_name][0]) / table.ODDS[bet_name][1]
    else:
        return ((amount * table.ODDS[bet_name][point][0]) /
                table.ODDS[bet_name][point][1])


class TestPlayer(unittest.TestCase):

    def test_player(self):
        me = player.Player()
        tbl = table.Table()

        #
        # Gotta have a betting strategy.
        #
        nose.tools.assert_raises(NotImplementedError, me.make_bets, tbl)

    def test_pass_player(self):
        me = player.PassPlayer(200)
        tbl = table.Table()
        me.make_bets(tbl)

        #
        # Only a pass bet.
        #
        nose.tools.assert_equal(len(tbl.bets['pass']), 1)
        bt = tbl.bets['pass'][0]
        nose.tools.assert_equal(bt.amount, tbl.minimum)
        nose.tools.assert_equal(bt.player, me)
        nose.tools.assert_equal(bt.table, tbl)

        #
        # Point set. Still only a pass bet.
        #
        tbl.dice_total = 5
        tbl.pay_bets()
        me.make_bets(tbl)
        nose.tools.assert_equal(len(tbl.bets['pass']), 1)
        nose.tools.assert_equal(bt, tbl.bets['pass'][0])

    def test_come_player(self):
        me = player.ComePlayer(200)
        tbl = table.Table()
        me.make_bets(tbl)

        #
        # No come bets
        #
        for point in tbl.bets['come'].iterkeys():
            nose.tools.assert_equal(len(tbl.bets['come'][point]), 0)

        tbl.dice_total = 8
        tbl.pay_bets()
        me.make_bets(tbl)

        #
        # Come out bet
        #
        bt = tbl.bets['come']['out'][0]
        nose.tools.assert_equal(bt.amount, tbl.minimum)
        nose.tools.assert_equal(bt.player, me)
        nose.tools.assert_equal(bt.table, tbl)

        #
        # Come points and come out bet
        #
        tbl.dice_total = 4
        tbl.pay_bets()
        me.make_bets(tbl)
        tbl.dice_total = 5
        tbl.pay_bets()
        me.make_bets(tbl)
        nose.tools.assert_equal(tbl.bets['come'][4][0], bt)
        nose.tools.assert_equal(len(tbl.bets['come']['out']), 1)
        nose.tools.assert_equal(len(tbl.bets['come'][5]), 1)

    def test_place_player(self):
        me = player.PlacePlayer(200)
        tbl = table.Table()

        #
        # Point off, no place bets
        #
        me.make_bets(tbl)
        nose.tools.assert_false(me.six)
        nose.tools.assert_false(me.eight)
        nose.tools.assert_false(me.point_on)
        for point in tbl.bets['place'].iterkeys():
            nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)

        #
        # Point on, place 6 and 8
        #
        tbl.dice_total = 4
        tbl.pay_bets()
        me.make_bets(tbl)
        nose.tools.assert_true(me.six)
        nose.tools.assert_true(me.eight)
        nose.tools.assert_true(me.point_on)
        for point in tbl.bets['place'].iterkeys():
            if point in (6, 8):
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)

        #
        # Win place 6
        #
        tbl.dice_total = 6
        tbl.pay_bets()
        for point in tbl.bets['place'].iterkeys():
            if point == 8:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)
        me.make_bets(tbl)
        nose.tools.assert_true(me.six)
        nose.tools.assert_true(me.eight)
        nose.tools.assert_true(me.point_on)
        for point in tbl.bets['place'].iterkeys():
            if point in (6, 8):
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)

        #
        # Point made
        #
        tbl.dice_total = 4
        tbl.pay_bets()
        me.make_bets(tbl)
        nose.tools.assert_true(me.six)
        nose.tools.assert_true(me.eight)
        nose.tools.assert_false(me.point_on)
        for point in tbl.bets['place'].iterkeys():
            if point in (6, 8):
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)

        #
        # Point 6
        #
        tbl.dice_total = 6
        tbl.pay_bets()
        for point in tbl.bets['place'].iterkeys():
            if point in (6, 8):
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)
        me.make_bets(tbl)
        nose.tools.assert_true(me.six)
        nose.tools.assert_true(me.eight)
        nose.tools.assert_true(me.point_on)
        for point in tbl.bets['place'].iterkeys():
            if point in (6, 8):
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)

        #
        # 7 lose
        #
        tbl.dice_total = 7
        tbl.pay_bets()
        for point in tbl.bets['place'].iterkeys():
            nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)
        me.make_bets(tbl)
        nose.tools.assert_false(me.six)
        nose.tools.assert_false(me.eight)
        nose.tools.assert_false(me.point_on)
        for point in tbl.bets['place'].iterkeys():
            nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)

        #
        # 11 no place bets
        #
        tbl.dice_total = 11
        tbl.pay_bets()
        for point in tbl.bets['place'].iterkeys():
            nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)
        me.make_bets(tbl)
        nose.tools.assert_false(me.six)
        nose.tools.assert_false(me.eight)
        nose.tools.assert_false(me.point_on)
        for point in tbl.bets['place'].iterkeys():
            nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)

        #
        # Not enough money for both bets
        #
        me.money = 18
        tbl.dice_total = 10
        tbl.pay_bets()
        me.make_bets(tbl)
        nose.tools.assert_true(me.six)
        nose.tools.assert_false(me.eight)
        nose.tools.assert_true(me.point_on)
        for point in tbl.bets['place'].iterkeys():
            if point == 6:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)

    def test_odds_player(self):
        me = player.OddsPlayer(money=200)
        tbl = table.Table()
        me.make_bets(tbl)
        nose.tools.assert_equal(me.money, 185)
        tbl.dice_total = 4
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 185)
        me.make_bets(tbl)
        nose.tools.assert_equal(me.money, 155)
        tbl.dice_total = 5
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 155)
        me.make_bets(tbl)
        nose.tools.assert_equal(me.money, 124)
        tbl.dice_total = 6
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 124)
        me.make_bets(tbl)
        nose.tools.assert_equal(me.money, 94)
        tbl.dice_total = 8
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 94)

        #
        # All the odds bets
        #
        for point in tbl.bets['odds'].iterkeys():
            if point in (4, 5, 6):
                nose.tools.assert_equal(len(tbl.bets['odds'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['odds'][point]), 0)

        #
        # Win all the bets.
        #
        tbl.dice_total = 6
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 157)
        tbl.dice_total = 5
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 227)
        tbl.dice_total = 4
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 302)
        for point in tbl.bets['odds'].iterkeys():
            nose.tools.assert_equal(len(tbl.bets['odds'][point]), 0)
