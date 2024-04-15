import random
import mysql.connector
from classes.common.data_entry import DataEntry
import settings.config_loader as config_loader

table_names = ["Problem", "ProblemMeta", "Meta", "Test"]

settings = config_loader.get_settings()

global_db = mysql.connector.connect(
    host = settings.mysql.hostname,
    port = 3306,
    user = settings.mysql.user,
    password = settings.mysql.password,
    database = "chery_society"
)
cursor = global_db.cursor()

# Print first (num_dump) entries of the table. (Dump all if num_dump == -1)
def dump_table(table_name, num_dump = -1):
    cursor.execute("SHOW COLUMNS FROM " + table_name)
    headers = cursor.fetchall()

    header_names = []
    for header in headers:
        header_names.append(header[0])
    print(header_names)

    cursor.execute("SELECT * FROM " + table_name)
    row_datas = cursor.fetchall()

    if num_dump == -1:
        num_dump = len(row_datas)

    for index in range(num_dump):
        print(row_datas[index])


# Load data of a table: dict of (key: id, value: DataEntry)
def load_table(table_name):
    cursor.execute("SHOW COLUMNS FROM " + table_name)
    headers = cursor.fetchall()

    cursor.execute("SELECT * FROM " + table_name)
    row_datas = cursor.fetchall()

    print("Loading table '{0}', which has {1} entries.".format(table_name, len(row_datas)))

    id_index = -1
    for i in range(len(headers)):
        if headers[i][0] == "id":
            id_index = i
            break

    if id_index == -1:
        print("'id' column not found in the table; aborted.")
        return

    entries = {}

    for row_data in row_datas:
        cur_entry = DataEntry(table_name)
        
        for (header, data) in zip(headers, row_data):
            cur_entry.set_attribute(header[0], data)
        
        entries[row_data[id_index]] = cur_entry
    
    return entries

# Resolve "key_name" attribute of dict, from id to DataEntry
def resolve_foreign_key(dict, foreign_dict, key_name):
    for value in dict.values():
        foreign_key = value.get_attribute(key_name)
        
        resolved_value = None
        if foreign_key in foreign_dict:
            resolved_value = foreign_dict[foreign_key]
        
        value.set_attribute(key_name, resolved_value)

data = {}

# Get full data: dict of (key: table name, value: dict of (id, DataEntry))
def get_full_data():
    global data
    if len(data) > 0:
        return data

    for table_name in table_names:
        data[table_name] = load_table(table_name)

    resolve_foreign_key(data["Problem"], data["ProblemMeta"], "code")
    resolve_foreign_key(data["Problem"], data["Test"], "test_id")
    resolve_foreign_key(data["ProblemMeta"], data["Meta"], "meta_id")
    resolve_foreign_key(data["Test"], data["Meta"], "meta_id")

    return data
