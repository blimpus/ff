import requests
from datetime import datetime
import math
from lxml import html
import csv
import pandas as pd

def run_trade_values(content_not_found_switch):
    # Define the start date of NFL season (used to calculate which NFL week it is)
    static_date = datetime(2023, 9, 3)

    # Get today's date
    today_date = datetime.now()

    # Calculate the time difference
    time_difference = today_date - static_date

    # Calculate the number of weeks
    weeks_difference = math.ceil(time_difference.days / 7)

    if not content_not_found_switch:
        weeks_difference = weeks_difference - 1

    # Convert weeks to string to use in URL
    weeks_difference_str = str(weeks_difference)

    # URL of the website to scrape
    url = "https://www.fantasypros.com/2023/09/fantasy-football-trade-value-chart-week-" + weeks_difference_str + "-2023/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:

        ######## USING PANDAS ###########

        table_ff = pd.read_html(url)
        frames = [frame for frame in table_ff]

        # concat data frames with keys to position, so you can filter on what position you want to show later
        # example table_ff = table_ff.loc["TE"] will only show the TE positions
        table_ff = pd.concat(frames, keys=["QB", "RB", "WR", "TE"])

        # remove first row and set next row as column headers
        table_ff.columns = table_ff.iloc[0]
        table_ff = table_ff[1:]

        #Output data frame to csv
        pandas_filename = 'trade_values_pandas.csv'
        table_ff.to_csv(pandas_filename, index=True)

        print(f"saving pandas version of trade values to: {pandas_filename}")

        ######## USING traditional html scraping ###########

        # Parse the HTML response content
        tree = html.fromstring(response.text)

        # Find all the tables within the <div class="general-article__content">
        general = tree.xpath(".//div[@class='general-article__content']")

        if general is not None:
            data = []

            for general_element in general:
                tables = general_element.xpath(".//div[@class='mobile-table']")
                if tables is not None:
                    for table in tables:
                        rows = table.xpath(".//tr")
                        for row in rows:
                            cells = row.xpath(".//td")
                            row_data = [cell.text_content().strip() for cell in cells]
                            data.append(row_data)
            # Create CSV
            csv_filename = "tradeValues.csv"

            # Write data to CSV
            with open(csv_filename, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(data)

            print(f"Data has been saved to {csv_filename}")

        else:
            print("No tables found in content")
    elif content_not_found_switch:
        print("Content not found. Showing results for previous week")
        run_trade_values(False)
    else:
        print("Content not found.")
