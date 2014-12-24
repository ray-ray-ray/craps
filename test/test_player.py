"""
Test for the player object.
"""
__author__ = 'rcourtney'

import nose.tools
import player
import table
import unittest


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
        tbl.dice = (3, 2)
        tbl.pay_bets()
        me.make_bets(tbl)
        nose.tools.assert_equal(len(tbl.bets['pass']), 1)
        nose.tools.assert_equal(bt, tbl.bets['pass'][0])