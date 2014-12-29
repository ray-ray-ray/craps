"""
The table object manages game flow, bets, and payouts.
"""
__author__ = 'rcourtney'

import random

CRAPS = (2, 3, 12)
WINNERS = (7, 11)
ODDS = {
    'pass': (1, 1),
    'come': (1, 1),
    'place': {
        4: (9, 5),
        5: (7, 5),
        6: (7, 6),
        8: (7, 6),
        9: (7, 5),
        10: (9, 5)
    },
    'odds': {
        4: (2, 1),
        5: (3, 2),
        6: (6, 5),
        8: (6, 5),
        9: (3, 2),
        10: (2, 1)
    }
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
            },
            'place': {
                4: [],
                5: [],
                6: [],
                8: [],
                9: [],
                10: []
            },
            'odds': {
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

    def bets_exist(self):
        """
        Are there any bets currently on the table?

        :return: true/false
        """
        for bet in self.bets.iterkeys():
            if isinstance(self.bets[bet], dict):
                for point in self.bets[bet].iterkeys():
                    if len(self.bets[bet][point]) > 0:
                        return True
            elif len(self.bets[bet]) > 0:
                return True
        return False

    def shoot(self):
        """
        Roll the dice.

        :return: None
        """
        self.dice = (random.choice(self.die), random.choice(self.die))
        self.dice_total = sum(self.dice)

    def payout(self, bet_type, point=None):
        """
        Pay winning bets.

        :param bet_type: come, pass, place, etc.
        :param point: out or the number
        :return: None
        """
        if point is None:
            bets = self.bets[bet_type]
            odds = ODDS[bet_type]
        else:
            bets = self.bets[bet_type][point]

            #
            # Come bet has a point, but even odds.
            #
            if bet_type == 'come':
                odds = ODDS[bet_type]
            else:
                odds = ODDS[bet_type][point]

        [bets.pop().payout(odds) for _ in xrange(len(bets))]

    def clear_bets(self, bet_type, point=None):
        """
        Remove losing bets.

        :param bet_type: come, place, pass, etc.
        :param point: out or the number
        :return: None
        """
        if point is None:
            if isinstance(self.bets[bet_type], dict):
                for pnt in self.bets[bet_type].iterkeys():
                    self.bets[bet_type][pnt] = []
            else:
                self.bets[bet_type] = []
        else:
            self.bets[bet_type][point] = []

    def pass_check(self):
        """
        Check any pass and odds bets against the current roll.

        :return: None
        """
        if self.point is None:
            if self.dice_total in CRAPS:
                #
                # No point. Craps. Lose on the pass line.
                #
                self.clear_bets('pass')
            elif self.dice_total in WINNERS:
                #
                # No point. Winners on the pass line.
                #
                self.payout('pass')
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
                self.clear_bets('pass')
                self.clear_bets('odds')
                self.point = None
            elif self.dice_total == self.point:
                #
                # Win on the pass line.
                #
                self.payout('pass')
                self.payout('odds', self.point)
                self.point = None

    def come_check(self):
        """
        Check any Come and associated odds bets against the current roll
        :return:
        """
        if self.dice_total in CRAPS:
            #
            # Come out lose
            #
            self.clear_bets('come', point='out')
        elif self.dice_total in WINNERS:
            #
            # Come out win.
            #
            self.payout('come', point='out')

            if self.dice_total == 7:
                #
                # Everyone else loses.
                #
                self.clear_bets('come')
                self.clear_bets('odds')
        else:
            #
            # Come point winners.
            #
            self.payout('come', point=self.dice_total)

            #
            # Odds point winners
            #
            self.payout('odds', point=self.dice_total)

            #
            # Set come out points.
            #
            for bet in self.bets['come']['out']:
                self.bets['come'][self.dice_total].append(bet)
            self.clear_bets('come', point='out')

    def place_check(self):
        """
        Check any place bets when a point is already set.

        :return: None
        """
        if self.point is not None:
            #
            # 7 loses
            #
            if self.dice_total == 7:
                self.clear_bets('place')
            #
            # Payout winners
            #
            elif self.dice_total not in CRAPS + WINNERS:
                self.payout('place', point=self.dice_total)

    def pay_bets(self):
        """
        Update the table based on the recent roll and payout any winners.

        :return: None
        """
        #
        # Have to check place bets before pass so that the point isn't cleared.
        #
        self.place_check()
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
            raise PointNotSet
        self.bets['come']['out'].append(bet)

    def odds_bet(self, point, bet):
        """
        Make an odds bet on an existing Pass or Come bet.

        :param point: the existing Pass or Come point
        :param bet: bet.Bet
        :return: None
        """
        if point in CRAPS + WINNERS:
            raise InvalidPoint
        if (point != self.point) and (len(self.bets['come'][point]) == 0):
            raise PointNotSet
        if bet.amount % ODDS['odds'][point][1] != 0:
            raise FractionalOdds

        self.bets['odds'][point].append(bet)

    def place_bet(self, point, bet):
        """
        Make a place bet.

        :param point: which number to place
        :param bet: bet.Bet
        :return: None
        """
        if self.point is None:
            raise PointNotSet
        if point in CRAPS + WINNERS:
            raise InvalidPoint
        if bet.amount % ODDS['place'][point][1] != 0:
            raise FractionalOdds

        self.bets['place'][point].append(bet)


class PointNotSet(Exception):
    """
    Betting on something other than pass when there's no point set.
    """
    pass


class InvalidPoint(Exception):
    """
    Betting on a number that's not a valid point.
    """
    pass


class FractionalOdds(Exception):
    """
    Place bet needs to be an odds multiple
    """
    pass