from flask import Flask, g, jsonify, render_template, request, redirect,url_for
from sqlalchemy import create_engine

app = Flask(__name__)


# function that connects to the RDS database using the credentials
def connect_to_database():
    engine = create_engine("mysql+mysqldb://comp30830:password@comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
                           "/comp30830")
    return engine


# function that gets the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

# Route for the home page that renders the base.html template
# gets the static data from the rds to populate the drop downs
@app.route('/')
def base():
        try:
            engine = get_db()
            datalist = []
            rows = engine.execute("SELECT * FROM BikeStatic;")
            for row in rows:
                datalist.append(dict(row))
            if datalist:
                #return jsonify(available=datalist)
               return render_template('base.html', datalist=datalist)
            else:
                print("No Static Data exists")
                return redirect('/')
        except:
            redirect('/')




# Route for 404 errors
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404.html")



# route for providing the dynamic information for a given station id
@app.route("/<int:station_id>", methods=['GET', 'POST'])
def get_dynamic():
    if request.method == 'POST':
        station_id = request.form['stopID']
        try:
            engine = get_db()
            data = []
            rows = engine.execute("SELECT * FROM BikeDynamic where Stop_Number = {} "
                                  "order by Last_Update desc limit 1;".format(station_id))

            for row in rows:
                data.append(dict(row))
            if data:

                return jsonify(available=data)
            else:
                print("No such station id")
                return redirect('/')
        except:
            redirect('/')

    return redirect('/')


@app.route("/static", methods=['GET', 'POST'])
def get_static():
    if request.method == 'GET':
        try:
            engine = get_db()
            datalist = []
            rows = engine.execute("SELECT * FROM BikeStatic;")
            for row in rows:
                datalist.append(dict(row))
            if datalist:
                return jsonify(available=datalist)

            else:
                print("No Static Data exists")
                return redirect('/')
        except:
            redirect('/')

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
