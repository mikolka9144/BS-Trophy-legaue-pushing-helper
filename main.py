from BrawlStarsAPI import API
from MainLogic import BrawlStarsCalculator, Brawler_Status
from ErrorInfo import InfoError
import sys


class Main_CLI:
    def generate_report(self, report):
        if len(report.brawlers_reports) == 0:
            print(
                "Looks like none of your brawlers qualifyes for trophy league."
                " Get some above 500 trophies and try again."
            )
        for brawler in report.brawlers_reports:
            self.generate_brawler_message(brawler)
        print(
            f"Total: -{report.trophy_loss_total} trophies and +{report.starpoints_total} starpoints"
        )

    def generate_brawler_message(self, brawler):
        print(f"{brawler.brawler.name} ", end="")
        if brawler.status == Brawler_Status.OUT_OF_LEAGUE:
            print(f"got out of league. Win 1 game to get it back to league.")
        else:
            print(
                f"will lose {brawler.trophy_loss} trophies "
                f"and get {brawler.starpoints_reward} starpoints.",
                end="",
            )

            if brawler.status == Brawler_Status.I_WIN_AWAY:
                print(" Win 1 game to progress to next tier.")
            elif brawler.status == Brawler_Status.II_WINS_AWAY:
                print(" Win 2 games to progress to next tier.")
            else:
                print()  # to print /n character


def Get_ID():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        return input("Enter your ID: ")
def format_ID(id:str):
    return id.upper()

if __name__ == "__main__":
    try:
        cli = Main_CLI()
        id = format_ID(Get_ID())
        print("Gathering data")
        api = API(id)

        print("calculating")
        logic = BrawlStarsCalculator(api)
        brawlers = logic.Get_brawlers_starpoints_rewards_report()

        cli.generate_report(brawlers)
    except InfoError:
        value = sys.exc_info()[1]
        print(value.message)
