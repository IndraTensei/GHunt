from typing import *
from pathlib import Path
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime
import base64

from autoslot import Slots

from gkia import globals as gb


class SmartObj(Slots):
    pass

class AndroidCreds(SmartObj):
    def __init__(self) -> None:
        self.master_token: str = ""
        self.authorization_tokens: Dict = {}

class gkiaCreds(SmartObj):
    """
        This object stores all the needed credentials that gkia uses,
        such as cookies, OSIDs, keys and tokens.
    """
    
    def __init__(self, creds_path: str = "") -> None:
        self.cookies: Dict[str, str] = {}
        self.osids: Dict[str, str] = {}
        self.android: AndroidCreds = AndroidCreds()

        if not creds_path:
            cwd_path = Path().home()
            gkia_folder = cwd_path / ".malfrats/gkia"
            if not gkia_folder.is_dir():
                gkia_folder.mkdir(parents=True, exist_ok=True)
            creds_path = gkia_folder / "creds.m"
        self.creds_path: str = creds_path

    def are_creds_loaded(self) -> bool:
        return all([self.cookies, self.osids, self.android.master_token])

    def load_creds(self, silent=False) -> None:
        """Loads cookies, OSIDs and tokens if they exist"""
        if Path(self.creds_path).is_file():
            try:
                with open(self.creds_path, "r", encoding="utf-8") as f:
                    raw = f.read()
                data = json.loads(base64.b64decode(raw).decode())

                self.cookies = data["cookies"]
                self.osids = data["osids"]

                self.android.master_token = data["android"]["master_token"]
                self.android.authorization_tokens = data["android"]["authorization_tokens"]

                if not silent:
                    gb.rc.print("[+] Authenticated !", style="sea_green3")
            except Exception:
                if not silent:
                    print("[-] Stored cookies are corrupted\n")
        else:
            if not silent:
                print("[-] No stored cookies found\n")

    def save_creds(self, silent=False):
        """Save cookies, OSIDs and tokens to the specified file."""
        data = {
            "cookies": self.cookies,
            "osids": self.osids,
            "android": {
                "master_token": self.android.master_token,
                "authorization_tokens": self.android.authorization_tokens
            }
        }

        with open(self.creds_path, "w", encoding="utf-8") as f:
            f.write(base64.b64encode(json.dumps(data, indent=2).encode()).decode())

        if not silent:
            print(f"\n[+] Creds have been saved in {self.creds_path} !")

### Maps

class Position(SmartObj):
    def __init__(self):
        self.latitude: float = 0.0
        self.longitude: float = 0.0

class MapsGuidedAnswer(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.question: str = ""
        self.answer: str = ""

class MapsLocation(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.address: str = ""
        self.position: Position = Position()
        self.tags: List[str] = []
        self.types: List[str] = []
        self.cost: int = 0 # 1-4

class MapsReview(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.comment: str = ""
        self.rating: int = 0
        self.location: MapsLocation = MapsLocation()
        self.guided_answers: List[MapsGuidedAnswer] = []
        self.approximative_date: relativedelta = None

class MapsPhoto(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.url: str = ""
        self.location: MapsLocation = MapsLocation()
        self.approximative_date: relativedelta = None
        self.exact_date: datetime = None

### Drive
class DriveExtractedUser(SmartObj):
    def __init__(self):
        self.gaia_id: str = ""
        self.name: str = ""
        self.email_address: str = ""
        self.role: str = ""
        self.is_last_modifying_user: bool = False