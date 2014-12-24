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
        me = player.PassPlayer(money=ANTE)
        roll_count = 0

        #
        # Main play loop
        #
        while (roll_count < ROLLS) and (me.money >= tbl.minimum):
            me.make_bets(tbl)
            tbl.shoot()
            roll_count += 1
            tbl.pay_bets()

        results.append([roll_count, me.money, me.money/ANTE])

    print tabulate.tabulate(results, headers='firstrow')
