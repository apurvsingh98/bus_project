import pandas as pd

# The main function in this module is get_on_time_percent(), which reads data from the downloaded csv called
# 'on_time_percentage.csv' in the same directory. The function takes in a list of dates to filter by, and then returns
# the summary statistics from the csv, which comes from the Pittsburth Port Authority.


# This function takes in a str representing a single month and outputs a set with every possible combination of year
# and month in the csv dataset, formatted to be compatible with that dataset.
def get_all_year_combos(month):
    years_covered = ['2022', '2021', '2020', '2019', '2018', '2017']
    year_combos = set()
    for i in range(6):
        year_combos.add(int(years_covered[i] + month))
    return year_combos


# This function takes in a list of strings, each representing a single date formatted like '2022-10-10', and returns the
# a set of all months contained in the input list, formatted as a two-digit number.
def months_from_days(days):
    months = set()
    for day in days:
        date_parts = day.split('-')
        month = date_parts[1]
        months.add(month)
    return list(months)


# Input -> A list of strings representing days, and a string representing a ROUTE_ID.
# Output -> A dict, with the keys being the months present in the input dates, and the values each being a DataFrame
#           with three rows (SAT/SUN/WEEKDAY) and one column, representing the mean of the officially-reported on-time
#           percentage in the historical data.
def get_on_time_percent(days, route_id):
    # This dict allows us to format dates correctly.
    month_dict = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
                  '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    # Pull out the months represented in our inputted date strings.
    months = months_from_days(days)

    csv = pd.read_csv('on_time_percentage.csv')
    # Filter by the provided ROUTE_ID.
    csv = csv.loc[csv['route'] == route_id]

    results = {}
    for month in months:
        # For each month, combine with available years in the csv dataset using get_all_year_combos().
        year_combos = get_all_year_combos(month)
        # Filter DataFrame by month.
        var = csv.loc[csv['year_month'].isin(year_combos)]
        # Calculate means for SAT/SUN/WEEKDAY and add the resulting DataFrame to a dict of DataFrames, with each
        # DataFrame filtered by a particular month.
        results[month_dict[month]] = var.groupby(["day_type"])["on_time_percent"].mean()

    return results
