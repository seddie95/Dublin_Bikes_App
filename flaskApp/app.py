from flask import Flask, g, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from logging import FileHandler, WARNING

app = Flask(__name__)

# Create errorlog text-file to store all the non http errors
if not app.debug:
    file_handler = FileHandler('errorlog.txt')
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)


# function that connects to the RDS database using the credentials
def connect_to_database():
    engine = create_engine("mysql+mysqldb://comp30830:password@comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
                           "/comp30830")
    return engine


# function that gets the database if it exists
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


def getStatic(json=False):
    """Function to retrieve the static data from the database and return it as either json or pass it to the
    html using jinja for the purpose of displaying the map data."""
    # call the function get_db to connect to the database
    try:
        engine = get_db()

        datalist = []
        # sql query that returns all of the static information form the RDS database
        rows = engine.execute("SELECT * FROM BikeStatic;")
        # for loop appends the rows to dictionary which will be inserted into the list datalist
        for row in rows:
            datalist.append(dict(row))

        # if the datalist list is not empty it will render the template base.html and pass it the function datalist
        # the datalist function will be used with jinja to populate the dropdown lists
        if datalist:
            if json:
                return jsonify(available=datalist)
            if not json:
                return render_template('index.html', datalist=datalist)
        else:
            noStatic = "Error: No static data was found "
            return render_template('index.html', noStatic=noStatic)

    except OperationalError:
        return '<h1> Problem connecting to the Database:</h1>' \
               '<br><h2>Please sit tight and we will resolve this issue</h2>' \
               '<br> <a href="/">Home</a>'


# Route for the home page that renders the base.html template
# gets the static data from the rds to populate the drop downs
@app.route('/')
def base():
    return getStatic()


# Route to get the static data in a json format
@app.route("/static")
def staticJson():
    return getStatic(json=True)


# route for providing the dynamic information for a given station id
@app.route("/dynamic")
def get_stations():
    try:
        engine = get_db()
        data = []

        SQLquery = """SELECT dd.Stop_Number, dd.Bike_Stands, dd.Available_Spaces,
                            dd.Available_Bikes, dd.Station_Status, dd.Last_Update,
                            sd.Stop_Name, sd.Banking, sd.Pos_Lat, sd.Pos_Lng
                            FROM comp30830.BikeDynamic as dd,comp30830.BikeStatic as sd
                            WHERE dd.Stop_Number = sd.Stop_Number AND (dd.Stop_Number,dd.Last_Update) IN
                                    (SELECT Stop_Number as SN, MAX(Last_Update) as LU
                                    FROM comp30830.BikeDynamic
                                    GROUP BY Stop_Number
                                    ORDER BY Last_Update desc);"""

        rows = engine.execute(SQLquery)

        for row in rows:
            data.append(dict(row))

        # test to see if the station is in the database by seeing if returned dictionary is empty
        if data:
            return jsonify(available=data)
        else:
            return '<h1>Station ID not found in Database</h2>'

    # OperationError states that the database does not exist
    except OperationalError:
        return '<h1> Problem connecting to the Database:</h1>' \
               '<br><h2>Please sit tight and we will resolve this issue</h2>' \
               '<br> <a href="/">Home</a>'


# Error  Webpages

# error handling for page not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


# Server error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')


if __name__ == "__main__":
    app.run(debug=True)
