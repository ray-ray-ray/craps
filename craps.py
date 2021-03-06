"""
Simulate craps strategies.
"""
__author__ = 'rcourtney'

import player
import table
import tabulate

ROLLS = 1000
ANTE = 200.0
SIMULATIONS = 10

if __name__ == '__main__':
    results = [['Rolls', 'Money', 'Return']]
    for i in xrange(SIMULATIONS):
        tbl = table.Table()
        me = player.OddsPlayer(money=ANTE)
        #print "money: %s" % me.money
        roll_count = 0

        #
        # Main play loop
        #
        while tbl.bets_exist() or (
                    (roll_count < ROLLS) and (me.money >= tbl.minimum)):
            if roll_count < ROLLS:
                me.make_bets(tbl)
            #print tbl.bets
            tbl.shoot()
            #print tbl.dice
            roll_count += 1
            tbl.pay_bets()
            #print "money: %s" % me.money

        results.append([roll_count, me.money, me.money/ANTE])

    print tabulate.tabulate(results, headers='firstrow')
