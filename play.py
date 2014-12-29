"""
Interactive CLI
"""
__author__ = 'rcourtney'

import bet
import player
import table


def make_bet(plr, tb):
    """
    Prompt player for a bet type, amount, and point if necessary.
    :param plr: player.Player
    :param tb: table.Table
    :return: None
    """
    print '(p)ass, (c)ome, (pl)ace, (o)dds'
    bet_type = raw_input('--> ')
    print 'Enter amount.'
    amount = int(raw_input('--> '))
    bt = bet.Bet(amount, plr, tb)
    if bet_type == 'p':
        tb.pass_bet(bt)
    elif bet_type == 'c':
        tb.come_bet(bt)
    else:
        print 'Enter point.'
        point = int(raw_input('--> '))
        if bet_type == 'pl':
            tb.place_bet(point, bt)
        elif bet_type == 'o':
            tb.odds_bet(point, bt)


def print_bets(tb):
    """
    Display the current bets.

    :param tb: table.Table
    :return: None
    """
    print 'pass: [%s]' % ', '.join(map(str, tb.bets['pass']))
    print 'come: {out: [%s], 4: [%s], 5: [%s], 6: [%s], 8: [%s], 9: [%s], 10: [%s]' % (
        ', '.join(map(str, tb.bets['come']['out'])),
        ', '.join(map(str, tb.bets['come'][4])),
        ', '.join(map(str, tb.bets['come'][5])),
        ', '.join(map(str, tb.bets['come'][6])),
        ', '.join(map(str, tb.bets['come'][8])),
        ', '.join(map(str, tb.bets['come'][9])),
        ', '.join(map(str, tb.bets['come'][10]))
    )
    print 'odds: {4: [%s], 5: [%s], 6: [%s], 8: [%s], 9: [%s], 10: [%s]' % (
        ', '.join(map(str, tb.bets['odds'][4])),
        ', '.join(map(str, tb.bets['odds'][5])),
        ', '.join(map(str, tb.bets['odds'][6])),
        ', '.join(map(str, tb.bets['odds'][8])),
        ', '.join(map(str, tb.bets['odds'][9])),
        ', '.join(map(str, tb.bets['odds'][10]))
    )
    print 'place: {4: [%s], 5: [%s], 6: [%s], 8: [%s], 9: [%s], 10: [%s]' % (
        ', '.join(map(str, tb.bets['place'][4])),
        ', '.join(map(str, tb.bets['place'][5])),
        ', '.join(map(str, tb.bets['place'][6])),
        ', '.join(map(str, tb.bets['place'][8])),
        ', '.join(map(str, tb.bets['place'][9])),
        ', '.join(map(str, tb.bets['place'][10]))
    )

if __name__ == '__main__':
    print 'Enter starting money.'
    money = int(raw_input('--> '))
    me = player.Player(money=money)
    print 'Enter table minimum.'
    minimum = int(raw_input('--> '))
    tbl = table.Table(minimum=minimum)
    rolls = 0
    done = False

    while not done:
        if tbl.point is None:
            print 'Point: OFF'
        else:
            print 'Point: %s' % tbl.point
        print_bets(tbl)
        print 'Money: %s' % me.money
        print '(b)et, (s)hoot, (q)uit'
        action = raw_input('--> ')
        if action == 'b':
            make_bet(me, tbl)
        elif action == 's':
            tbl.shoot()
            rolls += 1
            print 'Dice: %s %s' % tbl.dice
            tbl.pay_bets()
        elif action == 'q':
            done = True

    print 'Rolls: %s' % rolls
    print 'Money: %s' % me.money
    print 'Return: %s' % (float(me.money) / money)