import pandas as pd


def get_all_year_combos(month):
    years_covered = ['2022', '2021', '2020', '2019', '2018', '2017']
    year_combos = set()
    for i in range(6):
        year_combos.add(int(years_covered[i] + month))
    return year_combos


def months_from_days(days):
    months = set()
    for day in days:
        date_parts = day.split('-')
        month = date_parts[1]
        months.add(month)
    return list(months)


# Input -> A list of strings representing days, a string representing a ROUTE_ID.
# Output -> A dict, with the keys being the months present in the input dates. Each value is a DataFrame with three rows
#           (SAT/SUN/WEEKDAY) and one column, representing the mean of the officially-reported on-time percentage in
#           historical data.
def get_on_time_percent(days, route_id):
    month_dict = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
                  '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    months = months_from_days(days)

    csv = pd.read_csv('on_time_percentage.csv')
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 1000)

    csv = csv.loc[csv['route'] == route_id]

    results = {}
    for month in months:
        year_combos = get_all_year_combos(month)
        var = csv.loc[csv['year_month'].isin(year_combos)]
        results[month_dict[month]] = var.groupby(["day_type"])["on_time_percent"].mean()

    return results
