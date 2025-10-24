
class SumSolution:

    def compute(self, number_one: int, number_two: int) -> int:
        if not isinstance(number_one, int) or not isinstance(number_two, int) \
            or not (0 <= number_one <= 100) or not (0 <= number_two <= 100):
            raise ValueError("Both inputs must be integers between 0 and 100.")
        return number_one + number_two
