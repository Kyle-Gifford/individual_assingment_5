# python version 3.9.7
# pip install flask==2.2.2
# pip install flask-mysqldb==1.0.1



from flask import Flask, render_template
from credentials import port as PORT


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.j2')

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
