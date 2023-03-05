# import flask
from flask import Flask
# create an app instance
app = Flask(__name__)
# create a route /
@app.route("/")     
# define the function hello             
def hello():
   # return "hello world" when
   return "Hello World!"
# on running python app.py
if __name__ == "__main__":
   # run the flask app
   app.run()