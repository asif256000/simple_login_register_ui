# import time
# import flask
from flask import Flask, request, render_template
from flask import redirect, url_for

# from flask_bootstrap import Bootstrap
from intermediate_fn import websiteFunctions

fn_obj = websiteFunctions()

app = Flask(__name__)
# Bootstrap(app)


@app.route("/")
def homepage_view():
    try:
        args_dict = request.args
        msg = None
        if 'msg_to_display' in args_dict:
            msg = args_dict['msg_to_display']
        return render_template("index.html", display_msg=msg)
    except Exception as exc:
        print(f"Error {exc} while displaying home page.")
        return redirect(url_for('homepage_view'))


@app.route("/login_and_regn")
def view_login_regn_page():
    try:
        args_dict = request.args
        message, go_to = None, None
        if 'msg' in args_dict:
            message = args_dict['msg']
        if 'go_to' in args_dict:
            go_to = args_dict['go_to']
        return render_template("login_regn.html", alert_msg=message, go_to_page=go_to)
    except Exception as exc:
        print(f"Error {exc} while displaying login and registration page.")
        return redirect(url_for('homepage_view'))


@app.route("/welcome_<usr>")
def user_welcome(usr):
    try:
        return render_template("welcome_user.html", user=usr)
    except Exception as exc:
        print(f"Error {exc} while displaying user welcome page.")
        return redirect(url_for('homepage_view'))


@app.route("/user_login", methods=['GET', 'POST'])
def user_logging_in():
    try:
        if request.method != 'POST':
            return redirect(url_for('view_login_regn_page'))
        user = request.form['username']
        pw = request.form['password']
        if fn_obj.login_user(user, pw):
            print(f"{user}: {pw} YAY")
            return redirect(url_for('user_welcome', usr=user))
        else:
            log_str = 'Incorrect Username or Password!!'
            print(log_str)
            # flask.flash(log_str)
            return redirect(url_for('view_login_regn_page', msg=log_str))
    except Exception as exc:
        print(f"Error {exc} while logging in...")
        return redirect(url_for('homepage_view'))


@app.route("/user_registration", methods=['GET', 'POST'])
def user_regn():
    try:
        if request.method != 'POST':
            return redirect(url_for('view_login_regn_page'))
        user = request.form['username']
        mail_id = request.form['email_id']
        pw = request.form['password']
        conf_pw = request.form['confirm_password']
        check_val = request.form.getlist('agree-terms')
        if pw != conf_pw:
            log_str = "Passwords do not match"
            print(log_str)
            return redirect(url_for('view_login_regn_page', msg=log_str))
        elif 'agree-terms' not in check_val:
            log_str = 'Terms and Conditions not accepted'
            print(log_str)
            return redirect(url_for('view_login_regn_page', msg=log_str))
        else:
            print('CONDITIONS ACCEPTED AND PASSWORDS MATCH')
            ins = fn_obj.register_user(user, mail_id, pw)
            if isinstance(ins, str):
                return redirect(url_for('view_login_regn_page', msg=ins))
            elif ins:
                print('USER REGISTERED')
                msg_str = f'User {user} has been registered. You can login now!'
                return redirect(url_for('homepage_view', msg_to_display=msg_str))
            else:
                log_str = 'USER NOT REGISTERED SOME ERROR OCCURRED'
                print(log_str)
                return redirect(url_for('view_login_regn_page', msg=log_str))
    except Exception as exc:
        print(f"Error {exc} while registering user...")
        return redirect(url_for('homepage_view'))


@app.route("/user_deletion")
def user_del():
    try:
        user = request.args.get('user')
        fn_obj.delete_user(user)
        return render_template("deleted_user.html", username=user)
    except Exception as exc:
        print(f"Error {exc} while deleting user...")
        return redirect(url_for('homepage_view'))


@app.route("/test")
def hello():
    # return render_template("deleted_user.html", username='Asif')
    return "Hello, World!"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

