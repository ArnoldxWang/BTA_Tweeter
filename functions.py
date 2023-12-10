import pandas as pd
from datetime import datetime, timedelta
from functions import *


def month_num(month):
    m_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12, '': None}
    return str(m_dict[month])


def todtfromdf(df, datec, timec, row_num):
    ''' df, str, str, int -> datetime
    from dataframe takes date/time w format 'Wed, Oct 25, 2023' and '7:30p' reformates it to 2023/10/25 7:30:00
    Turns reformatted string into datetime
    Moves Date time up 12 hours (turning it into pm)
    '''
    date_str = df.at[row_num, datec][-4:] + '/'  # add year
    date_str += month_num(df.at[row_num, datec][5:8]) + '/'  # add month
    # if day is single digit, string will be 15 characters long
    if len(df.at[row_num, datec]) == 16:
        date_str += df.at[row_num, datec][9:10] + ' '  # if day is single digit
    else:
        date_str += df.at[row_num, datec][9:11] + ' '  # if day is double digit
    time_str = df.at[row_num, timec].rsplit('p')[0]

    date_str += time_str + ':00'  # add time

    # tell datetime how string is going to be formatted
    date_format = '%Y/%m/%d %H:%M:%S'
    try:
        date_obj = datetime.strptime(
            date_str, date_format)  # reformat datetime
        date_obj = date_obj + timedelta(hours=12)  # move forward 12 hours
        return date_obj

    except:
        return 'End of DF'


def find_last_occurrence(df, column_name, value):
    """
    Find the index of the last occurrence of a value in a specific column of a Pandas DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to search.
    - column_name (str): The name of the column to search.
    - value: The value to find.

    Returns:
    - Index of the last occurrence of the value in the specified column.
      Returns None if the value is not found.
    """
    try:
        last_occurrence_index = df[df[column_name] == value].index[-1]
        return last_occurrence_index
    except IndexError:
        # IndexError will be raised if the value is not found
        return 'IndexError will be raised if the value is not found'


def recent_game_url(df, column='Unnamed: 4', value='Box Score'):
    ''' (df, str, str) -> str
    Uses schedule df and builds a string YYYYMMDD0LOC based on the most recent game
    Note: Column will always be set to Unnamed: 4 and value will always be Box Score

    YYYY = Year
    MM = Month
    DD = Day
    0
    LOC = 3 letter code either Home TOR or @ filled by nba teams dictionary
    '''
    YYYYMMDD0LOC = ''
    recent_game_index = find_last_occurrence(df, column, value)
    YYYYMMDD0LOC += str(df.iloc[recent_game_index][3].year)
    YYYYMMDD0LOC += df.iloc[recent_game_index][3].strftime('%m')
    YYYYMMDD0LOC += df.iloc[recent_game_index][3].strftime('%d')
    YYYYMMDD0LOC += '0'
    if df.iloc[recent_game_index][5] == 'Home':
        YYYYMMDD0LOC += 'TOR'
    elif df.iloc[recent_game_index][5] == '@':
        YYYYMMDD0LOC += nba_teams[df.iloc[recent_game_index][6]]

    return YYYYMMDD0LOC


def game_url(df, url='https://www.basketball-reference.com/boxscores/'):
    url += recent_game_url(df)
    url += '.html'
    return url


def num_of_threes(df):
    # grab number of 3's taken via last row (team totals), column 6 (3P)
    return (df.iloc[-1][5])
# check if now is after 3 hours post game starting


def is_game_finished(df, column='Unnamed: 4', value='Box Score'):
    ''' (df)->(bool)
    Checks if time datetime.now is after most recent game is finished
    This function assumes nba games last MAX 3.5 hours. Typical games are 2-2.5
    Time now must be within a certain interval to ensure the game has recently ended (13.5 hours after game finishes)
    '''
    recent_game_index = find_last_occurrence(df, column, value)
    # Assumes game is done after 3.5 hours
    post_game_time = df.iloc[recent_game_index][3] + \
        timedelta(hours=3.5)
    return datetime.now() > post_game_time and datetime.now() < post_game_time + timedelta(hours=10)


nba_teams = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BRK',
    'Charlotte Hornets': 'CHO',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'Los Angeles Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHX',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS'
}
