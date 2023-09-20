import json
import os.path

import requests
import csv
from datetime import datetime, timedelta

from ff.comparison import helper
from ff.UI import layouts as views
from ff.trade_value import TradeValues as tv
from player import Player

#https://fantasyfootballanalytics.net/2016/06/ffanalytics-r-package-fantasy-football-data-analysis.html

nfl_start = datetime(2023,9,7)

i = 0
compare = 'no'
position = 'booglie boo'
while True:
    event, values = views.window.read()

    if event == "ROS":
        option = "ros"
        views.window.close()
        position, position_values = views.position_window.read()
        position = position.lower()
        views.position_window.close()
        print("you might be wondering why you aren't being asked to compare values, its because I haven't added that yet (ㆆ _ ㆆ)")
        helper.switch(position)
        break

    elif event == "Next Week":
        option = "nw"
        views.window.close()
        position, position_values = views.position_window.read()
        position = position.lower()
        views.position_window.close()
        compare, compare_values = views.compare_window.read()
        views.compare_window.close()
        helper.switch(position)
        break

    elif event == "Trade Values":
        tv.run_trade_values(True)
        print("Exiting application")
        exit(2)


#todo: add params to filter yes no to comparing players then take x amount of players to show and filter all the rest
#add more stats and also look for potentially more urls
# Get today's date in ddmmyyyy format
today_date = datetime.now().strftime('%m%d%Y')
today_date_week = (datetime.now()-timedelta(days=datetime.now().weekday()))
week = int((today_date_week - (nfl_start - timedelta(days=nfl_start.weekday()))).days / 7) + 1

options = ''
for pos in helper.accepted_positions:
  options = options + pos + " "
# URL of the website to scrape
if option == "ros":
    if position != 'all positions':
        helper.switch(position)
        url = "https://www.fantasypros.com/nfl/rankings/ros-" + position + ".php"
    else:
        url = "https://www.fantasypros.com/nfl/rankings/ros-overall.php"
elif option == "nw":
    url = helper.switch(position)
else:
    print("you did it wrong (╯°□°)╯︵ ┻━┻ or maybe I did something wrong ┬─┬ノ(ಠ_ಠノ)")
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
players = {}
list_of_players = []
for player_data in data.get('players', []):
    player_id = player_data.get('player_id')
    name = player_data.get('player_name')
    player_position = player_data.get('player_position_id')
    rank = player_data.get('rank_ecr')
    p=Player(player_id,name,position,rank)
    players.__setitem__(rank, p)
    if not player_id:
        continue
    raw_data.append([player_id, name, player_position, rank])

# Create a CSV file, write columns, and write raw data to CSV
isExist = os.path.exists(f"./reports/{today_date}")
if not isExist:
    os.makedirs(f"./reports/{today_date}")
    print("created new reports directory...... you're welcome")


player_names = list(helper.get_player_name_list(players))
player_names.sort()

if option == 'nw':
    if 'yes' == compare.lower():
        players_to_compare = helper.compare_window_players(views.create_player_dropdown_window(player_names), player_names)
        helper.compare(players, players_to_compare, position, week)

fileName = f"reports/{today_date}/ranks_{position}.csv"
with open(fileName, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Player ID", "Player Name", "Position", "Rank"])
    csv_writer.writerows(raw_data)

print(f"{fileName} Created Successfully")
cwd = os.getcwd()
print("full directory path is " + str(cwd) + " so look here for the reports folder")
