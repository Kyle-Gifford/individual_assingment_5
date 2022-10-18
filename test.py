# python version 3.9.7
# pip install flask==2.2.2
# pip install flask-mysqldb==1.0.1



from flask import Flask, request, render_template, redirect
from credentials import port as PORT

user_data = {'emails': ['jpi@usr.edu'],
                'active_user': None,
                'jpi@usr.edu': {'name': 'joe', 'password': 'jip', 'email': 'jpi@usr.edu'}}


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.j2')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.j2')
    else:
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        if email not in user_data["emails"]:
            user_data["emails"].append(email)
            new_user = {"password": password, "email": email, "name": name}
            new_user['funds'] = 0
            user_data[str(email)] = new_user
            user_data['active_user'] = email
        print(user_data)
        return redirect("/home")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.j2')
    else:
        print('posting')
        email = request.form["email"]
        password = request.form["password"]
        print(user_data)
        print(email, user_data["emails"], password, user_data[email]['password'])
        if email in user_data["emails"] and password == user_data[email]['password']:
            print('login successful')
            user_data['active_user'] = email
            print(user_data)
            return redirect("/home")
        else:
            print('no')
            return render_template('login.j2')

@app.route('/home')
def home():
    return render_template('user_cp.j2', user_data=user_data)

@app.route('/logout')
def logout():
    user_data['active_user'] = None
    return redirect('/')


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
