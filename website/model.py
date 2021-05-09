from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, Blueprint
from flask_sqlalchemy import SQLAlchemy


model = Blueprint('model', __name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Medx.db'
db = SQLAlchemy(app)
db.create_all()

def get_login_details():
    with sqlite3.connect('Medx.db') as connected:
        cur = connected.cursor()
        if 'email' not in session:
            logged_in = False
            name = ''
            no_of_items = 0
        else:
            logged_in = True
            cur.execute("SELECT user_id, name FROM users WHERE email = " + "'" + session['email'] + "'" )
            user_id, name = cur.fetchone()
            cur.execute("SELECT count(product_id) FROM cart WHERE user_id = " + str(user_id))
            no_of_items = cur.fetchone()[0]
    connected.close()
    return(logged_in, name, no_of_items)


@app.route("/checkout")
def checkout():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    logged_in, name, no_of_items = get_login_details()
    email = session['email']
    #model
    with sqlite3.connect('Medx.db') as connected:
        current = connected.cursor()
        current.execute("SELECT user_id FROM users WHERE email = '" + email + "'")
        user_id = current.fetchone()[0]
        current.execute("SELECT medicine.product_id, medicine.name, medicine.price, medicine.image FROM medicine, cart WHERE medicine.product_id = cart.product_id AND cart.user_id = " + str(user_id))
        medicine = current.fetchall()
    connected.close()
    #controller
    total_price = 0
    for row in medicine:
        total_price += row[2]
    return render_template("cart.html", products = medicine, total_price=total_price, logged_in=logged_in, name=name, no_of_items=no_of_items)

@app.route("/add_to_cart")
def add_to_cart():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        product_id = request.args.get('product_id')
        logged_in, name, no_of_items = get_login_details()
        #model
        with sqlite3.connect('Medx.db') as connected:
            cur = connected.cursor()
            cur.execute("SELECT user_id FROM users WHERE email =" + " '" + session['email'] + "'")
            user_id = cur.fetchone()[0]
            #controller
            try:
                cur.execute("INSERT INTO cart (user_id, product_id) VALUES (?, ?)", (user_id, product_id))
                connected.commit()
                message = 'Added Successfully!'
            except:
                connected.rollback()
                message = 'Error!'
        
        connected.close()
        print(message)


@app.route("/remove_from_cart")
def remove_from_cart():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    #model
    product_id = request.args.get('product_id')

    with sqlite3.connect('Medx.db') as connected:
        cur = connected.cursor()
        cur.execute("SELECT user_id FROM users WHERE email = " + "'" + email + "'")
        user_id = cur.fetcone()[0]
        #controller
        try:
            cur.execute("DELETE FROM cart WHERE user_id = " + str(user_id) + " AND product_id = " + str(product_id))
            connected.commit()
            message = "removed from cart"
        except:
            connected.rollback()
            message = 'Error!'
        connected.close()
        print(message)
        return redirect(url_for('checkout'))

@app.route("/product_description")
def product_description():
    logged_in, name, no_of_items = get_login_details()
    #model
    product_id = request.args.get('product_id')

    with sqlite3.connect('Medx.db') as connected:
        cur = connected.cursor()
        cur.execute('SELECT product_id, name, company_name, price, description, image, quantity, side_effects FROM medicine WHERE product_id = ' + product_id)
        product_data = cur.fetchone()
    connected.close()
    #controller
    return render_template('product_description.html', data=product_data, logged_in=logged_in, name=name,
                           no_of_items=no_of_items)
