import mysql.connector
def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS campus_care")
    cursor.execute("USE campus_care")  # Switch to the new database

def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        UserID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        DateOfBirth DATETIME NOT NULL,
        Role ENUM('User', 'Admin') DEFAULT 'User'
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserActivityPreferences (
            PreferenceID INT AUTO_INCREMENT PRIMARY KEY,
            UserID INT,
            Activity VARCHAR(255),
            FOREIGN KEY(UserID) REFERENCES Users(UserID)
        )
    """)

def insert_initial_data(cursor):
    query = "INSERT INTO Users (Username, Password, Email, DateOfBirth, Role) VALUES (%s, %s, %s, %s, %s)"
    data = [
        ('user1', 'password1', 'user1@example.com', '2000-01-01', 'User'),
        # Add more users as needed
    ]
    cursor.executemany(query, data)

def test_database(cursor):
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    assert ('campus_care',) in databases, "Database 'campus_care' not found"


def test_table(cursor):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    assert ('Users',) in tables, "Table 'Users' not found"
    assert ('UserActivityPreferences',) in tables, "Table 'UserActivityPreferences' not found"

def test_data(cursor):
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    assert len(users) > 0, "No data found in 'Users' table"

    cursor.execute("SELECT * FROM UserActivityPreferences")
    preferences = cursor.fetchall()
    assert len(preferences) >= 0, "Error occurred while fetching data from 'UserActivityPreferences' table"

def main():
    db = mysql.connector.connect(host='localhost', user='root', password='team37', port=32001)

    cursor = db.cursor()

    try:
        create_database(cursor)
        create_tables(cursor)
        insert_initial_data(cursor)
        db.commit()

        # Run tests
        test_database(cursor)
        test_table(cursor)
        test_data(cursor)
        print("All tests passed!")
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    except AssertionError as err:
        print(f"A test failed: {err}")
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
