from flask import*
import pymysql
from functions import *
from mpesa import *
from werkzeug.security import generate_password_hash
import os
from datetime import datetime

app=Flask(__name__)
# session key 
app.secret_key="!@#$%^"
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Set the upload folder in the configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Directory to save uploaded images

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route("/")
def Homepage():
   
#    connect to DB 

 connection=pymysql.connect(
     host='os.getenv("DB_HOST")',
     user='os.getenv("DB_USER")',
     password='os.getenv("DB_PASSWORD")',
     database='os.getenv("DB_NAME")')
 
 sql="select * from products WHERE product_category = 'cups' "
 sql1="select * from products WHERE product_category = 'plates' "
 sql2="select * from products WHERE product_category ='hotpots' "
 sql3="select * from products WHERE product_category ='glasses' "
 
 
#  you need to have a cursor 
#  cursor-used to run /execute above sql 
 cursor=connection.cursor()
 cursor1=connection.cursor()
 cursor2=connection.cursor()
 cursor3=connection.cursor()


#  execute 
 cursor.execute(sql)
 cursor1.execute(sql1)
 cursor2.execute(sql2)
 cursor3.execute(sql3)


#  fetch  all the  rows

 cups=cursor.fetchall()
# fetch all monitors 
 plates=cursor1.fetchall()
 hotpots=cursor2.fetchall()
 glasses=cursor3.fetchall()

 return render_template("index.html",cups = cups,plates =plates,hotpots = hotpots,glasses = glasses)

# route fo a single item 
@app.route("/single/<product_id>")
def singleitem(product_id):
    # connection to db 
     connection=pymysql.connect(host='os.getenv("DB_HOST")',user='os.getenv("DB_USER")',password='os.getenv("DB_PASSWORD")',database='os.getenv("DB_NAME")')
# create sql query 
     sql= " select * from products where product_id = %s "
    #  create a cursor 
     cursor =connection.cursor()
     cursor.execute(sql,product_id)
    #  get the single product 
     product=cursor.fetchone() 
     return render_template ("single.html",product=product)

#upload products
@app.route("/upload",methods=['POST','GET'])
def Upload():
    if request.method == 'POST':
        # uer can add the products 
        product_name= request.form['product_name']
        product_desc =request.form['product_desc']
        product_cost =request.form['product_cost']
        product_category =request.form['product_category']
        product_image_name =request.files['product_image_name']
        product_image_name.save('static/images/' +  product_image_name.filename )

        # connection to db 

        connection=pymysql.connect(host='os.getenv("DB_HOST")',user='os.getenv("DB_USER")',password='os.getenv("DB_PASSWORD")',database='os.getenv("DB_NAME")')
        cursor=connection.cursor()

        sql= "insert into products (product_name, product_desc, product_cost, product_category, product_image_name) values(%s,%s,%s,%s,%s)"
        data = product_name, product_desc,product_cost,product_category ,product_image_name.filename


        # execute
        cursor.execute(sql,data)
        # save the changes 
        connection.commit()

        return render_template("upload.html", message = "product added successful")

    else:
     return render_template("upload.html", error = "please add a product ")
    
# fashion route-helps you nto see all the fashion 
@app.route("/decor")
def decor():
    connection=pymysql.connect(host='os.getenv("DB_HOST")',user='os.getenv("DB_USER")',password='os.getenv("DB_PASSWORD")',database='os.getenv("DB_NAME")')
    sql="select * from products WHERE product_category = 'curtains' "
    sql1="select * from products WHERE product_category = 'carpets' "
    sql2="select * from products WHERE product_category ='doormats' "
    sql3="select * from products WHERE product_category ='flowervest' "
    sql4="select * from products WHERE product_category ='frames' "
    
 
 
#  you need to have a cursor 
#  cursor-used to run /execute above sql 
    cursor=connection.cursor()
    cursor1=connection.cursor()
    cursor2=connection.cursor()
    cursor3=connection.cursor()
    cursor4=connection.cursor()



#  execute 
    cursor.execute(sql)
    cursor1.execute(sql1)
    cursor2.execute(sql2)
    cursor3.execute(sql3)
    cursor4.execute(sql4)


#  fetch  all the phones rows

    curtains=cursor.fetchall()
# fetch all monitors 
    carpets=cursor1.fetchall()
    doormats=cursor2.fetchall()
    flowervest=cursor3.fetchall()
    frames=cursor4.fetchall()
    

    return render_template("decor.html",curtains=curtains,carpets= carpets,doormats=doormats ,flowervest=flowervest,frames=frames, )
# a route to upload fashion
@app.route("/uploaddecor",methods=['POST','GET'])
def Uploaddecor():
    if request.method == 'POST':
        # uer can add the products 
        product_name= request.form['product_name']
        product_desc =request.form['product_desc']
        product_cost =request.form['product_cost']
        product_category =request.form['product_category']
        product_image_name =request.files['product_image_name']
        product_image_name.save('static/images/' +  product_image_name.filename )

        # connection to db 

        connection=pymysql.connect(host='os.getenv("DB_HOST")',user='os.getenv("DB_USER")',password='os.getenv("DB_PASSWORD")',database='os.getenv("DB_NAME")')
        cursor=connection.cursor()

        sql= "insert into products (product_name, product_desc, product_cost, product_category, product_image_name) values(%s,%s,%s,%s,%s)"
        data = product_name, product_desc,product_cost,product_category ,product_image_name.filename


        # execute
        cursor.execute(sql,data)
        # save the changes 
        connection.commit()

        return render_template("uploaddecor.html", message = "decor added successful")

    else:
     return render_template("uploaddecor.html", error = "please add a decor ")


@app.route("/about")
def About():
    return("this is about page")
# creating registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        gender = request.form['gender']
        phone = request.form['phone']
        password = request.form['password']
        
        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Database connection
        connection = pymysql.connect(host='os.getenv("DB_HOST")', user='os.getenv("DB_USER")', password='os.getenv("DB_PASSWORD")', database='os.getenv("DB_NAME")')

        cursor = connection.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_email = cursor.fetchone()
        
        if existing_email:
            return render_template("register.html", error="Email is already in use. Please use a different email.")

        # Insert new user record
        sql = "INSERT INTO users (username, email, gender, phone, password) VALUES (%s, %s, %s, %s, %s)"
        data = (username, email, gender, phone, hashed_password)

        # Execute and commit changes
        cursor.execute(sql, data)
        connection.commit()

        return render_template("register.html", message="Registration successful!")

    return render_template("register.html")
@app.route("/admin")
def admin():
    # Check if the user is logged in
    if 'key' not in session:
        return redirect("/login")  # Redirect to login if not logged in

    email = session['key']  # Retrieve the logged-in user's email from the session

    # Connect to the database
    connection = pymysql.connect(host='os.getenv("DB_HOST")', user='os.getenv("DB_USER")', password='os.getenv("DB_PASSWORD")', database='os.getenv("DB_NAME")')
    cursor = connection.cursor()

    # Query to check the user's role
    sql = "SELECT role FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    result = cursor.fetchone()  # Fetch the result from the query

    connection.close()  # Close the database connection

    # Check if the user has the 'admin' role
    if result and result[0] == 'admin':
        return render_template("admin.html")  # Allow access to the admin page
    else:
        return redirect("/")  # Redirect non-admin users to the homepage (or another page)

@app.route("/login", methods=['POST','GET'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    
       
       # connection to db 

        connection=pymysql.connect(host='os.getenv("DB_HOST")',user='os.getenv("DB_USER")',password='os.getenv("DB_PASSWORD")',database='os.getenv("DB_NAME")')
        cursor=connection.cursor()
#  check if user with email exist in the db 
        sql= "select * from users where email= %s and password = %s"
    
        data = (email,password)


        # execute
        cursor.execute(sql,data)
        # save the changes 
        if cursor.rowcount == 0:
            # it means if the username and password not found 

            return render_template("login.html", error= " invalid login credatials ")

        else:
            session['key']= email
            return redirect("/")
        
    return render_template("login.html")


    # mpesa  
    # implement STK PUSH 
@app.route('/mpesa', methods= ['POST'])
def mpesa():
   phone=request.form["phone"]
   amount=request.form["amount"]
   #use mpesa_payment function from mpesa.py 
   #it accepts the phone and amount as arguments
   mpesa_payment("1",phone) 



   return'<h1>Please complete payment in your form</h1>'\
   '<a href="/" class="btn btn-dark btn-sm">GO back to products </a>'

def get_products_by_category(category):
    """Retrieve products from the database based on the specified category."""
    # Connect to the MySQL database
    connection = pymysql.connect(host='os.getenv("DB_HOST")', user='os.getenv("DB_USER")', password='os.getenv("DB_PASSWORD")', database='os.getenv("DB_NAME")')
    
    try:
        with connection.cursor() as cursor:
            # Correct SQL query to fetch products based on the product_category
            query = "SELECT * FROM products WHERE product_category = %s"
            cursor.execute(query, (category,))
            
            # Fetch all products in the specified category
            products = cursor.fetchall()
            
        return products
    
    finally:
        connection.close()

# Flask route for the see_more page
@app.route('/see_more/<category>')
def see_more(category):
    # Retrieve all products in the specified category from the database
    products = get_products_by_category(category)
    
    # Render the see_more template with the category and products data
    return render_template('see_more.html', category=category, products=products)



# Search route
@app.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search_query").strip()
    connection = pymysql.connect(host='os.getenv("DB_HOST")', user='os.getenv("DB_USER")', password='os.getenv("DB_PASSWORD")', database='os.getenv("DB_NAME")')
    
    try:
        cursor = connection.cursor()
        
        # SQL query to search for products by name or description
        sql = "SELECT * FROM products WHERE product_name LIKE %s OR product_desc LIKE %s"
        like_query = f"%{search_query}%"
        cursor.execute(sql, (like_query, like_query))
        
        # Fetch results
        results = cursor.fetchall()
        
        # Print the structure of results to debug
        print("DEBUG: Results fetched from database:", results)
    finally:
        connection.close()
    
    # Render results page based on whether matches were found
    if results:
        return render_template("search_results.html", results=results, query=search_query)
    else:
        return render_template("search_results.html", results=None, query=search_query)



@app.route('/view_products')
def view_products():
    connection = pymysql.connect(
        host='os.getenv("DB_HOST")',
        user='os.getenv("DB_USER")',
        password='',
        database='os.getenv("DB_NAME")',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        # Fetch active products
        cursor.execute("SELECT * FROM products")
        active_products = cursor.fetchall()

        # Fetch deleted products
        cursor.execute("SELECT * FROM deleted_products")
        deleted_products = cursor.fetchall()

    connection.close()

    return render_template(
        'view_products.html',
        active_products=active_products,
        deleted_products=deleted_products
    )


@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    connection = pymysql.connect(
        host='os.getenv("DB_HOST")',
        user='os.getenv("DB_USER")',
        password='',
        database='os.getenv("DB_NAME")',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        # Fetch the product details
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

        # Move to deleted_products and delete from products table
        if product:
            cursor.execute(
                """
                INSERT INTO deleted_products (product_id, product_name, product_category, product_cost, deleted_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (product['product_id'], product['product_name'], product['product_category'], product['product_cost'], datetime.now())
            )
            cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
            connection.commit()

    connection.close()
    return redirect(url_for('view_products'))

@app.route('/restore/<int:product_id>', methods=['GET', 'POST'])
def restore_product(product_id):
    connection = pymysql.connect(
        host='os.getenv("DB_HOST")',
        user='os.getenv("DB_USER")',
        password='',
        database='os.getenv("DB_NAME")',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        # Fetch the product details from deleted_products
        cursor.execute("SELECT * FROM deleted_products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

        # If the form is submitted (POST), restore the product
        if request.method == 'POST' and product:
            cursor.execute(
                """
                INSERT INTO products (product_id, product_name, product_category, product_cost)
                VALUES (%s, %s, %s, %s)
                """,
                (product['product_id'], product['product_name'], product['product_category'], product['product_cost'])
            )
            # Delete from deleted_products after restoring
            cursor.execute("DELETE FROM deleted_products WHERE product_id = %s", (product_id,))
            connection.commit()

            flash("Product restored successfully!", "success")
            return redirect(url_for('view_products'))

    connection.close()
    return render_template('restore_product.html', product=product)


@app.route('/view_purchases')
def view_purchases():
    connection=pymysql.connect(host='os.getenv("DB_HOST")',user='os.getenv("DB_USER")',password='os.getenv("DB_PASSWORD")',database='os.getenv("DB_NAME")')

    with connection.cursor() as cursor:
        # SQL query to fetch purchase details
        query = """
            SELECT username AS user_name,email AS user_email,
                   products.product_name, products.product_cost,
                   purchases.mpesa_number
            FROM purchases
            JOIN users ON purchases.user_id = users.id
            JOIN products ON purchases.product_id =products.product_id
        """
        cursor.execute(query)
        purchases = cursor.fetchall()
    connection.close()
    
    # Render template with fetched data
    return render_template('view_purchases.html', purchases=purchases)


@app.route('/view_users')
def view_users():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of users per page
    offset = (page - 1) * per_page

    connection = pymysql.connect(host='os.getenv("DB_HOST")',
                                user='os.getenv("DB_USER")', password='',
                                cursorclass=pymysql.cursors.DictCursor ,
                                database='os.getenv("DB_NAME")')

    with connection.cursor() as cursor:
        # Fetch users with pagination, including id, username, email, and phone
        cursor.execute("SELECT id, username, email, phone FROM users LIMIT %s OFFSET %s", (per_page, offset))
        users = cursor.fetchall()

        # Get total user count for pagination calculation
        cursor.execute("SELECT COUNT(*) AS total FROM users")
        total_users = cursor.fetchone()['total']
    connection.close()

    # Calculate total pages
    total_pages = (total_users + per_page - 1) // per_page

    # Render the view_users template
    return render_template('view_users.html', users=users, page=page, total_pages=total_pages)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    connection=pymysql.connect(host='os.getenv("DB_HOST")',user='os.getenv("DB_USER")',password='os.getenv("DB_PASSWORD")',database='os.getenv("DB_NAME")')

    try:
        with connection.cursor() as cursor:
            # Delete the user with the specified ID
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            flash("User has been successfully deleted.", "success")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        flash("An error occurred while trying to delete the user.", "error")
    finally:
        connection.close()
    
    return redirect(url_for('view_users'))


@app.route('/daily_sales')
def daily_sales():
    connection=pymysql.connect(host='os.getenv("DB_HOST")',user='os.getenv("DB_USER")',password='os.getenv("DB_PASSWORD")',database='os.getenv("DB_NAME")')

    current_date = datetime.now().date()  # Get today's date

    try:
        with connection.cursor() as cursor:
            # Query to fetch sales for the current day
            cursor.execute("""
                SELECT sale_id, product_name, quantity, sale_date, total_amount 
                FROM sales 
                WHERE DATE(sale_date) = %s
                """, (current_date,))
            daily_sales = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        daily_sales = []
    finally:
        connection.close()

    return render_template('daily_sales.html', daily_sales=daily_sales, current_date=current_date)



@app.route('/view_stock')
def view_stock():
    connection = pymysql.connect(
        host='os.getenv("DB_HOST")',
        user='os.getenv("DB_USER")',
        password='',
        database='os.getenv("DB_NAME")',
        cursorclass=pymysql.cursors.DictCursor
    )

    
    try:
        with connection.cursor() as cursor:
            # Query to get all products with stock information by category
            cursor.execute("""
                SELECT product_id, product_name, product_category, stock_quantity 
                FROM products
                ORDER BY product_category, product_name
            """)
            products = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        products = []
    finally:
        connection.close()

    return render_template('view_stock.html', products=products)


@app.route('/monthly_sales')
def monthly_sales():
    return render_template('monthly_sales.html')


@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/login")
if __name__=="__main__":
    app.run(debug= True,port=4000)
