import settings.db_loader as db_loader

if __name__ == "__main__":
    num_dump = 5

    for table_name in db_loader.table_names:
        print("# Raw data of table '{0}'".format(table_name))
        db_loader.dump_table(table_name, num_dump)
        print("------------------------------------")

    data = db_loader.get_full_data()

    for table_name, table_dict in data.items():
        print("# Loaded data of table '{0}'".format(table_name))
        value_list = list(table_dict.values())
        for i in range(num_dump):
            print(value_list[i])
        print("------------------------------------")
