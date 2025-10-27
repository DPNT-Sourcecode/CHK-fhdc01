import pytest
from solutions.SUM.sum_solution import SumSolution


class TestSum():
    def test_sum(self):
        assert SumSolution().compute(1, 2) == 3
        assert SumSolution().compute(10, 30) == 40
        assert SumSolution().compute(1, 99) == 100
        assert SumSolution().compute(0, 0) == 0
        assert pytest.raises(ValueError, SumSolution().compute, -1, 1)
        assert pytest.raises(ValueError, SumSolution().compute, 0, 101)
        assert pytest.raises(ValueError, SumSolution().compute, 5, -6)
        assert pytest.raises(ValueError, SumSolution().compute, 5, -4)



