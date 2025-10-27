import pytest
from lib.solutions.CHK.checkout_solution import CheckoutSolution


class TestCheckout():
    def test_checkout_chk_r1(self):
        assert CheckoutSolution().checkout("") == 0
        assert CheckoutSolution().checkout("A") == 50
        assert CheckoutSolution().checkout("AA") == 100
        assert CheckoutSolution().checkout("AAA") == 130
        assert CheckoutSolution().checkout("B") == 30
        assert CheckoutSolution().checkout("BB") == 45
        assert CheckoutSolution().checkout("AB") == 80

    def test_checkout_chk_r1_bulk_discounts(self):
        assert CheckoutSolution().checkout("AAABB") == 175
        assert CheckoutSolution().checkout("ABB") == 95
        assert CheckoutSolution().checkout("AAAB") == 160
        assert CheckoutSolution().checkout("C") == 20
        assert CheckoutSolution().checkout("D") == 15
        assert CheckoutSolution().checkout("ABCD") == 115
        # Test for multiple special offers
    def test_checkout_chk_r1_multiple_bulk_discounts(self):
        assert CheckoutSolution().checkout("AAAA") == 180
        assert CheckoutSolution().checkout("AAAAA") == 200
        assert CheckoutSolution().checkout("AAAAAA") == 250
        assert CheckoutSolution().checkout("AAAAAAAA") == 330
        assert CheckoutSolution().checkout("AAAAAAAAA") == 380
        assert CheckoutSolution().checkout("BBBB") == 90
        assert CheckoutSolution().checkout("BBBBBB") == 135
        # Test for input with multiple cases

    def test_checkout_chk_r1_invalid_inputs(self):
        assert CheckoutSolution().checkout("Ab") == -1
        assert CheckoutSolution().checkout("AaaB") == -1
        assert CheckoutSolution().checkout("BBbBbB") == -1
        assert CheckoutSolution().checkout("aAAa") == -1
        assert CheckoutSolution().checkout("a1") == -1
        assert CheckoutSolution().checkout("1a") == -1
        

    def test_checkout_chk_r2(self):
        assert CheckoutSolution().checkout("E") == 40
        assert CheckoutSolution().checkout("EE") == 80
        assert CheckoutSolution().checkout("ABCDE") == 155

    def test_checkout_chk_r2_free_item(self):
        assert CheckoutSolution().checkout("EEB") == 80

    def test_checkout_chk_r2_offer_priority(self):
        # Price is less than with the b1g1 b free offer than the 2b for 45 offer
        assert CheckoutSolution().checkout("EEBB") == 125
        assert CheckoutSolution().checkout("EEEBB") == 165
        assert CheckoutSolution().checkout("EEEEBB") == 160
        assert CheckoutSolution().checkout("EEBAAAAA") == 280
        assert CheckoutSolution().checkout("EEBAAA") == 210
        


