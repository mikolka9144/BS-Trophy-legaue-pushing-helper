import unittest
import sys
import BrawlStarsAPI
from ErrorInfo import InfoErrorType,InfoError
from BrawlStarsAPI import API

api = API()


class BrawlStarsTests(unittest.TestCase):
    def test_getting_trophy_ranges(self):
        self.check_trophy_range(520, 20)
        self.check_trophy_range(599, 80)
        self.check_trophy_range(550, 70)
        self.check_trophy_range(500, 0)

    def check_trophy_range(self, trophies: int, starpoints: int):
        real_range = api.get_trophy_range(trophies)
        assert real_range.star_points == starpoints
if __name__ == "__main__":
    unittest.main()
