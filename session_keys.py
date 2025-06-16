from urllib.request import urlopen
import json
import pandas as pd
from streamlit import session_state

session_query = f"https://api.openf1.org/v1/sessions"
# Load in json data
def make_query(query):
    response = urlopen(query)
    data = json.loads(response.read().decode('utf-8'))
    return data
# Create df
data = make_query(session_query)
df = pd.DataFrame(data)

# Filter out unnecessary columns
df = df.iloc[:, [1, 2, 3, 4, 5, 6, 9, 11, 13]]

# Insert date column
df.insert(3, column = 'date', value = pd.to_datetime(df['date_start']).dt.strftime('%m/%d'))
# Rename start and end times
df = df.rename(columns={
    'date_start':'start_time',
    'date_end':'end_time'})
# Cut start and end times to just hh:mm
df.loc[:, 'start_time']=pd.to_datetime(df['start_time']).dt.strftime('%I:%M%p')
df.loc[:, 'end_time']=pd.to_datetime(df['end_time']).dt.strftime('%I:%M%p')

sessions = df

# Filter to only races
races = df[df['session_name']=='Race']

def get_year(df, input_year):
    # Given year, retrieves df of races/sessions that year
    result = df[df['year']==input_year]
    return result

def get_session_key(df, location):
    # Given location and df for a year, return session_key
    try:
        key = df[df['location']==location]['session_key'].item()
        return key
    except ValueError:
        print("Location not found")
