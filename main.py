import UpdateDB
import timeit
import time


# Main module.
def main():
    cnt = 0
    while cnt < 500:
        start = timeit.default_timer()
        estimates = UpdateDB.UpdateDB.scrape_estimates()
        UpdateDB.UpdateDB.update_db(estimates)
        stop = timeit.default_timer()
        print('Time taken to insert new rows:', stop - start)
        cnt += 1
        time.sleep(60)


if __name__ == '__main__':
    main()
