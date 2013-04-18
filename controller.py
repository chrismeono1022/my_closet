from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

# from http://postgresapp.com/documentation - does this need to be moved inside "__main__"?
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/my_closet.db'
db = SQLAlchemy(app)


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)