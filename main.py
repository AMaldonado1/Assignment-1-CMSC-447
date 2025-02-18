# import flask
# import flask_sqlalchemy
import pymysql
import getpass


DATABASE_NAME = "school"
FIND_DATABASE = (f"{DATABASE_NAME}",)
TABLE_NAMES = ("student", "instructor", "course", "enrollment")
FIND_TABLES = ((f"{TABLE_NAMES[0]}",), (f"{TABLE_NAMES[1]}",), (f"{TABLE_NAMES[2]}",), (f"{TABLE_NAMES[3]}",))
CREATE_TABLES = {f"{TABLE_NAMES[0]}": f"""CREATE TABLE {TABLE_NAMES[0]}
    (student_id     VARCHAR(10), 
	 name           VARCHAR(20), 
	 credits        NUMERIC(3,0) CHECK (credits > 0),
	 PRIMARY KEY (student_id)
	);""",
                 f"{TABLE_NAMES[1]}": f"""CREATE TABLE {TABLE_NAMES[1]}
    (instructor_id      VARCHAR(10), 
	 name               VARCHAR(20), 
	 department         VARCHAR(20),
	 PRIMARY KEY (instructor_id)
	);""",
                 f"{TABLE_NAMES[2]}": f"""CREATE TABLE {TABLE_NAMES[2]}
    (course_id          VARCHAR(10), 
	 instructor_id      VARCHAR(10), 
	 name               VARCHAR(20),
	 credits            NUMERIC(3,0) CHECK (credits > 0),
	 PRIMARY KEY (course_id),
	 FOREIGN KEY (instructor_id) REFERENCES {TABLE_NAMES[1]}(instructor_id)
	    ON DELETE SET null
	);""",
                 f"{TABLE_NAMES[3]}": f"""CREATE TABLE {TABLE_NAMES[3]}
    (course_id          VARCHAR(10), 
	 student_id         VARCHAR(10), 
	 semester           ENUM('Winter', 'Spring', 'Summer', 'Fall'),
	 year               YEAR,
	 PRIMARY KEY (course_id, student_id),
	 FOREIGN KEY (course_id) REFERENCES {TABLE_NAMES[2]}(course_id)
	    ON DELETE CASCADE,
	 FOREIGN KEY (student_id) REFERENCES {TABLE_NAMES[0]}(student_id)
	    ON DELETE CASCADE	 
	);"""}


def view_table():
    print("Table")
    pass


def add_entry():
    print("Adding new entry/row")


def remove_entry():
    print("Removing old entry/row")


def delete_all():
    print("Deleting all entries/rows")


def add_tables(cursor):
    print("\nChecking if all Tables already exist...")
    try:
        cursor.execute("SHOW TABLES;")
        all_tables = cursor.fetchall()
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
        cursor.execute("SHOW DATABASES;")
        all_databases = cursor.fetchall()
        if FIND_DATABASE in all_databases:
            print(f"\"{DATABASE_NAME}\" database already exists.")
        else:
            create_school_database = f"CREATE DATABASE {DATABASE_NAME}"
            cursor.execute(create_school_database)
            print(f"\"{DATABASE_NAME}\" database has been created!")
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
        print("\nUnable to connect to MySQL database. Double check your credentials.\n")
        return None


def main_menu(cursor):
    menu = """
    Please choose an option:
    1. View tables
    2. Add entry
    3. Remove entry
    4. Delete all entries
    5. Exit database
    """
    print(menu)
    command = input(">> ")
    match command:
        case "1":
            view_table()
        case "2":
            add_entry()
        case "3":
            remove_entry()
        case "4":
            delete_all()
        case "5":
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
    mysql_server.close()


if __name__ == "__main__":
    main()