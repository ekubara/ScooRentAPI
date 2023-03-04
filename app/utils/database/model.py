from mysql.connector import connect


class Connector:
    """This class is container for db connection."""

    connection = connect(
        host='localhost',
        user='scoorentadmin',
        password='scoorentpassword',
        database='ScooRentDB',
        autocommit=True
    )
