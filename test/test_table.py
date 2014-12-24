"""
Tests for the table object.
"""
__author__ = 'rcourtney'

import bet
import nose.tools
import player
import table
import unittest

class TestTable(unittest.TestCase):
    def test_point(self):
        tbl = table.Table()

        #
        # Craps
        #
        tbl.dice = (1, 2)
        tbl.pay_bets()
        nose.tools.assert_is_none(tbl.point)

        #
        # Winners
        #
        tbl.dice = (5, 6)
        tbl.pay_bets()
        nose.tools.assert_is_none(tbl.point)

        #
        # Point
        #
        tbl.dice = (4, 4)
        tbl.pay_bets()
        nose.tools.assert_equal(tbl.point, 8)

        #
        # 7 out
        #
        tbl.dice = (3, 4)
        tbl.pay_bets()
        nose.tools.assert_is_none(tbl.point)

        #
        # Point Winner
        #
        tbl.dice = (2, 4)
        tbl.pay_bets()
        tbl.dice = (6, 6)
        tbl.pay_bets()
        nose.tools.assert_equal(tbl.point, 6)
        tbl.dice = (3, 3)
        tbl.pay_bets()
        nose.tools.assert_is_none(tbl.point)

    def test_pass(self):
        #
        # Make pass bet.
        #
        me = player.Player(money=100)
        tbl = table.Table()
        tbl.pass_bet(bet.Bet(15, me, tbl))
        nose.tools.assert_equal(me.money, 85)

        #
        # Win the pass bet.
        #
        tbl.dice = (4, 4)
        tbl.pay_bets()
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 115)
