"""
The table object manages game flow, bets, and payouts.
"""
__author__ = 'rcourtney'

import random

CRAPS = (2, 3, 12)
WINNERS = (7, 11)
ODDS = {
    'pass': (1, 1),
    'come': (1, 1)
}


class Table(object):
    """
    Create a table object to play on.
    """
    die = range(1, 7)

    def __init__(self, minimum=15):
        """
        Create a craps table.

        :param minimum: amount of minimum bet
        :return: None
        """
        self.bets = {
            'pass': [],
            'come': {
                'out': [],
                4: [],
                5: [],
                6: [],
                8: [],
                9: [],
                10: []
            }
        }
        self.dice = (None, None)
        self.dice_total = None
        self.point = None
        self.minimum = minimum

    def shoot(self):
        """
        Roll the dice.

        :return: None
        """
        self.dice = (random.choice(self.die), random.choice(self.die))
        self.dice_total = sum(self.dice)

    def pass_check(self):
        """
        Check any pass bets against the current roll.

        :return: None
        """
        if self.point is None:
            if self.dice_total in CRAPS:
                #
                # No point. Craps. Lose on the pass line.
                #
                self.bets['pass'] = []
            elif self.dice_total in WINNERS:
                #
                # No point. Winners on the pass line.
                #
                for bet in self.bets['pass']:
                    bet.payout(ODDS['pass'])
                self.bets['pass'] = []
            else:
                #
                # Set the point.
                #
                self.point = self.dice_total
        else:
            if self.dice_total == 7:
                #
                # Lose on the pass line.
                #
                self.bets['pass'] = []
                self.point = None
            elif self.dice_total == self.point:
                #
                # Win on the pass line.
                #
                for bet in self.bets['pass']:
                    bet.payout(ODDS['pass'])
                self.point = None
                self.bets['pass'] = []

    def come_check(self):
        """
        Check any Come bets against the current roll
        :return:
        """
        if self.dice_total in CRAPS:
            #
            # Come out lose
            #
            self.bets['come']['out'] = []
        elif self.dice_total in WINNERS:
            #
            # Come out win.
            #
            for bet in self.bets['come']['out']:
                bet.payout(ODDS['come'])

            if self.dice_total == 7:
                #
                # Everyone else loses.
                #
                for point in self.bets['come'].iterkeys():
                    self.bets['come'][point] = []
            else:
                #
                # Clear the come out bets.
                #
                self.bets['come']['out'] = []
        else:
            #
            # Come point winners.
            #
            for bet in self.bets['come'][self.dice_total]:
                bet.payout(ODDS['come'])

            #
            # Set come out points.
            #
            self.bets['come'][self.dice_total] = []
            for bet in self.bets['come']['out']:
                self.bets['come'][self.dice_total].append(bet)
            self.bets['come']['out'] = []

    def pay_bets(self):
        """
        Update the table based on the recent roll and payout any winners.

        :return: None
        """
        self.pass_check()
        self.come_check()

    def pass_bet(self, bet):
        """
        Make a bet on the Pass line.

        :param bet: bet.Bet object
        :return: None
        """
        self.bets['pass'].append(bet)

    def come_bet(self, bet):
        """
        Make a Come bet.

        :param bet: bet.Bet
        :return: None
        """
        if self.point is None:
            raise NoPointSet
        self.bets['come']['out'].append(bet)


class NoPointSet(Exception):
    """
    Betting on something other than pass when there's no point set.
    """
    pass