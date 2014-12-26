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