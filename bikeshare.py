import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to input a city, month, and day to filter the data.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    city = city.lower()
    while city not in ['chicago', 'new york city', 'washington']:
        if city == '':
            city = input('\nChoose the city you would like to explore. Please enter Chicago, New York City, or Washington.\n')
        else:
            print('\nSorry, there must be a typo.\n')
            city = input('\nPlease enter Chicago, New York City, or Washington.\n')

    # get user input for month (all, january, february, ... , june)
    month = ''
    month = month.lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        if month == '':
            month = input('\nChoose the month you would like to explore. Please enter the month from January to June. If you would like to explore all, Please enter all.\n')
        else:
            print('\nSorry, there must be a typo.\n')
            month = input('\nPlease enter the month from January to June. If you would like to explore all, Please enter all.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    day = day.lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        if day == '':
            day = input('\nChoose the day of week you would like to explore. Please enter the day from Monday to Sunday. If you would like to explore all, Please enter all.\n')
        else:
            print('\nSorry, there must be a typo.\n')
            day = input('\nPlease enter the day from Monday to Sunday. If you would like to explore all, Please enter all.\n')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into data drame
    df = pd.read_csv(CITY_DATA[city])
    df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)

    # convert Start Time into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # exact month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day od week
    if day != 'all':
        day = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month: ', common_month)
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week: ', common_day)
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station: ', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most Common End Station: ', end_station)

    # display most frequent combination of start station and end station trip
    trip_series = df['Start Station'] + " station to " + df['End Station'] + " station"
    print("The most popular trip starts from {}.".format(trip_series.mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time: ", df['Trip Duration'].sum())

    # display mean travel time
    print("Average Travel Time: ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count for Each User Type:\n", df.groupby(['User Type'])['ID'].count(), "\n")

    if city in ['chicago', 'new york city']:
        # Display counts of gender
        print("Count for Each Gender:\n", df.groupby(['Gender'])['ID'].count(), "\n")

        # Display earliest, most recent, and most common year of birth
        print("Earliest Birth Year: ", df['Birth Year'].min())
        print("Most Recent Birth Year: ", df['Birth Year'].max())
        print("Most Common Birth Year: ", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # show raw data if requested
        raw_data = input('\nWhould you like to see the raw data? Please enter yes or no.\n')
        index = 0
        while raw_data != 'no':
            if raw_data.lower() not in ['yes', 'no']:
                raw_data = input('\nI\'m not sure. Please enter yes or no.\n')
            else:
                print(df.iloc[index:index + 5], '\n')
                raw_data = input('\nWhould you like to see more raw data? Please enter yes or no.\n')
                index += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
