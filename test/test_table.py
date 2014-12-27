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
        tbl.dice_total = 3
        tbl.pay_bets()
        nose.tools.assert_is_none(tbl.point)

        #
        # Winners
        #
        tbl.dice_total = 11
        tbl.pay_bets()
        nose.tools.assert_is_none(tbl.point)

        #
        # Point
        #
        tbl.dice_total = 8
        tbl.pay_bets()
        nose.tools.assert_equal(tbl.point, 8)

        #
        # 7 out
        #
        tbl.dice_total = 7
        tbl.pay_bets()
        nose.tools.assert_is_none(tbl.point)

        #
        # Point Winner
        #
        tbl.dice_total = 6
        tbl.pay_bets()
        tbl.dice_total = 12
        tbl.pay_bets()
        nose.tools.assert_equal(tbl.point, 6)
        tbl.dice_total = 6
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
        tbl.dice_total = 8
        tbl.pay_bets()
        tbl.pay_bets()
        nose.tools.assert_equal(me.money, 115)

    def test_come(self):
        #
        # Can't come if no point
        #
        me = player.Player(money=100)
        tbl = table.Table()
        nose.tools.assert_raises(
            table.NoPointSet,
            tbl.come_bet,
            bet.Bet(15, me, tbl))
        #
        # Give my money back from the incorrect bet.
        #
        me.money += 15

        #
        # Test come craps
        #
        tbl.point = 8
        tbl.come_bet(bet.Bet(tbl.minimum, me, tbl))
        nose.tools.assert_equal(len(tbl.bets['come']['out']), 1)
        tbl.dice_total = 12
        tbl.pay_bets()
        nose.tools.assert_equal(len(tbl.bets['come']['out']), 0)
        nose.tools.assert_equal(me.money, 100 - tbl.minimum)

        #
        # Test come out winners
        #
        tbl.come_bet(bet.Bet(tbl.minimum, me, tbl))
        tbl.dice_total = 11
        tbl.pay_bets()
        nose.tools.assert_equal(len(tbl.bets['come']['out']), 0)
        nose.tools.assert_equal(me.money, 100)

        #
        # Test come point
        #
        tbl.come_bet(bet.Bet(tbl.minimum, me, tbl))
        tbl.dice_total = 6
        tbl.pay_bets()
        nose.tools.assert_equal(len(tbl.bets['come']['out']), 0)
        nose.tools.assert_equal(len(tbl.bets['come'][6]), 1)

        #
        # Test come point winner
        #
        tbl.pay_bets()
        nose.tools.assert_equal(len(tbl.bets['come'][6]), 0)
        nose.tools.assert_equal(me.money, 100 + tbl.minimum)

        #
        # Test come point loser
        #
        tbl.come_bet(bet.Bet(tbl.minimum, me, tbl))
        tbl.pay_bets()
        tbl.dice_total = 7
        tbl.pay_bets()
        for point in tbl.bets['come']:
            nose.tools.assert_equal(len(tbl.bets['come'][point]), 0)
        nose.tools.assert_equal(me.money, 100)

    def test_place(self):
        #
        # Can't place if no point
        #
        me = player.Player(money=100)
        tbl = table.Table()
        bt = bet.Bet(tbl.minimum, me, tbl)
        nose.tools.assert_raises(table.NoPointSet, tbl.place_bet, 8, bt)

        #
        # Can't place if not an odds multiple
        #
        tbl.point = 4
        nose.tools.assert_raises(table.FractionalOdds, tbl.place_bet, 8, bt)

        #
        # Give back bad bet money
        #
        me.money = 100

        #
        # Test loser
        #
        place_amount = tbl.minimum + (
            table.ODDS['place'][8][1] - (
                tbl.minimum % table.ODDS['place'][8][1]))
        bt = bet.Bet(place_amount, me, tbl)
        tbl.point = 4
        tbl.place_bet(8, bt)
        for point in tbl.bets['place']:
            if point == 8:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 1)
            else:
                nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)
        nose.tools.assert_equal(tbl.bets['place'][8][0], bt)
        tbl.dice_total = 7
        tbl.pay_bets()
        for point in tbl.bets['place']:
            nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)
        nose.tools.assert_equal(me.money, 100 - place_amount)

        #
        # Test winner
        #
        tbl.point = 4
        tbl.place_bet(8, bet.Bet(place_amount, me, tbl))
        tbl.dice_total = 8
        tbl.pay_bets()
        nose.tools.assert_equal(tbl.point, 4)
        for point in tbl.bets['place']:
            nose.tools.assert_equal(len(tbl.bets['place'][point]), 0)
        nose.tools.assert_equal(
            me.money,
            100 - place_amount + (
                place_amount * table.ODDS['place'][8][0] /
                table.ODDS['place'][8][1]))

        #
        # Test place bet off when point off
        #
        tbl.point = 4
        tbl.place_bet(8, bet.Bet(place_amount, me, tbl))
        tbl.dice_total = 4
        tbl.pay_bets()
        nose.tools.assert_equal(len(tbl.bets['place'][8]), 1)
        tbl.dice_total = 7
        tbl.pay_bets()
        nose.tools.assert_equal(len(tbl.bets['place'][8]), 1)
        tbl.dice_total = 8
        tbl.pay_bets()
        nose.tools.assert_equal(len(tbl.bets['place'][8]), 1)
