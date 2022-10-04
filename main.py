import CreateDB

# Main module.


def main():
    CreateDB.CreateDB.make_db_with_stops()
    CreateDB.CreateDB.confirm_empty_table_generated()


if __name__ == '__main__':
    main()
