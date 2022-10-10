import UpdateDB
import timeit
import time
from UpdateDB import UpdateDB
from QueryDB import QueryDB
from avg_wait_time_generator import filtered_wait_time_averages


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

def delete_data_window():
    request_return = False

    while not request_return:
        n_records = QueryDB.count_estimates()[0][0]

        choice1 = input(f"\nWelcome to the delete menu. Enter 'RETURN' to return to the main menu.\n"
                        f"You currently have {n_records} scraped datapoints in your database. "
                        "To delete data, enter DELETE ALL, or pick what criteria you'd like to delete by: STOP_ID, ROUTE_ID, DATE RANGE: ")

        if choice1 == 'RETURN':
            return

        if choice1 == 'DELETE ALL':
            print('Deleting all previously scraped data...')
            # DROP ESTIMATES TABLE
            print('Sucessfully deleted!')

        if choice1 == 'STOP_ID':
            print('Currently you have these stops in your database:\n')
            stops = QueryDB.get_scraped_stops()
            for stop in stops:
                print(stop)
            choice2a = input("Select which stops you'd like to delete data for: ")
            print(f'Deleting all data for {choice2a}')
            # DELETE RELEVANT DATA WITH SQL QUERY
            print(f'Successfully deleted all data for {choice2a}')

        if choice1 == 'ROUTE_ID':
            print('Currently you have these routes in your database:\n')
            routes = QueryDB.get_scraped_routes()
            for route in routes:
                print(route)
            choice2b = input("Select which routes you'd like to delete data for: ")
            print(f'Deleting all data for {choice2b}')
            # DELETE RELEVANT DATA WITH SQL QUERY
            print(f'Successfully deleted all data for {choice2b}')

        if choice1 == 'DATE RANGE':
            print('Currently you have data from these days in your database:')
            days = QueryDB.get_scraped_days()
            for day in days:
                print(day)
            choice2c = input("Enter the starting day (inclusive) of the range of days you'd like to delete: ")
            choice2d = input("Enter the ending day (inclusive) of the range of days you'd like to delete: ")
            print(f'Deleting all data for {choice2c} to {choice2d}')
            # DELETE RELEVANT DATA WITH SQL QUERY
            print(f'Successfully deleted all data for {choice2c} to {choice2d}')


def explore_window():
    exp_choice = int(input('Welcome to the explore window. Enter RETURN to return to the main menu. '
                           '\nEnter 1 or 2 to select an option:\n1) Get average frequency '
                           'for all data in your database.\n2) Select filters.'))

    if exp_choice == 'RETURN':
        return

    if exp_choice == 1:
        # We need to add functionality here to specify arguments
        print(filtered_wait_time_averages(args))

    if exp_choice == 2:
        # We need to add functionality here to specify arguments
        print(filtered_wait_time_averages(args))

if __name__ == '__main__':
    main()
