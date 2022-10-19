# python version 3.9.7
# pip install flask==2.2.2
# pip install flask-mysqldb==1.0.1



import re
from flask import Flask, request, render_template, redirect
from credentials import port as PORT

user_data = {'emails': ['jpi@usr.edu'],
                'active_user': None,
                'jpi@usr.edu': {'items_owned': [], 'funds': 0, 'name': 'joe', 'password': 'jip', 'email': 'jpi@usr.edu'}}

items_db = []


app = Flask(__name__)

@app.route('/')
def root():
    if user_data['active_user'] is not None:
        return redirect('/user_cp')
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
            new_user['items_owned'] = []
            user_data[str(email)] = new_user
            user_data['active_user'] = email
        print(user_data)
        return redirect("/user_cp")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.j2')
    else:
        print('posting')
        email = request.form["email"]
        password = request.form["password"]
        print(email, password, user_data)
        if email in user_data["emails"] and password == user_data[email]['password']:
            print(email, user_data["emails"], password, user_data[email]['password'])
            print('login successful')
            user_data['active_user'] = email
            print(user_data)
            return redirect("/user_cp")
        else:
            print('no')
            return render_template('login.j2')

@app.route('/user_cp')
def user_cp():
    if user_data['active_user'] is not None:
        return render_template('user_cp.j2', user_data=user_data)
    return redirect('/login')

@app.route('/add_funds', methods=['GET', 'POST'])
def add_funds():
    if request.method == 'POST':
        try:
            amount = int(request.form['amount'])
        except:
            return render_template('add_funds.j2', user_data=user_data)
        user_data[user_data['active_user']]['funds'] += amount
    return render_template('add_funds.j2', user_data=user_data)


@app.route('/logout')
def logout():
    user_data['active_user'] = None
    return redirect('/')

@app.route('/add_item', methods=["GET", "POST"])
def add_item():
    if user_data['active_user'] == None:
        return redirect('/')
    if request.method == 'GET':
        return render_template('add_item.j2')
    name = value = rate = None
    try:
        name = request.form['name']
        value = int(request.form['value'])
        rate = int(request.form['rate'])
    except:
        return redirect('/add_item')
    return add_new_item(name, value, rate)


@app.route('/my_items')
def my_items():
    if user_data['active_user'] == None:
        return redirect('/')
    print('goint to my items...', items_db, user_data)
    return render_template('my_items.j2', user_data = user_data, items_db = items_db)

@app.route('/search')
def search():
    return render_template('search.j2')

@app.route('/borrowd')
def borrowd():
    return render_template('borrowd.j2')

def add_new_item(name, value, rate):
    id = len(items_db)
    owner = user_data['active_user']
    item = {'status': 'unloaned', 'name': name, 'value': value, 'rate': rate, 'owner': owner}
    items_db.append(item)
    user_data[owner]['items_owned'].append(id)
    return redirect('/my_items')


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
