import psycopg2 as ps


class Database:

    __HOST = "localhost"
    __DATABASE = "chat"
    __USER = "postgres"
    __PASSWORD = "newpassword98"
    __TABLE = "users"

    def __init__(self):
        self.__CONNECTION = self.__connect()
        self.__CURSOR = self.__CONNECTION.cursor()

    def __connect(self):
        return ps.connect(host=self.__HOST,
                          database=self.__DATABASE,
                          user=self.__USER,
                          password=self.__PASSWORD)

    def __disconnect(self):
        ''' _disconnect(self) -> disconnects connection to database for a given object'''

        self.__CURSOR.close()
        self.__CONNECTION.close()

    def __check_if_user_exists(self, username):
        ''' _check_if_user_exists(user_id) -> creates a sql query that returns
        user_id if a given user_id exists in a table, else returns false'''

        self.__CURSOR.execute(
            f"SELECT user_id FROM {self.__TABLE} WHERE username LIKE '{username}'")
        return True if len(self.__CURSOR.fetchall()) > 0 else False

    def _log_in(self, username, password):
        ''' _log_in(username, password) -> function that returns True in case that
        username and password combination match and False otherwise or in case that
        user with given username doesn't exist'''

        if(not self.__check_if_user_exists(username)):
            return False

        self.__CURSOR.execute(
            f"SELECT username, password FROM {self.__TABLE} WHERE username LIKE '{username}'")
        credientals = self.__CURSOR.fetchone()
        print(credientals[0])
        return True if username == credientals[0] and password == credientals[1] else False

    def _register(self, username, password):
        ''' _register(username, password) -> function that adds new user to table with given username, password
        combination and return True in case that user with given username doesn't exist already, otherwise return False'''

        if(self.__check_if_user_exists(username)):
            return False

        self.__CURSOR.execute(
            f"INSERT INTO {self.__TABLE} VALUES ('{username}', '{password}')")
        self.__CONNECTION.commit()
        self.__CURSOR = self.__CONNECTION.cursor()
        self.__create_table(username)
        return True

    def __create_table(self, name):
        ''' _create_table(name) -> Call internaly only, function that creates new table when a
        new user is added, the table should be called user_[username]'''

        self.__CURSOR.execute(
            f'CREATE TABLE user_{name} (user_id INT NOT NULL UNIQUE)')
        self.__CONNECTION.commit()
        self.__CURSOR = self.__CONNECTION.cursor()
        self.__CURSOR.execute(
            f'ALTER TABLE user_{name} ADD FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE')
        self.__CONNECTION.commit()
        self.__CURSOR = self.__CONNECTION.cursor()

    def _add_friend(self, username, friend):
        if(not self.__check_if_user_exists(friend)):
            return False

        self.__CURSOR.execute(
            f"SELECT user_id FROM users WHERE username LIKE '{friend}'")
        friend_id = self.__CURSOR.fetchone()[0]
        self.__CURSOR.execute(
            f"INSERT INTO user_{username} VALUES ({friend_id})")
        self.__CONNECTION.commit()
        return True

    def _delete_user(self, username):
        if(not self.__check_if_user_exists(username)):
            return False

        try:
            self.__CURSOR.execute(f"DROP TABLE user_{username}")
            self.__CONNECTION.commit()
        except:
            pass

        self.__CURSOR.execute(
            f"DELETE FROM users WHERE username LIKE '{username}'")
        self.__CONNECTION.commit()

        return True


def main():
    db = Database()
    username = "Naruto"
    password = "newpassword98"
    if(not db._log_in(username=username, password=password)):
        print("Error: Couldn't LogIn")
        if(not db._register(username=username, password=password)):
            print("Error: Couldn't Register")
        else:
            print(f"Registration succeded! {username}")
    else:
        print("LogIn succeded!")

    username = "NotNarutoFan"
    password = "newpassword98"
    if(not db._log_in(username=username, password=password)):
        print("Error: Couldn't LogIn")
        if(not db._register(username=username, password=password)):
            print("Error: Couldn't Register")
        else:
            print(f"Registration succeded! {username}")
    else:
        print("LogIn succeded!")

    db._add_friend("Naruto", username)

    # db._delete_user(username)


if __name__ == "__main__":
    main()
