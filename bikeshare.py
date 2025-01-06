
import time
import pandas as pd
import numpy as np
import calendar
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

# We load the Google stock data into a DataFrame
df1 = pd.read_csv('chicago.csv').assign(city='chicago', city_num=1)

# We load the Apple stock data into a DataFrame
df2 = pd.read_csv('new_york_city.csv').assign(city='new_york_city', city_num=2)

# We load the Amazon stock data into a DataFrame
df3 = pd.read_csv('washington.csv').assign(city='washington', city_num=3)

# Merge dataframes into one dataframe with all records. Rename unnamed column to id
df = pd.concat([df1, df2, df3])
df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)

# convert the Start Time column to datetime
df['Start Time'] = pd.to_datetime(df["Start Time"])

# extract hour from the Start Time column to create an hour column
df['hour'] = df['Start Time'].dt.hour
df['month'] = df['Start Time'].dt.month
df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

# start and endstation
df["trip"] = df["Start Station"] + " " + df["End Station"]

# lists of available choices to be used in functions
city_list = ['chicago', 'nyc', 'washington']
month_list = [1, 2, 3, 4, 5, 6]
day_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
choice_list = ['month', 'day', 'none', 'both']



def user_choice_month():
    """
    Asks user to specify a month and checks if choice is valid
    """
    global month
    while True:
        month = int(input('Which month are you interested in? Enter number of month, 1 to 6.'))
        if month in month_list:
            break
        else:
            print("Invalid month. Please try again!")
        return month


def user_choice_day():
    """
    Asks user to specify a day and checks if choice is valid
    """
    global day
    while True:
        day = input('Which weekday are you interested in?').lower()
        if day in day_list:
            break
        else:
            print("Invalid day. Please try again!")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        city - name of the city to analyze
        month - number of the month to filter by
        day - name of the day of week to filter by
    """
    global day
    day = 'none'
    global month
    month = 'none'
    global city
    global user_choice
    print('Hello! Let\'s explore some US bikeshare data!')

    loop_active = True
    while loop_active:
        city = input('What city are you interested in? Chicago, NYC or Washington.').lower()
        if city in city_list:
            break
        else:
            print("Invalid city. Please try again!")
    if city == 'nyc':
        city = 'new_york_city'
        print(city)

    while loop_active:
        user_choice = input("Would you like to filter by day, month, both or not at all? Enter 'none' for no filter").lower()
        if user_choice in choice_list:
            if user_choice == 'month':
                user_choice_month()
            if user_choice == 'day':
                user_choice_day()
            if user_choice == 'both':
                user_choice_day()
                user_choice_month()
            break
        else:
            print("Invalid choice. Please try again!")

    print('-'*40)
    return city, month, day


# Function for statistics
def station_statistics():

    print(f"As requested statistics for {city.capitalize()} will be presented.")
    if month != 'none':
        print(f"The requested month is {calendar.month_name[month]}.")
    if day != 'none':
        print(f"The following will include travelling in weekday {day.capitalize()}.")
    print("\n")
    df_temp = df.loc[(df['city'] == city)]

    if user_choice == 'month' or user_choice == 'both':
        df_temp = df.loc[(df['month'] == month)]
    if user_choice == 'day' or user_choice == 'both':
        df_temp = df.loc[(df['day_of_week'] == day)]
    print(f"The most common hour is {int(df_temp.mode()['hour'].iat[0])}.")
    if user_choice != 'day':
        print(f"The most common day is {df_temp.mode()['day_of_week'].iat[0]}.")
    if user_choice != 'month':
        print(f"The most common month is {int(df_temp.mode()['month'].iat[0])}.")
    print(f"The most common start station is {df_temp.mode()['Start Station'].iat[0]}.")
    print(f"The most common end station is {df_temp.mode()['End Station'].iat[0]}.")
    print(f"The most common combination of start and end station is {df_temp.mode()['trip'].iat[0]}.")
    print(f"The total travel time is {round(df_temp['Trip Duration'].sum()/3600, 0)} hours.")
    print(f"The average travel time is {round(df_temp['Trip Duration'].mean()/60, 0)} minutes.")
    print(f"The counts of each user type is \n{df_temp['User Type'].value_counts()}.")
    print(f"\nThe counts of each gender is \n{df_temp['Gender'].value_counts()}.")
    if city != 'washington':
        print(f"The earliest year of birth is {df_temp['Birth Year'].min()}.")
        print(f"The latest year of birth is {df_temp['Birth Year'].max()}.")
        print(f"The most frequent year of birth is {df_temp.mode()['Birth Year'].iat[0]}.")
    print('-'*40)
    raw = 'y'
    start = 1
    while raw == 'y':
        raw = input('Would you like to see some raw data(Y/N)?').lower()
        if raw == 'y':
            print(tabulate(df_temp.iloc[start:start + 5], headers='keys', tablefmt="fancy_grid"))
        else:
            raw == 'n'
        start += 5


while True:
    get_filters()
    station_statistics()
    print("Would you like to check some more statistics(Y/N)?")
    user_choice = input().lower()
    if user_choice == 'n':
        print('Perhaps another time. Thanks for using our services!')
        break
