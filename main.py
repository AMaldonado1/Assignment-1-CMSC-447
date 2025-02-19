# import flask
# import flask_sqlalchemy
import pymysql
import getpass
import pandas as pd


DATABASE_NAME = "school"
FIND_DATABASE = (f"{DATABASE_NAME}",)
TABLE_NAMES = ("student", "instructor", "course", "enrollment")
FIND_TABLES = ((f"{TABLE_NAMES[0]}",), (f"{TABLE_NAMES[1]}",), (f"{TABLE_NAMES[2]}",), (f"{TABLE_NAMES[3]}",))
CREATE_TABLES = {f"{TABLE_NAMES[0]}": f"""CREATE TABLE {TABLE_NAMES[0]}
    (student_id     INT AUTO_INCREMENT, 
	 name           VARCHAR(20), 
	 credits        NUMERIC(3,0) CHECK (credits > 0),
	 PRIMARY KEY (student_id)
	) AUTO_INCREMENT=0;""",
                 f"{TABLE_NAMES[1]}": f"""CREATE TABLE {TABLE_NAMES[1]}
    (instructor_id      INT AUTO_INCREMENT, 
	 name               VARCHAR(20), 
	 department         VARCHAR(20),
	 PRIMARY KEY (instructor_id)
	) AUTO_INCREMENT=0;""",
                 f"{TABLE_NAMES[2]}": f"""CREATE TABLE {TABLE_NAMES[2]}
    (course_id          INT AUTO_INCREMENT, 
	 instructor_id      INT, 
	 name               VARCHAR(20),
	 credits            NUMERIC(3,0) CHECK (credits > 0),
	 PRIMARY KEY (course_id),
	 FOREIGN KEY (instructor_id) REFERENCES {TABLE_NAMES[1]}(instructor_id)
	    ON DELETE SET null
	) AUTO_INCREMENT=0;""",
                 f"{TABLE_NAMES[3]}": f"""CREATE TABLE {TABLE_NAMES[3]}
    (course_id          INT, 
	 student_id         INT, 
	 year               YEAR,
	 PRIMARY KEY (course_id, student_id),
	 FOREIGN KEY (course_id) REFERENCES {TABLE_NAMES[2]}(course_id)
	    ON DELETE CASCADE,
	 FOREIGN KEY (student_id) REFERENCES {TABLE_NAMES[0]}(student_id)
	    ON DELETE CASCADE	 
	);"""}

def delete_database(cursor):
    choice = input("Are you sure? Delete the whole database? (Y/N)")
    if choice.strip().upper() != "Y":
        print("Delete failed.")
        return False
    try:
        # If they agree to delete, and it works, database is removed
        cursor.execute(f"DROP DATABASE {DATABASE_NAME};")
        cursor.connection.commit()
        print("Delete successful!")
        return True

    except pymysql.err.OperationalError:
        print("Delete failed.")
        return False


def show_table(cursor, table_index):
    # Get all the columns/entities of the given table
    column_query = f"SHOW COLUMNS FROM {TABLE_NAMES[table_index]}"
    cursor.execute(column_query)
    columns = cursor.fetchall()
    # Get all the rows/entries of the given table
    row_query = f"SELECT * FROM {TABLE_NAMES[table_index]};"
    cursor.execute(row_query)
    rows = cursor.fetchall()
    # Make a dataframe to display in pandas
    columns = [column[0] for column in columns]
    df_table = pd.DataFrame(rows, columns=columns)
    print(f"\nTable: {TABLE_NAMES[table_index]}")
    print(df_table)


def view_table(cursor):
    view_table_menu = f"""
        Please choose a table(s) by number and space
        (ex: "2 4") to view both {TABLE_NAMES[1]} and {TABLE_NAMES[3]}
        or choose all:
        0. all
        1. {TABLE_NAMES[0]}
        2. {TABLE_NAMES[1]}
        3. {TABLE_NAMES[2]}
        4. {TABLE_NAMES[3]}
        5. Go back
        """
    print(view_table_menu)
    command = input(">> ")
    # Take their command, remove duplicates, sort and invalid input
    if "5" in command:
        return
    command = sorted({item.strip() for item in command.split() if item.strip() in ("0", "1", "2", "3", "4")})
    try:
        if not command:
            print("Invalid option.")
            return
        # For each table given as input, print it out
        for table_chosen in command:
            if table_chosen == "0":
                show_table(cursor, 0)
                show_table(cursor, 1)
                show_table(cursor, 2)
                show_table(cursor, 3)
                break
            else:
                show_table(cursor, int(table_chosen) - 1)
        return

    except pymysql.err.OperationalError:
        print("Unable to view tables.")
        return


def add_entry_full(cursor, table_index):
    # Get the full list of attributes to insert
    cursor.execute(f"SHOW COLUMNS FROM {TABLE_NAMES[table_index]}")
    all_attributes = cursor.fetchall()
    usable_attributes = [attribute[0] for attribute in all_attributes if "PRI" not in attribute[3]]
    attributes_type = [attribute[1] for attribute in all_attributes if "PRI" not in attribute[3]]
    complete_attributes = [f"{usable_attributes[i]} ({attributes_type[i]})" for i in range(len(attributes_type))]
    msg = f"""
    To add a(n) {TABLE_NAMES[table_index]} entry, type in each value for each attribute separate by comma space.
    Attribute(s): {", ".join(complete_attributes)}
    """
    print(msg)
    command = input(">> ")
    # Convert inputted attributes to correct type
    finished_command = []
    for attribute_type, attribute_name in zip(attributes_type, command.split(", ")):
        if attribute_type != "varchar(20)":
            finished_command.append(int(attribute_name))
        else:
            finished_command.append(attribute_name)
    # Add parameters by number of attributes
    total_attributes = []
    for i in range(len(usable_attributes)):
        total_attributes.append("%s")
    insert_parameters = f"({", ".join(total_attributes)})"
    # Insert the row to the table
    insert = f"INSERT INTO {TABLE_NAMES[table_index]} ({", ".join(usable_attributes)}) VALUES " + insert_parameters
    cursor.execute(insert, finished_command)
    cursor.connection.commit()
    return


def add_entry(cursor):
    add_entry_menu = f"""
        Please choose an option:
        0. Add {TABLE_NAMES[0]} entry
        1. Add {TABLE_NAMES[1]} entry
        2. Go back
        """
    print(add_entry_menu)
    command = input(">> ").strip()
    match command:
        case "0" | "1":
            try:
                add_entry_full(cursor, int(command))
            except (pymysql.err.OperationalError, TypeError, ValueError):
                print("Unable to add entry.")
                return
        case "2":
            return
        case _:
            print("Invalid option.")
            return
    return

def remove_entry_full(cursor, table_index):
    # Get the full list of attributes to remove
    cursor.execute(f"SHOW COLUMNS FROM {TABLE_NAMES[table_index]}")
    all_attributes = cursor.fetchall()
    primary_attributes = [attribute[0] for attribute in all_attributes if "PRI" in attribute]
    primary_attributes_types = [attribute[1] for attribute in all_attributes if "PRI" in attribute]
    complete_attributes = [f"{primary_attributes[i]} ({primary_attributes_types[i]})" for i in range(len(primary_attributes_types))]
    # Show rows to remove
    show_table(cursor, table_index)
    msg = f"""
        To remove a(n) {TABLE_NAMES[table_index]} entry, type in IDs/Primary Key(s) value from the entry separate by comma space.
        Primary Key(s): {", ".join(complete_attributes)}
        """
    print(msg)
    command = input(">> ")
    finished_command = [int(value.strip()) for value in command.split(", ")]
    # Add parameters by number of attributes
    total_attributes = []
    for i in range(len(finished_command)):
        total_attributes.append("%s")
    remove_parameters = f"({", ".join(total_attributes)})"
    # Remove the row to the table
    remove = f"DELETE FROM {TABLE_NAMES[table_index]} WHERE ({", ".join(primary_attributes)}) IN " + remove_parameters
    cursor.execute(remove, finished_command)
    cursor.connection.commit()
    return


def remove_entry(cursor):
    remove_entry_menu = f"""
            Please choose an option:
            0. Remove {TABLE_NAMES[0]} entry
            1. Remove {TABLE_NAMES[1]} entry
            2. Go back
            """
    print(remove_entry_menu)
    command = input(">> ").strip()
    match command:
        case "0" | "1":
            try:
                remove_entry_full(cursor, int(command))
            except (pymysql.err.OperationalError, TypeError, ValueError):
                print("Unable to remove entry.")
                return
        case "2":
            return
        case _:
            print("Invalid option.")
            return
    return


def delete_all(cursor):
    choice = input("Are you sure? Delete all entries/rows from all tables? (Y/N)")
    if choice.strip().upper() != "Y":
        print("Delete failed.")
        return
    try:
        # If they agree to delete, and it works, all rows are removed from all tables
        cursor.execute("SHOW TABLES;")
        all_tables = cursor.fetchall()
        for table in all_tables:
            cursor.execute(f"DELETE FROM {table[0]};")
            cursor.connection.commit()
        print("Delete successful!")
        return

    except pymysql.err.OperationalError:
        print("Delete failed.")
        return


def add_tables(cursor):
    print("\nChecking if all Tables already exist...")
    try:
        # Gets all the current tables in the database
        cursor.execute("SHOW TABLES;")
        all_tables = cursor.fetchall()
        # If the tables exist then use it, if not create it
        for table in FIND_TABLES:
            if table in all_tables:
                print(f"\"{table[0]}\" table already exists.")
            else:
                create_table = CREATE_TABLES[table[0]]
                cursor.execute(create_table)
                print(f"\"{table[0]}\" table has been created!")
        return True

    except pymysql.err.OperationalError:
        print(f"Unable to create Tables.")
        return False


def create_database(cursor):
    print(f"Checking if \"{DATABASE_NAME}\" database already exists...")
    try:
        # Gets all the current databases in the MySQL Server
        cursor.execute("SHOW DATABASES;")
        all_databases = cursor.fetchall()
        # If the database exists then use it, if not create it
        if FIND_DATABASE in all_databases:
            print(f"\"{DATABASE_NAME}\" database already exists.")
        else:
            create_school_database = f"CREATE DATABASE {DATABASE_NAME}"
            cursor.execute(create_school_database)
            print(f"\"{DATABASE_NAME}\" database has been created!")
        # Make sure we only use the school database, keep others hidden
        select_school_database = "USE school;"
        cursor.execute(select_school_database)
        return True

    except pymysql.err.OperationalError:
        print(f"Unable to create \"{DATABASE_NAME}\" database.")
        return False


def create_connection():
    # Connecting to the database, server is hosted on my local machine
    mysql_username = getpass.getpass("Enter Username: ")
    mysql_password = getpass.getpass("Enter Password: ")
    mysql_host = input("Enter Host (localhost): ")
    mysql_port = int(input("Enter Port (3306): "))

    # Use given credentials to establish connection to MySQL server
    try:
        server_connection = pymysql.connect(
            user=mysql_username,
            password=mysql_password,
            host=mysql_host,
            port=mysql_port
        )
        print("\nSuccessfully connected to the MySQL database!\n")
        return server_connection

    except pymysql.err.OperationalError:
        print("\nUnable to connect to MySQL database. Double check your credentials and server status.\n")
        return None


def main_menu(cursor):
    menu = """
    Please choose an option:
    0. View tables
    1. Add entry
    2. Remove entry
    3. Delete all entries (Tables are kept)
    4. Exit database
    5. Delete and Exit database
    """
    print(menu)
    command = input(">> ")
    match command:
        case "0":
            view_table(cursor)
        case "1":
            add_entry(cursor)
        case "2":
            remove_entry(cursor)
        case "3":
            delete_all(cursor)
        case "4":
            return True
        case "5":
            if delete_database(cursor):
                return True
        case _:
            print("Invalid option.")

    return False


def run_crud_app(cursor):
    # Check if school database already exists, if not make it
    if not create_database(cursor):
        return
    # Check if school tables already exists, if not make them
    if not add_tables(cursor):
        return
    # Main loop
    exit_database = False
    while not exit_database:
        exit_database = main_menu(cursor)
    # Exiting message
    print("Thank you for using School CRUD MySQL")
    return


def main():
    print("CMSC 447 Assignment 1 Part 2: School CRUD MySQL\n")
    # Attempt to create a connection
    mysql_server = create_connection()
    # Check if connection is successful
    if mysql_server is None:
        return
    # Create cursor for SQL
    cursor = mysql_server.cursor()
    # Simple CLI CRUD
    run_crud_app(cursor)
    # Close the MySQL server
    cursor.close()
    mysql_server.close()


if __name__ == "__main__":
    main()