import requests
from bs4 import BeautifulSoup
import pandas as pd
from functions import *

url_schedule = 'https://www.basketball-reference.com/teams/TOR/2024_games.html'
# Send an HTTP request to the URL
response = requests.get(url_schedule)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup_schedule = BeautifulSoup(response.text, 'html.parser')

    # Now you can work with the parsed HTML, for example, print the title
    # print("Title:", soup_schedule.title.text)

    # Here, you can add more code to extract and manipulate data from the HTML
else:
    print(
        f"Error: Unable to fetch the URL. Status code: {response.status_code}")
schedule = soup_schedule.find_all(id='games')

schedule_table = pd.read_html(str(schedule))[0]

# Replace column names with ones that make sense
new_columns = {"Unnamed: 3": 'DateTime', 'Start (ET)': 'Time', "Unnamed: 5": "Location",
               'Unnamed: 7': 'Result', 'Unnamed: 8': 'Overtime?', 'Notes': 'In-Season Tournament'}
schedule_table.rename(columns=new_columns, inplace=True)
# Note In Season Tornaments
schedule_table['In-Season Tournament'].replace(
    'In-Season Tournament', True, inplace=True)
# Overtime
schedule_table['Overtime?'].replace('OT', True, inplace=True)

# Replace Nan Location values with home
schedule_table.fillna(
    {'Location': 'Home', 'In-Season Tournament': False}, inplace=True)
# Remove extra rows
schedule_table.drop([20, 41, 62], inplace=True)
schedule_table.reset_index(inplace=True)
schedule_table.drop(columns='index', inplace=True)
# Fill DateTime column using Date and Time
# for index, row in df.iloc[:-1].iterrows():
for index, row in schedule_table.iloc[:-1].iterrows():
    schedule_table.at[index, 'DateTime'] = todtfromdf(
        schedule_table, 'Date', 'Time', index)
    if schedule_table.at[index, 'Unnamed: 4'] == 'Box Score' and schedule_table.at[index, 'Overtime?'] != True:
        schedule_table.at[index, 'Overtime?'] = False
# Check Schedule_table
# print(schedule_table.head(30))
