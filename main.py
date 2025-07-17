from src.ingestion.api_sports_client import APISportsClient
client = APISportsClient()

# Find the Champions League entry
cl_entry = next(
    e for e in client._get("/leagues")["response"]
    if e["league"]["id"] == 2
)

# Print all valid years
years = sorted(s.get("year") for s in cl_entry["seasons"] if s.get("year"))
print("Valid Champions League seasons:", years)
