from flask import Flask, render_template, g, request, redirect
import sqlite3

app = Flask(__name__)

#database
DATABASE = 'menu.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#closes database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#default homepage
@app.route("/")
def home():
    cursor = get_db().cursor()
    #gets cursor and displays the menu
    sql = "SELECT * FROM menulist"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("menu.html", results = results)

#adding burgers into the menu
@app.route('/add', methods=["GET" , "POST"])
def add():
    if request.method == "POST":
        cursor = get_db().cursor()
        #gets the new item name, price and mealprice
        new_burger = request.form["item_name"]
        new_price = request.form["item_price"]
        new_meanprice = request.form["item_meal"]
        sql = "INSERT INTO menulist(name, price, mealprice) VALUES (?,?,?)"
        cursor.execute(sql,(new_burger, new_price, new_meanprice))
        #adds into the database
        get_db().commit()
    return redirect('/')
    

@app.route('/delete', methods=["GET","POST"])
def delete():
    if request.method == "POST":
        #gets the item and deletes it from the database
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM menulist WHERE id = ?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
