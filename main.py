# import flask
# import flask_sqlalchemy
import pymysql
import getpass


def delete_database():
    pass


def create_database():
    pass


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
        print("Successfully connected to the MySQL database!")
        return server_connection

    except pymysql.err.OperationalError:
        print("Unable to connect to MySQL database! Double check your credentials.")
        return None


def run_crud_app():
    pass


def main():
    # Attempt to create a connection
    mysql_server = create_connection()
    # Check if connection is successful
    if mysql_server is None:
        return

    cursor = mysql_server.cursor()
    mysql_server.close()
    # Check if school database already exists, if so use it



if __name__ == "__main__":
    main()