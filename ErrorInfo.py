import enum
from builtins import Exception


class InfoErrorType(enum.Enum):
    SCRAPPING_ERROR=0
    BRAWLIFY_CONNECTION_FAILED=1
    MISSING_TIER=2
class InfoError(Exception):
    def __init__(self,infoType:InfoErrorType,**kwargs):
        super().__init__()
        self.infoType = infoType
        if infoType is InfoErrorType.SCRAPPING_ERROR:
            self.message = "Couldn't scrap response from brawlify. Did you entered ID correctly?"
        elif infoType is InfoErrorType.BRAWLIFY_CONNECTION_FAILED:
            self.message = "Couldn't connect brawlify. Check internet connection."
