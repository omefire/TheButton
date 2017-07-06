import unittest
from ethereum import tester as t
from ethereum import utils as u
#from ethereum.state import State as new_state
from ethereum.state import State
#import ethereum.new_state


# Amount in Wei everyone pressing the button should pay
MIN_AMOUNT_REQUIRED = 100

class TheButton(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TheButton, self).__init__(*args, **kwargs)

    def setUp(self):
        self.state = t.state()
        self.contract = self.state.abi_contract("TheButton.se")

    def test_once_game_is_over_stop_people_from_playing(self):

        result = self.contract.process(MIN_AMOUNT_REQUIRED, value = 200, sender = t.k0)
        self.assertNotEquals(result, -50)

        # Simulate the game ending
        self.contract.endGame()

        result = self.contract.process(MIN_AMOUNT_REQUIRED, value = 340, sender = t.k0)
        self.assertEquals(result, -50)


    def test_if_enough_time_passed_since_last_play_then_grant_earnings_to_last_player(self):

        # Player 1 presses the button
        result = self.contract.process(MIN_AMOUNT_REQUIRED, value = 140, sender = t.k0)
        self.assertEquals(result, 1)

        self.state.mine(1)

        winningBalanceBefore = State().get_balance(u.int_to_addr(t.k1))
        losingBalanceBefore = State().get_balance(u.int_to_addr(t.k0))

        # Player 2 presses the button
        result = self.contract.process(MIN_AMOUNT_REQUIRED, value=140, sender=t.k1)
        self.assertEquals(result, 1)

        self.state.mine(3)

        # Player 2 presses the button again
        result = self.contract.process(MIN_AMOUNT_REQUIRED, value=140, sender=t.k1)
        self.assertEquals(result, 2)

        winningBalanceAfter = State().get_balance(u.int_to_addr(t.k1))
        losingBalanceAfter = State().get_balance(u.int_to_addr(t.k0))

        self.assertEquals(losingBalanceAfter, losingBalanceBefore)
        self.assertTrue(winningBalanceAfter > losingBalanceBefore)



    def test_make_sure_each_player_sends_enough_ether_to_participate(self):
        result = self.contract.process(MIN_AMOUNT_REQUIRED, value=50, sender=t.k0)
        self.assertEquals(result, -49)

    def test_each_player_can_only_play_once(self):
        result = self.contract.process(MIN_AMOUNT_REQUIRED, value=140, sender=t.k0)
        self.assertEquals(result, 1)

        result = self.contract.process(MIN_AMOUNT_REQUIRED, value=140, sender=t.k0)
        self.assertEquals(result, -48)

def main():
    unittest.main()

if __name__ == '__main__':
    main()