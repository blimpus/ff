import requests
import pandas as pd
from datetime import datetime
import csv
accepted_positions = {'rb', 'qb', 'flex', 'te', 'k', 'dst'}
today_date = datetime.now().strftime('%m%d%Y')


def switch(position):
    position = position.lower()
    if position not in accepted_positions:
        print("entered value does not match a valid position. Valid positions are rb, qb, te, k, dst, flex")
        exit(1)
    return "https://www.fantasypros.com/nfl/rankings/"+position+".php"

def compare(players):
    for player in players.values():
        print(str(player.rank) + " " + player.position + " " + player.name + " " + str(player.id))
    rank1, rank2 = input("enter the ranks of the players you want to compare seperated by a space: ").split()

    full_player_1 = players.get(int(rank1))
    full_player_2 = players.get(int(rank2))

    if full_player_2.position != full_player_1.position:
        position = 'all_positions'
    else:
        position = str(players.get(int(rank1)).position)

    print(players.get(int(rank1)).get_data())
    player1 = players.get(int(rank1)).name
    player2 = players.get(int(rank2)).name

    get_ros_projection(player1, player2, position.lower())

def get_ros_projection(name1, name2, position):
    ros_projections_url = "https://www.fantasypros.com/nfl/projections/"+ position +".php?week=draft"
    response = requests.get(ros_projections_url)

    table_ff = pd.read_html(ros_projections_url)[0]

    list_of_stats = []
    headers_array = []
    headers = []
    for header in table_ff:
        headers_array.append(header)

    #todo: tables for kickers and dst are set up differently so will need if statement to fix headers here
    if 'k' in position.lower() or 'dst' in position.lower():
        for entry in headers_array:
            headers.append(entry)
    else:
        for entry in headers_array:
            headers.append(entry[0] + ' ' + entry[1])

    #remove leading bad data element from headers array
    headers[0] = 'PLAYER NAME'

    for player_name in table_ff.values.__array__().__array__():
        if name1 in player_name[0] or name2 in player_name[0]:
            list_of_stats.append(player_name)

    difference = ["differences"]
    for x in range(len(list_of_stats[0])):
        player1 = list_of_stats[0]
        player2 = list_of_stats[1]
        if x != 0:
            difference.append(player1[x]-player2[x])

    list_of_stats.append(difference)
    write_comparison_to_csv(position,list_of_stats,headers)

def write_comparison_to_csv(position,list_of_stats,headers):
    fileName = f"reports/{today_date}/ranks_{position}_comparison.csv"
    with open(fileName, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        csv_writer.writerows(list_of_stats)
        print("comparison created")


