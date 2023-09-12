import json
import requests
import csv
from datetime import datetime, timedelta


#todo: add params to filter yes no to comparing players then take x amount of players to show and filter all the rest
#add more stats and also look for potentially more urls
# Get today's date in ddmmyyyy format
today_date = datetime.now().strftime('%m%d%Y')

# URL of the website to scrape
url = "https://www.fantasypros.com/nfl/rankings/ros-overall.php"

# Make a GET request to the API
response = requests.get(url)

# Find the Rank JSON data within the HTML page
start_index = response.text.find("var ecrData = ") + len("var ecrData = ")
end_index = response.text.find("};", start_index) + 1
json_data = response.text[start_index:end_index]

# Parse the JSON data
data = json.loads(json_data)

# Extract id, name, position, and rank from the JSON and write to an empty list
raw_data = []
for player_data in data.get('players', []):
    player_id = player_data.get('player_id')
    name = player_data.get('player_name')
    position = player_data.get('player_position_id')
    rank = player_data.get('rank_ecr')
    if not player_id:
        continue
    raw_data.append([player_id, name, position, rank])

# Create a CSV file, write columns, and write raw data to CSV
fileName = f"ranks_{today_date}.csv"
with open(fileName, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Player ID", "Player Name", "Position", "Rank"])
    csv_writer.writerows(raw_data)

print(f"{fileName} Created Successfully")