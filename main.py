import UpdateDB
import timeit
import time


# Main module.
def main():
    cnt = 0
    while cnt < 500:
        start = timeit.default_timer()
        estimates = UpdateDB.UpdateDB.scrape_estimates()
        if estimates is not None:
            UpdateDB.UpdateDB.update_db(estimates)
        stop = timeit.default_timer()
        print('Time taken to complete while loop:', stop - start)
        cnt += 1
        time.sleep(30)


if __name__ == '__main__':
    main()
