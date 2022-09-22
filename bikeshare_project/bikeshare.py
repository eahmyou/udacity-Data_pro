import time
import pandas as pd
import numpy as np
#import calendar
import datetime

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

    # Initialize the variables city, month and day
    city = ''
    month = ''
    day = ''
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in ['chicago', 'new york city', 'washington']: # the loop condition will stay true till user input in valid 
        city= input('kindly select which city needed to explore bike data ,\
            \nselect from  Chicago, New York City, Washington (Note: inpute is case insensitive): ').lower() 
            #.lower() is added as User inputs should be made case insensitive,
            #which means the input should accept the string of "Chicago" and its case variants, such as
            #"chicago", "CHICAGO", or "cHicAgo". so whatever user input it will be passed to the variable as lower case

    #the next Formula extract the months' names from the dataset selected when city is selected.
    #so become general for datasets for different months    
    months = sorted(list(pd.to_datetime(pd.read_csv(CITY_DATA[city])['Start Time'])\
        .dt.month_name().unique()),key=lambda m: datetime.datetime.strptime(m, "%B")) 

    # get user input for month (all, january, february, ... , june)
    while (month.title() not in months ) and (month != 'all'):# the loop condition will stay true till user input in valid 
        month = input('select the month you of data need to be analyzed\nSelect from months {} or select all to see all periods (Note: inpute is case insensitive): '\
            .format(months)).lower()
            #.lower() is added as User inputs should be made case insensitive,
            #which means the input should accept the month name with different case variants a long as the month in months list,
            # #such as "may", "ARRil".the input passed to the variable as lower case

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day.title() not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] \
        and (day != 'all'): # the loop condition will stay true till user input in valid 
        day = input('select the day you want to chack [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday] or select all to act on all days (Note: inpute is case insensitive): ').lower()
            #.lower() is added as User inputs should be made case insensitive,
            #which means the input should accept the day name with different case variants a long as the spelling is correct, such as
            #"monDay", "SunDaY".the input passed to the variable as lower case

    print('-'*40)
    return city, month, day


def load_data(city, month='all', day='all'):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load the data based on city selection
    df = pd.read_csv(CITY_DATA[city])

    # extract month and day of week and start Hour from Start Time to create new columns
    df['Month'] = pd.to_datetime(df['Start Time']).dt.month_name()
    df['Day of week'] = pd.to_datetime(df['Start Time']).dt.day_name()
    df['Hour'] = pd.to_datetime(df['Start Time']).dt.hour

    # Create the DF based on the month and Day of week selection
    if month != 'all'and day != 'all':
        df = df[df['Month'] == month.title()]
        df = df[df['Day of week'] == day.title()]
        
    elif month == 'all' and day != 'all':
        df = df[df['Day of week'] == day.title()] 
    elif month != 'all'and day == 'all':
        df = df[df['Month'] == month.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    print('the most common month is: {} it is repeated {} times'\
    .format(df['Month'].mode()[0],df.groupby(['Month']).size().max()))

    # display the most common day of week
    print('The Most commn day of week is: {} it is repeated {} times'\
        .format(df['Day of week'].mode()[0],df.groupby(['Day of week']).size().max()))

    # display the most common start hour

    print('The Most commn start hour is: {} it is repeated {} times'\
        .format(df['Hour'].mode()[0],df.groupby(['Hour']).size().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('most commonly used start station is :{} it used as start station for {} times'\
        .format(df['Start Station'].mode()[0],df.groupby(['Start Station']).size().max()))

    # display most commonly used end station
    print('most commonly used end station is: {} it used as destination station for {} times'\
        .format(df['End Station'].mode()[0],df.groupby(['End Station']).size().max()))

    # display most frequent combination of start station and end station trip
    df['Route']=df['Start Station']+" <--> "+ df['End Station']
    print('most frequent combination of start station and end station trip is: {} riders used this route for {} times'\
        .format(df['Route'].mode()[0],df.groupby(['Route']).size().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel duration is : {}'.format(datetime.timedelta(seconds = float(df['Trip Duration'].sum()))))

    # display mean travel time
    print('Mean Travel duration is : {}'.format(datetime.timedelta(seconds = float(df['Trip Duration'].mean()))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('The Counts of Users types are: \n{}'.format(df['User Type'].value_counts()))
    

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nThe Counts based on Gender are: \n{}'.format(df['Gender'].value_counts()))
    else:
        print('\nNo Gender Data is available in the Data Set')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe earlist Year of birth is: {}, Most recent Year of birth is: {} and the most common Year of birth is: {}'\
            .format(int(df['Birth Year'].min()),int(df['Birth Year'].max()),int(df['Birth Year'].mode())))
    else:
        print('\nNo Birth Year Data is available in the Data Set')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_show(df):
    user_response = input ('Would you like to view 5 rows of individual trip data? Enter [yes] or no? ').lower()
    location = 0
    while user_response != 'no':
        print(df.iloc[location:location+5].to_json(orient="records",indent=4))
        location+=5
        user_response = input ('Would you like to view the next 5 rows of individual trip data? Enter [yes] or no? ').lower()
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_show(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
