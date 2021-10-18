import sys

import mysqlx


# import mysql.connector


class SqlFunctions:
    """
    This class is defined to perform basic SQL queries and operations.

    :param ip: IP Address of the database server.
    :type ip: basestring
    :param user: Username of the database admin to be logged into.
    :type user: basestring
    :param pw: Password for the given user.
    :type pw: basestring
    """
    def __init__(self, ip, user, pw):
        """
        Constructor method for class SqlFunctions.

        :param ip: IP Address of the database server.
        :type ip: basestring
        :param user: Username of the database admin to be logged into.
        :type user: basestring
        :param pw: Password for the given user.
        :type pw: basestring
        """
        try:
            self.conn_obj = self.create_connection(ip, user, pw)
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n",
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")

    def create_connection(self, host_name, user_name, user_password):
        """
        Function to create a connection to SQL Database.

        :param host_name: IP Address of the database server.
        :param user_name: Username of the database admin to be logged into.
        :param user_password: Password for the given user.
        :return: Connection object to the database if connection is established.
        :rtype: MySQLConnection or PooledMySQLConnection
        """
        connection = None
        try:
            connection = mysqlx.get_client({
                'host': host_name,
                'port': 33060,
                'user': user_name,
                'password': user_password
                # 'ssl-mode': mysqlx.SSLMode.DISABLED
            },
                {"enabled": False
                 })
            # connection = mysql.connector.connect(
            #     host=host_name,
            #     user=user_name,
            #     passwd=user_password
            # )
            print(f"Connection to MySQL DB to user {user_name} successful")
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
        finally:
            return connection

    def insert_to_sql(self, dbname, tablename, column_list, values_list):
        """
        Function to insert some value (single row in a function call) to some table in connected MySQL instance.

        :param dbname:
        :param tablename:
        :param column_list:
        :param values_list:
        :return: True if insertion was successful, False otherwise.
        :rtype: bool.
        """
        sess = self.conn_obj.get_session()
        sess.start_transaction()
        try:
            db = sess.get_schema(dbname)
            table = db.get_table(tablename)

            assert len(column_list) == len(values_list)

            table.insert(column_list).values(values_list).execute()

            return True
        except AssertionError:
            print('Length of Columns and Values don\'t match')
            sess.rollback()
            return False
        except Exception as exc:
            sess.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False
        finally:
            sess.commit()

    def delete_from_sql(self, dbname, tablename, query_str):
        """

        :param dbname:
        :param tablename:
        :param query_str:
        :return:
        """
        sess = self.conn_obj.get_session()
        sess.start_transaction()
        try:
            db = sess.get_schema(dbname)
            table = db.get_table(tablename)

            table.delete().where(query_str).execute()

            return True
        except Exception as exc:
            sess.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False
        finally:
            sess.commit()

    def get_singlerow_from_sql(self, dbname, tablename, column_list, query_str):
        """
        Fetches single row matching the query from connected MySQL instance.

        :param dbname:
        :param tablename:
        :param column_list:
        :param query_str:
        :return: Dictionary having column names as keys and their values as values. If nothing is found, returns False.
        :rtype: dict or bool.
        """
        sess = self.conn_obj.get_session()
        sess.start_transaction()
        try:
            db = sess.get_schema(dbname)
            table = db.get_table(tablename)

            result = table.select(column_list).where(query_str).execute().fetch_one()

            if result:
                return dict(zip(column_list, result))
            else:
                return False
        except Exception as exc:
            sess.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False
        finally:
            sess.commit()

    def get_multiplerows_from_sql(self, dbname, tablename, column_list, query_str, num_of_rec_reqd):
        """
        Fetches limited number of row matching the query from connected MySQL instance.

        :param dbname:
        :param tablename:
        :param column_list:
        :param query_str:
        :param num_of_rec_reqd:
        :return: Dictionary having column names as keys and their values as values. If nothing is found, returns False.
        :rtype: dict or bool.
        """
        sess = self.conn_obj.get_session()
        sess.start_transaction()
        try:
            db = sess.get_schema(dbname)
            table = db.get_table(tablename)

            result = table.select(column_list).where(query_str).limit(num_of_rec_reqd).execute().fetch_all()

            if result:
                return [dict(zip(column_list, res)) for res in result]
            else:
                return False
        except Exception as exc:
            sess.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False
        finally:
            sess.commit()

    def get_allrows_from_sql(self, dbname, tablename, column_list, query_str):
        """
        Fetches all rows matching the query from connected MySQL instance.

        :param dbname:
        :param tablename:
        :param column_list:
        :param query_str:
        :return: List containing dictionaries having column names as keys and their values as values. If nothing is found, returns False.
        :rtype: list or bool.
        """
        sess = self.conn_obj.get_session()
        sess.start_transaction()
        try:
            db = sess.get_schema(dbname)
            table = db.get_table(tablename)

            result = table.select(column_list).where(query_str).execute().fetch_all()

            if result:
                ret_list = list()
                for res in result:
                    ret_list.append(dict(zip(column_list, res)))
                return ret_list
            else:
                return False
        except Exception as exc:
            sess.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False
        finally:
            sess.commit()

    def update_data_in_sql(self, dbname, tablename):
        """

        :param dbname:
        :param tablename:
        :return:
        """
        sess = self.conn_obj.get_session()
        sess.start_transaction()
        try:
            db = sess.get_schema(dbname)
            table = db.get_table(tablename)

        except Exception as exc:
            sess.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False
        finally:
            sess.commit()


if __name__ == '__main__':
    pass