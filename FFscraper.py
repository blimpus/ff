import json
import requests
import csv
from datetime import datetime, timedelta

#https://fantasyfootballanalytics.net/2016/06/ffanalytics-r-package-fantasy-football-data-analysis.html

accepted_positions = {'rb', 'qb', 'flex', 'te', 'k', 'dst'}
def switch(position):
    position = position.lower()
    if position not in accepted_positions:
        print("entered value does not match a valid position. Valid postions are rb, qb, te, k, dst, flex")
        exit(1)
    return "https://www.fantasypros.com/nfl/rankings/"+position+".php"

#todo: add params to filter yes no to comparing players then take x amount of players to show and filter all the rest
#add more stats and also look for potentially more urls
# Get today's date in ddmmyyyy format
today_date = datetime.now().strftime('%m%d%Y')
option = input("do you want ros (rest of season) or next week rankings (answer ros or nw) "  )
# URL of the website to scrape
if option == "ros":
    url = "https://www.fantasypros.com/nfl/rankings/ros-overall.php"
if option == "nw":
    position = input("pick the position you want to report on "  )
    url = switch(position)
else:
    print("you did it wrong (╯°□°)╯︵ ┻━┻")
    exit(1)

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
