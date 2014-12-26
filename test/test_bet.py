"""
Test the bet object
"""
__author__ = 'rcourtney'

import bet
import nose.tools
import player
import table
import unittest


class TestBet(unittest.TestCase):

    def test_bet(self):
        #
        # Check money problems
        #
        me = player.Player(money=10)
        tbl = table.Table(minimum=10)
        nose.tools.assert_raises(bet.NotEnoughMoney, bet.Bet, 15, me, tbl)
        nose.tools.assert_raises(bet.MinimumBetRequired, bet.Bet, 5, me, tbl)

        bt = bet.Bet(10, me, tbl)
        nose.tools.assert_equal(me.money, 0)