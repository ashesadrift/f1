from session_keys import *

def find_session_key():
    input_year = int(input("Enter year: "))
    input_location = input("Enter location: ")

    year_races = get_year(races, input_year)
    session_key = get_session_key(year_races, input_location)
    print('Session key:', session_key)
    return session_key

# Get session key based on user input
session_key = find_session_key()

# Access race results
position_query = f"https://api.openf1.org/v1/position?session_key={session_key}"
race = make_query(position_query) # dict
df_race = pd.DataFrame(race)

# Fix time
df_race.loc[:, 'date']=pd.to_datetime(df_race['date']).dt.strftime('%m/%d %I:%M%p')


# Get final table
positions_sorted = df_race.sort_values(['driver_number', 'date'])
final_positions = positions_sorted.groupby('driver_number').tail(1)
final_positions = final_positions.sort_values('position')

def main():
    print(final_positions)
    return final_positions
main()