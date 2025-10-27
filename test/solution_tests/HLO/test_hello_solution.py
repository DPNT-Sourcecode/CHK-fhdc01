import pytest
from lib.solutions.HLO.hello_solution import HelloSolution


class TestHello():
    def test_hello(self):
        assert HelloSolution().hello("Stuart") == "Hello, Stuart!"
        assert HelloSolution().hello("Dave") == "Hello, Dave!"

