import UpdateDB
import timeit
import time
from UpdateDB import UpdateDB
from QueryDB import QueryDB
from DeleteDBRecords import DeleteDBRecords
from avg_wait_time_generator import filtered_wait_time_averages_stops
from weather_func import get_matching_weather_dates
from sports import get_sports_schedule


# Main module.
def main():
    print("Welcome to the Main Menu. Enter EXIT to exit the program.")
    request_close = False

    while True:
        try:
            main_select = input("\nEnter 1/2/3 to pick an option:\n1) Scrape new data\n2) Delete existing data\n3) Explore existing data\n")
            if main_select == 'EXIT':
                break

            if int(main_select) == 1:
                scrape_window()

            if int(main_select) == 2:
                delete_data_window()

            if int(main_select) == 3:
                explore_window()

            if int(main_select) < 0 or 3 < int(main_select):
                print('I couldn\'t understand that. Please enter 1, 2, or 3.')

        except ValueError as ve:
            print(ve)


def scrape_window():
    request_return = False

    while not request_return:
        choice1 = input("\nWelcome to the scrape menu. Enter 'RETURN' to return to the main menu.\nTo see a list of "
                        "routes that are available to scrape, enter ROUTES. To begin scraping, enter the lines you "
                        "would like to scrape separated by commas, like so: 71A, 71C, 65\n")

        if choice1 == 'RETURN':
            return

        if choice1 == 'ROUTES':
            available_routes = QueryDB.get_available_routes()
            for route in available_routes:
                print(route)

        if choice1 != 'ROUTES':
            routes_to_scrape = choice1.split(',')
            for i in range(len(routes_to_scrape)):
                routes_to_scrape[i] = routes_to_scrape[i].strip()

            n_iters = int(input("""Got it! How many times would you like to scrape the TrueTime website? On average, it takes about 30 per route, per scrape. Enter an int: """))
            print(f'Scraping {routes_to_scrape}, {n_iters} times...')

            cnt = 0
            while cnt < n_iters:
                start = timeit.default_timer()
                estimates = UpdateDB.scrape_estimates(['71C', '71A'])
                if estimates is not None:
                    UpdateDB.update_db(estimates)
                stop = timeit.default_timer()
                print('One scrape cycle completed, taking:', stop - start)
                cnt += 1
                print('Done scraping!')

def delete_all_estimates():
    final_delete_choice = input("Are you sure you want to delete all previously scraped data (Y/N)?")
    if final_delete_choice == 'Y':
        print('Deleting all previously scraped data...')
        DeleteDBRecords.wipe_estimates_table()
        print('Sucessfully deleted!')

def delete_by_stops():
    print('Currently you have these stops in your database:\n')
    stops = QueryDB.get_scraped_stops()
    for stop in stops:
        print(stop)
    choice2a = input("Select which stops you'd like to delete data for (for multiple stops, separate by commas: ")
    print(f'Deleting all data for {choice2a}')

    if ',' in choice2a:
        stops_to_delete = choice2a.split(',')
        for i in range(len(stops_to_delete)):
            stops_to_delete[i] = stops_to_delete[i].strip()

    if ',' not in choice2a:
        stops_to_delete = [choice2a.strip()]

    DeleteDBRecords.delete_by_criteria(stops_to_delete, [], [])

    print(f'Successfully deleted all data for {choice2a}')

def delete_by_routes():
    print('Currently you have these routes in your database:\n')
    routes = QueryDB.get_scraped_routes()
    for route in routes:
        print(route)
    choice2b = input("Select which routes you'd like to delete data for: ")
    print(f'Deleting all data for {choice2b}')

    if ',' in choice2b:
        routes_to_delete = choice2b.split(',')
        for i in range(len(routes_to_delete)):
            routes_to_delete[i] = routes_to_delete[i].strip()

    if ',' not in choice2b:
        routes_to_delete = [choice2b.strip()]

    DeleteDBRecords.delete_by_criteria([], routes_to_delete, [])

    print(f'Successfully deleted all data for {choice2b}')


def delete_by_dates():
    print('Currently you have data from these days in your database:')
    days = QueryDB.get_scraped_days()
    for day in days:
        print(day)
    choice2c = input(
        "Enter the dates you'd like to delete data for, separated by commas (e.g. 2020-10-05, 2020-10-07): ")
    print(f'Deleting all data for {choice2c}')

    if ',' in choice2c:
        dates_to_delete = choice2c.split(',')
        for i in range(len(dates_to_delete)):
            dates_to_delete[i] = dates_to_delete[i].strip()

    if ',' not in choice2c:
        dates_to_delete = [choice2c.strip()]

    DeleteDBRecords.delete_by_criteria([], [], dates_to_delete)

    print(f'Successfully deleted all data for {choice2c}')


def delete_data_window():
    request_return = False

    while not request_return:
        n_records = QueryDB.count_estimates()[0][0]

        choice1 = input(f"\nWelcome to the delete menu. Enter 'RETURN' to return to the main menu.\n"
                        f"You currently have {n_records} scraped datapoints in your database. "
                        "To delete data, enter DELETE ALL, or pick what criteria you'd like to delete by: STOP_ID, ROUTE_ID, DATES: ")

        if choice1 == 'RETURN':
            return

        if choice1 == 'DELETE ALL':
            delete_all_estimates()

        if choice1 == 'STOP_ID':
            delete_by_stops()

        if choice1 == 'ROUTE_ID':
            delete_by_routes()

        if choice1 == 'DATES':
            delete_by_dates()

def get_avg_frequency_for_all():
    print('Calculating average frequency...')
    scraped_stops = QueryDB.get_scraped_stops()
    scraped_routes = QueryDB.get_scraped_routes()
    scraped_days = QueryDB.get_scraped_days

    averages = []
    for route in scraped_routes:
        averages.append(filtered_wait_time_averages_stops(scraped_stops, route, scraped_days))

    for dict_list in averages:
        for key, value in dict_list.items():
            print(f'The average frequency at stop: {key} over the selected period is {value}')


def get_avg_frequency_by_criteria():
    # Limit by these days. Set should be a set of strings, one string per date.
    limit_by_days = set()

    sports_op = input("Filter by days when sports games are happening in the area? (YES/NO): ")

    if sports_op == 'YES':
        sports_dict = get_sports_schedule()
        for dictionary in sports_dict:
            for key in dictionary:
                # Validate input for correct date format.
                if len(key) == 10 and type(key) == str:
                    limit_by_days.add(key)

    weather_op = input("Filter by weather similar to today? (YES/NO)")

    weather_dates = []
    if weather_op == 'YES':
        weather_dates = get_matching_weather_dates()
        for weather_date in weather_dates:
            if len(weather_date) == 10 and type(weather_date) == str:
                limit_by_days.add(weather_date)

    print('limit_by_days', limit_by_days)

    stop_op = input("Only select data from these stops (separate stop_id with commas; if all enter ALL): ")

    if ',' in stop_op:
        stop_list = stop_op.split(',')
        for i in range(len(stop_list)):
            stop_list[i] = int(stop_list[i].strip())
    if ',' not in stop_op:
        stop_list = [int(stop_op.strip())]

    route_op = input("Select a route (you can only select one route, and you must select one): ")

    route = route_op.strip()

    print('Calculating average frequency based on entered parameters...')

    # Find the days for which we have data which are not in the list of selected dates.
    scraped_days_list = QueryDB.get_scraped_days()
    scraped_days_set = set(scraped_days_list)
    days_we_want = scraped_days_set - limit_by_days

    # Pass three parameter to this module. Each should either be a list of values, or an empty indicating "all" for that criterion
    averages = filtered_wait_time_averages_stops(stop_list, route, list(days_we_want))
    print(averages)
    if averages:
        for dict_list in averages:
            for key, value in dict_list.items():
                print(f'The average frequency at stop: {key} over the selected period is {value}')


def explore_window():
    exp_choice = int(input('Welcome to the explore window. Enter RETURN to return to the main menu. '
                           '\nEnter 1 or 2 to select an option:\n1) Get average frequency '
                           'for all data in your database.\n2) Select filters.\n'))

    if exp_choice == 'RETURN':
        return

    if exp_choice == 1:
        get_avg_frequency_for_all()

    if exp_choice == 2:
        get_avg_frequency_by_criteria()


if __name__ == '__main__':
    main()
