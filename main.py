import UpdateDB
import timeit
import time
from UpdateDB import UpdateDB
from QueryDB import QueryDB


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
        choice1 = input("""Welcome to the scrape menu.\n Enter 'RETURN' to return to the main menu.\n To see a list of routes that 
        are available to scrape, enter ROUTES. To begin scraping, enter the lines you would like to scrape separated by 
        commas, like so: 71A, 71C, 65\n\n""")

        if choice1 == 'RETURN':
            return

        if choice1 == 'ROUTES':
            available_routes = QueryDB.get_available_routes
            for route in available_routes:
                print(route)

        n_iters = 1

        cnt = 0
        while cnt < n_iters:
            start = timeit.default_timer()
            estimates = UpdateDB.scrape_estimates(['71C', '71A'])
            if estimates is not None:
                UpdateDB.update_db(estimates)
            stop = timeit.default_timer()
            print('One scrape cycle completed, taking:', stop - start)
            cnt += 1

def delete_data_window():
    pass

def explore_window():
    pass


if __name__ == '__main__':
    main()
