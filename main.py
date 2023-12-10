import tweepy
import requests
from keys import *
from auth import *
from scraping import *
from bs4 import BeautifulSoup
from functions import *

print(game_url(schedule_table))
# Send an HTTP request to the URL
response = requests.get(game_url(schedule_table))

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Now you can work with the parsed HTML, for example, print the title
    # print("Title:", soup.title.text)

    # Here, you can add more code to extract and manipulate data from the HTML

else:
    print(
        f"Error: Unable to fetch the URL. Status code: {response.status_code}")
# Remove unnecessary top row with name: th.over_header.center
soup.find('tr', class_='over_header').decompose()
# name of table class: box-TOR-game-basic, grab table
rap_box = soup.find_all(id='box-TOR-game-basic')
# turn table class into a dataframe
rap_table = pd.read_html(str(rap_box))[0]
# check 3s
threes = num_of_threes(rap_table)
game_day = recent_game_url(schedule_table)[0:8]
if int(threes) >= 12:
    # create tweet w client
    get_twitter_conn_v2().create_tweet(
        text="Scored {0} three pointers! Free Fries Today! (Game day: {1})".format(threes, game_day))
elif int(threes) < 12:
    get_twitter_conn_v2().create_tweet(
        text="Only scored {0} threes. Better luck next time... (Game day: {1})".format(threes, game_day))
