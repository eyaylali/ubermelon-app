from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""

    if "cart" not in session:
        session["cart"]={}

    melon_list= []
    for id, qty in session["cart"].items():
        melon = model.get_melon_by_id(id)
        melon_list.append((melon, qty))

    sum = 0
    for melon, qty in melon_list:
        sub_total = melon.price * qty
        sum = (sum + sub_total)
    sum = "%.2f" % sum

    sub_total_dictionary={}
    for melon, qty in melon_list:
        sub_total = melon.price * qty
        sub_total = "%.2f" % sub_total
        sub_total_dictionary[melon.common_name]= sub_total
        
    return render_template("cart.html", melon_list= melon_list, sum = sum, sub_total_dictionary=sub_total_dictionary)
 

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    if "cart" in session:
        if str(id) in session["cart"]: 
            qty =session["cart"][str(id)]
            qty = qty + 1
            session["cart"][str(id)] = qty
        else:
            session["cart"].update({id:1})
    else:
        session["cart"]={id:1}

    flash("You have successfully added a melon to your cart!")
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():

    if "user" in session:
        flash("You're already logged in!")
        ###get their name###
        ###create the text "logout"
        ###pass text to base template to change button text to "logout"
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""

    email= request.form.get("email")
    customer = model.get_customer_by_email(email)

    if customer == None:
        flash("No user with this email exists!")
    else:
        session["user"]={"name":customer.name,"email":customer.email}
        display_name = session["user"]["name"]
        g.display= "Hi",display_name
        flash("Login successful!")
        return redirect("/melons")

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
