import os
import requests
from dotenv import load_dotenv

load_dotenv()

class APISportsClient:
    BASE_URL = "https://v3.football.api-sports.io"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("API_SPORTS_KEY")
        if not self.api_key:
            raise ValueError("API_SPORTS_KEY not set in env")
        self.headers = {"x-apisports-key": self.api_key}

    def _get(self, path: str, params: dict = None):
        url = f"{self.BASE_URL}{path}"
        resp = requests.get(url, headers=self.headers, params=params, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError(f"API call failed [{resp.status_code}]: {resp.text}")
        return resp.json()
    
    def get_status(self):
        return self._get("/status")

    def get_countries(self):
        """Fetch available countries."""
        return self._get("/countries")

    def get_seasons(self):
        """Fetch all unique seasons across all leagues."""
        resp = self._get("/leagues")
        seasons = set()
        for entry in resp.get("response", []):
            for s in entry.get("seasons", []):
                year = s.get("year")
                try:
                    seasons.add(int(year))
                except (TypeError, ValueError):
                    continue 
        return sorted(seasons)

    def get_leagues(self, season: int = None, country: str = None):
        """
        Fetch Football leagues from v3, then filter by season and/or country.
        Returns a list of league dicts.
        """
        resp = self._get("/leagues")               # no params here
        leagues = []

        for entry in resp.get("response", []):
            # Country filter
            if country and entry.get("country", {}).get("code") != country:
                continue

            # Season filter: Football uses "season" in each season dict
            if season is not None:
                # entry["seasons"] is a list of dicts like {"season":2024,...}
                if not any(s.get("year") == season for s in entry.get("seasons", [])):
                    continue

            # Unwrap the league object
            leagues.append(entry["league"])

        return leagues
    
    