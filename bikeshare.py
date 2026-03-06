import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """ 
    Asks user to specify a city, month, and day to analyze.
        
    Returns:
        city (str): Name if the city selected by the user.
        month (str): Month selected for filtering, or 'all'.
        day (str): Day of the week selected for filtering, or 'all'.
    """
    print('Welcome to BikeShare DataSearch! Let\'s explore some US bikeshare data!')
 
    # user input for city
    valid_cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?").lower()
        if city in valid_cities:
           break
        else:
           print("Invalid input. Please enter Chicago, New York City, or Washington.")

    # user input for filter type or none 
    valid_filters = ['month', 'day', 'none']
   
    while True:
        filter_type = input("Would you like to filter by month, day or none?").lower()
        if filter_type in valid_filters:
            break
        else:
           print("Invalid input. Please enter month, day, or none.")
    month = 'all'
    day = 'all'

    # user input for month
    if filter_type =='month':
        valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
   
        while True:
            month = input("Which month? (January - June):").lower()
            if month in valid_months:
                break
            else:
                print("Invalid month. Try again.")

    # user input for day
    elif filter_type == 'day':
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
       
        while True:
            day = input("Which day?:").lower()
            if day in valid_days:
                break
            else:
                print("Invalid day. Try again.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads bikeshare data for the specified city and filters by month and day if applicable.
    
    Args:
        city (str): The city whose data will be analyzed.
        month (str): Month filter applied to the dataset.
        day (str): Day of the week filter applied to the dataset.
    
    Returns:
        df (DataFrame): Filtered pandas DataFrame containing bikeshare data.
    """ 
    
    df = pd.read_csv(CITY_DATA[city])
    
    #convert Start Time to datetime 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month, day, hour 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month 
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df= df[df['month'] == month_index]
        
    # filter by day    
    if day != 'all':
        df= df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of bikeshare travel.

    This function calculates and prints the most common month, most common day of the week, and most common 
    start hour from the bikeshare dataset.

    Args:
        df (pandas.DataFrame): The dataframe containing bikeshare trip data.

    Returns:
        None
    """

    start_time = time.time()

    # display the most common month 
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print("Most Common Month:", months[common_month - 1])

    # display the most common day of week    
    common_day = df['day_of_week'].mode()[0]
    print("Most Common Day:", common_day)

    # display the most common start hour 
    common_hour = df['hour'].mode()[0]
    print("Most Common Start Hour:", common_hour)    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular bikeshare stations and trips.

    This function calculates and prints the most commonly used start and end stations, and the most common 
    trip combination (start station to end station).

    Args:
        df (pandas.DataFrame): The dataframe containing bikeshare trip data.

    Returns:
        None
    """

    start_time = time.time()

    # display most commonly used start station 
    common_start = df['Start Station'].mode()[0]
    print( "Most Common Start Station:", common_start)

    # display most commonly used end station 
    common_end = df['End Station'].mode()[0]
    print("Most Common End Station:", common_end)

    # display most frequent trip 
    df['Trip Combination'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip Combination'].mode()[0]
    print("Most Frequent Trip:", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Display statistics on the total and average trip duration.
    
    This function calculates and prints the total travel time and the mean travel time from the bikeshare 
    dataset.

    Args:
        df (pandas.DataFrame): The dataframe containing bikeshare trip data.

    Returns:
        None.
    """

    start_time = time.time()

    #display total travel time 
    total_time = df['Trip Duration'].sum()
    print("Total Travel Time:", total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean Travel Time:", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    This function calculates and displays the counts of user types, counts of gender, and the earliest, most 
    recent, and most common birth year.

    Args:
        df (pandas.DataFrame): The dataframe containing bikeshare trip data.

    Returns:
        None
    """

    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Type Counts:")
    print(user_types)
    print('-'*40)

    # display counts of gender 
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nGender Counts:") 
        print(gender_counts)
        print('-'*40)
    else:
        print("\nGender data not available for this city.")
        print('-'*40)

    # display earliest, most recent, and most common year of birth ---
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])

        print("\nEarliest Birth Year:", earliest)
        print("Most Recent Birth Year:", recent)
        print("Most Common Birth Year:", common)
        print('-'*40)
    else:
        print("\nBirth Year data not available for this city.")
        print('-'*40)
        
def gender_trip_length(df):
    """
    Displays the average trip duration grouped by gender and identifies which gender has the longest average    
    trip.
    
    Args:
        df (DataFrame): The pandas DataFrame containing bikeshare data.

    Returns:
        None
    """
    start_time = time.time()
    
    if 'Gender' in df.columns:
        avg_duration = df.groupby('Gender')['Trip Duration'].mean()
        
        print("Average Trip Duration by Gender:")
        print(avg_duration)

        longest = avg_duration.idxmax()
        print("\nGender with the longest average trip:", longest)
    
    else:
        print("Gender data not available for this city.")
      
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """
    Runs the bikeshare data analysis program.
    
    This function repeatedly asks the user for filters, loads the data, displays stats, optionally shows raw    
    data, and allows the user to restart the program.
    """
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        gender_trip_length(df)

        # display raw data 
        start_loc = 0
        while True:
            raw = input("Would you like to see 5 rows of raw data? Enter yes or no:").lower()
            
            if raw == 'no':
                break
            elif raw == 'yes':
                if start_loc >= len(df):
                    print("\nNo more data to display.")
                    break
                print("\nDisplaying next 5 rows of raw data:\n")
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
   
        # restart program 
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        
            if restart == 'yes':
                break  # break restart loop and restart program
            elif restart == 'no':
                print("\nThank you for using the BikeShare DataSearch. Have a great day!")
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")  
            

if __name__ == "__main__":
	main()

