"""
The table object manages game flow, bets, and payouts.
"""
__author__ = 'rcourtney'

import random

CRAPS = (2, 3, 12)
WINNERS = (7, 11)


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
            'pass': []
        }
        self.dice = (None, None)
        self.point = None
        self.minimum = minimum

    def shoot(self):
        """
        Roll the dice.

        :return: None
        """
        self.dice = (random.choice(self.die), random.choice(self.die))

    def pay_bets(self):
        """
        Update the table based on the recent roll and payout any winners.

        :return: None
        """
        dice_total = sum(self.dice)
        if self.point is None:
            if dice_total in CRAPS:
                #
                # No point. Craps. Lose on the pass line.
                #
                self.bets['pass'] = []
            elif dice_total in WINNERS:
                #
                # No point. Winners on the pass line.
                #
                for bet in self.bets['pass']:
                    self.pass_win(bet)
                self.bets['pass'] = []
            else:
                #
                # Set the point.
                #
                self.point = dice_total
        else:
            if dice_total == 7:
                #
                # Lose on the pass line.
                #
                self.bets['pass'] = []
                self.point = None
            elif dice_total == self.point:
                #
                # Win on the pass line.
                #
                for bet in self.bets['pass']:
                    self.pass_win(bet)
                self.point = None
                self.bets['pass'] = []

    def pass_bet(self, bet):
        """
        Make a bet on the Pass line.

        :param bet: bet.Bet object
        :return: None
        """
        self.bets['pass'].append(bet)

    def pass_win(self, bet):
        """
        Payout a bet on the pass line.

        :param bet: bet.Bet object
        :return: None
        """
        bet.player.money += (2 * bet.amount)