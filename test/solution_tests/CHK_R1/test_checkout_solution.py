import pytest
from solutions.CHK.checkout_solution import CheckoutSolution


class TestCheckout():
    def test_hello(self):
        assert CheckoutSolution().checkout("A") == 50
