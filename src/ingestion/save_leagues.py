import json
from pathlib import Path

# Import the API client from the same package. Using a relative import ensures
# this module can be executed with ``python -m`` without requiring the project
# root to be on ``PYTHONPATH``.
from .api_sports_client import APISportsClient


def save_leagues_for_season(season: int, country: str = None):
    """Fetch leagues for a season (and optional country) and persist them."""
    client = APISportsClient()
    leagues = client.get_leagues(season=season, country=country)

    raw_dir = Path.cwd() / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    filename = raw_dir / f"leagues_{season}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(leagues, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(leagues)} leagues to {filename}")


if __name__ == "__main__":
    # This guard will fire when the module is executed directly.
    save_leagues_for_season(2024)
