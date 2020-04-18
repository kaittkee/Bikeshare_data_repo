import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
      city =  input('Which of the following cities would you like to analyze: chicago, new york city, washington?\n')
      if city == 'chicago' or  city == 'new york city' or city == 'washington':
          print('Let\'s look at some stats for :', city)
          break
      else :
          print('That\'s not a valid entry! Please select from the given list of cities')

    while True:
      month =  input('Which month would you like to filter your data by: january, february, march, april, may,june. If you don\'t want to           filter by a particular month, type all?\n')
      if month == 'january' or  month == 'february' or month == 'march' or month == 'april' or month == 'may' or month =='june' or month ==         'all':
          print('Let\'s analyze:', month)
          break
      else :
          print('That\'s not a valid entry! Please try again!')

    while True:
      day =  input('Would you like to filter your data by a particular day of the week : monday, tuesday, wednesday, thursday, friday,             saturday, sunday. If you don\'t want to filter by a particular day, type all?\n')
      if day == 'monday' or  day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day =='saturday' or day ==           'sunday' or day == 'all':
          print('Let\'s analyze:', day)
          break
      else :
          print('Please select a valid option')

    print('-'*40)
    return city, month, day
"""
filters the data and loads it into a dataframe based on the inputs provided by the user for the questions above
"""
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df
    
"""
 Calculates and prints time stats like the most common month, day of the week, start time, most common hour along 
 with the counts for each of these variables based on the user inputs for city, day and month
 Returns:
 Most common month - The month that appeared maximum number of times in the input
 Most common day of the week - The day of the week that appeared maximum number of times in the input
 Most common hour - The hour that appeared maximum number of times in the input
 Maximum Value Count - Gives the count for each of the variables
 """
def time_stats(df): 
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time() 
    counts_by_months = df['month'].value_counts()
    index_of_month_w_max_counts = max(counts_by_months.index)
    max_value_count = max(counts_by_months)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    final_month = months[index_of_month_w_max_counts - 1]
    print("The most common month is:",(final_month))
    print("Maximum value count is:",max_value_count)
    
    counts_by_day = df['day_of_week'].value_counts()
    name_of_day_w_max_counts = counts_by_day.idxmax(axis = 1)
    max_value_count = max(counts_by_day)
    print("The most common day is:",name_of_day_w_max_counts)
    print("Maximum value count is:",max_value_count)
    
    df['hour'] = df['Start Time'].dt.hour
    counts_by_hour = df['hour'].value_counts()
    most_common_start_hour = counts_by_hour.idxmax(axis = 1)
    max_value_count = max(counts_by_hour)
    print("The most common hour is : " , most_common_start_hour)
    print("Maximum value count is:",max_value_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
"""
Calculates the most common start and end stations and the most common trip (a combination of start and end stations) for a city, day and month based on user inputs
Returns:
Most common start station - The start station that appeared maximum number of times in the input
Most common end station - The end station that appeared maximum number of times in the input
Start station value count - The number of times start station appeared in the input
End Station value count - The number of times end station appeared in the input
Common Start and End station combination - The most common start and end station combination
Combination value counts - The number of times the start and end station combination occur in input
"""
def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    most_common_start_station = df['Start Station'].value_counts()
    start_station_name = most_common_start_station.idxmax(axis = 1)
    start_station_value_count =  max(most_common_start_station)

    most_common_end_station = df['End Station'].value_counts()
    end_station_name = most_common_end_station.idxmax(axis = 1)
    end_station_value_count =  max(most_common_end_station)
    
    df['Counter'] = 1
    common_combination = df.groupby(['Start Station' ,'End Station'])['Counter'].count().reset_index().sort_values(by = 'Counter', ascending      = False).iloc[0]
    start_stn = common_combination['Start Station']
    end_stn = common_combination['End Station']
    count = common_combination['Counter']
    print("The most common combination is: " , start_stn , "," , end_stn, " and count is:", count)
    print("Most common Start Station is:" ,start_station_name, ",", "and count is:", start_station_value_count)
    print("Most common End Station is:" , end_station_name, ",", "and count is:", end_station_value_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
"""
Calculates the trip duration statistics like total travel time and mean travel time
Returns:
Total travel time - In hours
Mean travel time  - In minutes
"""
def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    
    start_time = time.time()
    total_travel_time = (df['Trip Duration'].sum())/(60*60)
    print("Total trip duration:" ,total_travel_time, "hours")
    
    mean_travel_time = (df['Trip Duration'].mean())/60
    print("Mean travel time:" , mean_travel_time, "minutes")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
"""
Calculates user statistics based on User type, Gender and birth date
Returs:
User Type : User Type with the corresponding counts
Gender : Gender of the user and the corresponding counts
Earliest birth year - The minimum birth year in the input data
Most common birth year - The birth year which appeared maximum number of times in the input data
Most recent birth year - The maximum birth year in the input data
Please note the birth year and gender are available only for NYC and Chicago 

"""
def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)

    if 'Gender' in df.columns:
        counts_by_gender = df['Gender'].value_counts()
        print(counts_by_gender)

    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].value_counts().idxmax(axis = 1)
        print("Earliest birth year:", earliest_birth_year)
        print("Most recent Birth Year:", most_recent_birth_year)
        print("Most common birth year:" ,most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    index = 0
    while index in range (len(df)):
         show_raw_data = input('Would you like to see raw data. Type yes or no?\n')
         index = index + 5
         if show_raw_data == 'Yes':
              print(df.iloc[index - 5:index])
         else:
             break
          
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
