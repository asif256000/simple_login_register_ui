import hashlib
import json
import sys
import uuid

from db_functions import SqlFunctions

with open('db_connect.json', 'r') as db_file:
    db_creds = json.load(db_file)

db_obj = SqlFunctions("localhost", str(db_creds['username']), str(db_creds['password']))


class websiteFunctions:

    def __init__(self):
        pass

    def register_user(self, user_id, user_mail, user_pw):
        """

        :param user_id:
        :param user_mail:
        :param user_pw:
        :return:
        """
        try:
            pw_res = db_obj.get_singlerow_from_sql('userinfo', 'user_pw', ['user_name', 'user_password'], f'user_name="{user_id}"')
            user_res = db_obj.get_singlerow_from_sql('userinfo', 'user_mail', ['user_id', 'user_mail'], f'user_id="{user_id}"')

            if pw_res or user_res:
                return f'User {user_id} already exists'
            
            hashed_pw, user_salt = self.hash_password(user_pw)

            if hashed_pw and user_salt:
                pw_bool = db_obj.insert_to_sql('userinfo', 'user_pw', ['user_name', 'user_password', 'user_salt'],
                                               [user_id, hashed_pw, user_salt])
                user_bool = db_obj.insert_to_sql('userinfo', 'user_mail', ['user_id', 'user_mail'], [user_id, user_mail])
            else:
                return False

            return pw_bool or user_bool
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False

    def login_user(self, user_id, password):
        """

        :param user_id:
        :param password:
        :return:
        """
        login_check = False
        try:
            result_dict = db_obj.get_singlerow_from_sql('userinfo', 'user_pw',
                                                        ['user_name', 'user_password', 'user_salt'],
                                                        f'user_name="{user_id}"')
            print(result_dict, 'result_dict')
            if result_dict and self.check_password(
                result_dict['user_password'], result_dict['user_salt'], password
            ):
                login_check = True
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
        finally:
            return login_check

    def delete_user(self, user_id):
        """

        :param user_id:
        :return:
        """
        try:
            db_obj.delete_from_sql('userinfo', 'user_pw', f'user_name="{user_id}"')
            db_obj.delete_from_sql('userinfo', 'user_mail', f'user_id="{user_id}"')

            return True
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False

    def hash_password(self, password):
        try:
            # uuid is used to generate a random number
            salt = uuid.uuid4().hex  # os.urandom(32) returns byte, not string. Can be handled by storing separately.
            return hashlib.sha256(salt.encode() + password.encode()).hexdigest(), salt
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return None, None

    def check_password(self, hashed_password, salt, user_password):
        try:
            return hashed_password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            print(f"Error filename: {fname}\nError type: {exc_type}\n"
                  f"Error line: {exc_tb.tb_lineno}\nError msg: {exc}")
            return False
