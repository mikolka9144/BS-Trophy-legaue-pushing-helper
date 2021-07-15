from enum import Enum
from dataclasses import dataclass
from BrawlStarsAPI import API, Brawler, TrophyLeagueTier
from ErrorInfo import InfoErrorType,InfoError
BSWIN_REWARD = 8


class BrawlStarsCalculator:
    def __init__(self, BSAPI: API):
        self.API = BSAPI

    def _trophy_loss_sort(self, brawler_report):
        return brawler_report.trophy_loss

    def _Get_status(self, trophy_tier: TrophyLeagueTier, brawler: Brawler):
        if trophy_tier.star_points == 0:
            return Brawler_Status.OUT_OF_LEAGUE
        elif trophy_tier.trophies_max - brawler.trophies <= BSWIN_REWARD:
            return Brawler_Status.I_WIN_AWAY
        elif trophy_tier.trophies_max - brawler.trophies <= BSWIN_REWARD * 2:
            return Brawler_Status.II_WINS_AWAY
        else:
            return Brawler_Status.STABLE

    def Get_brawlers_starpoints_rewards_report(self):
        report = BrawlersStarpointsReport()
        for brawler in self.API.get_trophy_legaue_affected():
            trophy_range = self.API.get_trophy_range(brawler.trophies)
            if trophy_range is None:
                raise InfoError(InfoErrorType.MISSING_TIER,trophies=brawler.trophies)
            report.brawlers_reports.append(
                BrawlerReport(
                    brawler,
                    trophy_range.star_points,
                    brawler.trophies - trophy_range.trophies_decay,
                    self._Get_status(trophy_range, brawler),
                )
            )
        report.brawlers_reports.sort(key=self._trophy_loss_sort, reverse=True)
        return report


class BrawlersStarpointsReport:
    def __init__(self):
        self.brawlers_reports = list()

    @property
    def trophy_loss_total(self):
        trophy_loss = 0
        for brawler in self.brawlers_reports:
            trophy_loss += brawler.trophy_loss
        return trophy_loss

    @property
    def starpoints_total(self):
        starpoints = 0
        for brawler in self.brawlers_reports:
            starpoints += brawler.starpoints_reward
        return starpoints


class Brawler_Status(Enum):
    STABLE = 0
    I_WIN_AWAY = 1
    II_WINS_AWAY = 2
    OUT_OF_LEAGUE = 3


@dataclass
class BrawlerReport:
    brawler: Brawler
    starpoints_reward: int
    trophy_loss: int
    status: Brawler_Status
