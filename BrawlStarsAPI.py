import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup
from bs4 import Tag
from ErrorInfo import InfoErrorType, InfoError


class API:
    def __init__(self, Id: str = ""):
        if Id != "":
            self.brawlers = self._gather_brawlers(Id)
        self.trophy_ranges = [
            TrophyLeagueTier(500, 500, 0),
            TrophyLeagueTier(524, 500, 20),
            TrophyLeagueTier(549, 524, 50),
            TrophyLeagueTier(574, 549, 70),
            TrophyLeagueTier(599, 574, 80),
            TrophyLeagueTier(624, 599, 90),
            TrophyLeagueTier(649, 624, 100),
            TrophyLeagueTier(674, 649, 110),
            TrophyLeagueTier(699, 674, 120),
            TrophyLeagueTier(724, 699, 130),
            TrophyLeagueTier(749, 724, 140),
            TrophyLeagueTier(774, 749, 150),
        ]

    def _gather_brawlers(self, ID: str):
        brawlers_list = list()
        request = requests.request("GET", f"https://brawlify.com/stats/profile/{ID}")
        if request.status_code != 200:
            raise InfoError(InfoErrorType.BRAWLIFY_CONNECTION_FAILED)
        try:
            response = BeautifulSoup(str(request.content), features="html.parser")
            brawlers = response.find_all("div", {"class": "row"})[7].find_all(
                "a", recursive=False
            )
            for brawler in brawlers:
                tag: Tag = brawler
                name = tag.attrs["data-name"]
                trophies = tag.find(
                    "div", {"class": "text-hp brl-btm-l pr-1"}
                ).contents[1]
                brawlers_list.append(Brawler(name, int(trophies)))
            return brawlers_list
        except:
            raise InfoError(InfoErrorType.SCRAPPING_ERROR)
    @property
    def total_trophies(self):
        total = 0
        for brawler in self.brawlers:
            total += brawler.trophies
        return total
    def get_trophy_legaue_affected(self):
        filtered_brawlers = list()
        for brawler in self.brawlers:
            if brawler.trophies >= 500:
                filtered_brawlers.append(brawler)
        return filtered_brawlers

    def get_trophy_range(self, trophies: int):
        for range in self.trophy_ranges:
            if trophies <= range.trophies_max:
                return range
        return None


@dataclass
class Brawler:
    name: str
    trophies: int


@dataclass
class TrophyLeagueTier:
    trophies_max: int
    trophies_decay: int
    star_points: int
