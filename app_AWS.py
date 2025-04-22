from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector as ms
import os
import datetime

app = Flask("__name__")

app.secret_key = 'T08 /sdk ejfncnsjdi dj875'

app.config['SESSION_TYPE'] = 'filesystem'

UPLOAD_FOLDER = "static/images/dataset_gambar_mobil"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# INITIALIZATION
@app.route("/")
def start_web():
    return render_template("FN_user/login_site.html")

def get_db_connection():
    try:
        conn = ms.connect (
            host='database-1-ken.cnywe662esx7.us-east-1.rds.amazonaws.com',
            user='admin',
            password="Smart321!!",
            database='carrental'
        )
    except ms.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    else:
        return conn
    
def initialization_database():
    try:
        conn = ms.connect (
            host='database-1-ken.cnywe662esx7.us-east-1.rds.amazonaws.com',
            user='admin',
            password="Smart321!!",
        )
    except ms.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")

    database_arr = [db[0] for db in cursor.fetchall()]

    if "carrental" not in database_arr:
        os.system(f"python setup_DB_AWS.py Smart321!!")
    else:
        return f"Database exists"

# USER
@app.route("/login", methods=['POST'])
def login_form():
    username = request.form.get('name')
    password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT password, mode FROM user
        WHERE nama_asli = %s
    """, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        # Check if user's password is according
        if user[0] == password:
            session.permanent = True
            session['username'] = username

            # Handle according to the mode of the user
            if user[1] == 'user':
                return redirect(url_for('main_application'))
            elif user[1] == 'admin':
                return redirect(url_for('main_application_admin'))
            
        else:
            return render_template('FN_user/login_site.html', error=f"Incorrect password. Please try again")
    else:
        return render_template('FN_user/login_site.html', error=f"User not found. Please register first")


@app.route("/Register", methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        new_username = request.form.get('name')
        new_password = request.form.get('password')
        new_email = request.form.get('email')
        new_dob = request.form.get('dob')
        new_sim_number = request.form.get('sim_number')
        mode = 'user'

        if not new_sim_number:
            new_sim_number = ''

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check to see if the username exists or not
        cursor.execute("""
            SELECT * FROM user
            WHERE nama_asli = %s
        """, (new_username,))
        
        existing_user = cursor.fetchone()
        if existing_user and existing_user == new_username:
            return render_template('register_site.html', error="This username has been registered! Choose a different one.")

        cursor.execute("""
            INSERT INTO user (nama_asli, password, email, date_of_birth, sim_nomor, mode, biography)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (new_username, new_password, new_email, new_dob, new_sim_number, mode, ""))

        conn.commit()
        cursor.close()
        conn.close()

        session.permanent = True
        session['username'] = new_username

        return redirect(url_for('start_web'))
    
    return render_template("FN_user/register_site.html")


@app.route("/logout", methods=['GET'])  
def logout_form():
    return render_template('FN_user/logout.html') 

@app.route("/confirm_logout", methods=['POST'])  
def logout():
    session.clear()
    return redirect(url_for('start_web'))


@app.route("/Homepage")
def main_application():
    return render_template("FN_user/MAIN.html")


@app.route("/see_all_car")
def all_car_page ():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Take only with the availability set as True
    cursor.execute("""
        SELECT id, merek, description, filepath FROM mobil
        WHERE availability = True
    """)
    cars = cursor.fetchall()

    cursor.close()
    conn.close()

    # Split them into groups of three
    car_groups_arr = [cars[i:i + 3] for i in range(0, len(cars), 3)]


    return render_template("FN_user/all_car.html", car_groups = car_groups_arr)


@app.route("/Approval")
def approval_page():
    conn = get_db_connection()
    cursor = conn.cursor()

    name = session.get('username')

    cursor.execute("""
        SELECT mobil.merek, mobil.harga, approval.mode, approval.start_date, approval.end_date FROM approval
        JOIN user ON (approval.id_user = user.id)
        JOIN mobil ON (mobil.id = approval.mobil_id)
        WHERE nama_asli = %s AND approval.mode = 'pending'
        ORDER BY approval.start_date DESC
    """, (name,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("FN_user/approval.html", data_arr = data)


@app.route("/History", methods=['GET', 'POST'])
def History_page():
    conn = get_db_connection()
    cursor = conn.cursor()

    name = session.get("username")

    if request.method == 'POST':
        merek = request.form.get("merek")

        cursor.execute("""
            SELECT id FROM mobil
            WHERE merek = %s
        """, (merek,))
        car_id = cursor.fetchone()
        car_id = car_id[0]

        cursor.execute("""
            UPDATE mobil
            SET availability = True 
            WHERE id = %s
        """, (car_id,))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("all_car_page"))

    cursor.execute("""
        SELECT mobil.merek, mobil.harga, approval.mode, approval.start_date, approval.end_date FROM approval
        JOIN user ON (approval.id_user = user.id)
        JOIN mobil ON (mobil.id = approval.mobil_id)
        WHERE nama_asli = %s AND (approval.mode = 'accepted' OR approval.mode = 'rejected')
        ORDER BY approval.start_date DESC
    """, (name,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("FN_user/history.html", data=data)


@app.route("/Profile", methods=['GET', 'POST'])
def profile_page():
    conn = get_db_connection()
    cursor = conn.cursor()

    name = session.get("username")

    if request.method == 'POST':
        new_bio = request.form.get("new-bio")
        
        cursor.execute("""
            UPDATE user
            SET biography = %s
            WHERE nama_asli = %s
        """, (new_bio, name))

        conn.commit()

        return redirect(url_for("profile_page"))

    cursor.execute("""
        SELECT biography FROM user
        WHERE nama_asli = %s
    """, (name,))

    bio = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("FN_user/profile.html", bio = bio)


@app.route("/Rentaling/<int:car_id>", methods=["GET", 'POST'])
def rentaling_page(car_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM mobil
        WHERE id = %s
    """, (car_id, ))
    car = cursor.fetchone()

    if request.method == "POST":
        name = request.form.get("name")
        sim_number = request.form.get('SIM_number')

        cursor.execute("""
            SELECT * FROM user
            WHERE nama_asli = %s and sim_nomor = %s
        """, (name, sim_number))
    
        data = cursor.fetchone()

        if not data:
            error = f"Please enter your name and your SIM number correctly"
            return render_template("FN_user/rentaling.html", error = error, car_data = car)
        
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        cursor.execute("""
            UPDATE mobil
            SET availability = False
            WHERE id = %s
        """, (car[0],))

        cursor.execute("""
            INSERT INTO approval (mode, mobil_id, id_user, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, ('pending', car[0], data[0], start_date, end_date))

        cursor.execute("""
            INSERT INTO history (user_id, nama_asli, tanggal_peminjaman, tanggal_pengembalian, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (data[0], data[1], start_date, end_date, 'pending'))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("approval_page"))


    return render_template("FN_user/rentaling.html", car_data = car)


# ADMIN
@app.route("/HomepageAdmin")
def main_application_admin():
    return render_template("ADMIN_SIDE/ADMIN.html")


@app.route("/see_all_carAdmin")
def all_car_page_admin ():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, merek, description, filepath FROM mobil WHERE availability = True")

    cars = cursor.fetchall()

    cursor.close()
    conn.close()

    # Split them into groups of three
    car_groups_arr = [cars[i:i + 3] for i in range(0, len(cars), 3)]

    return render_template("ADMIN_SIDE/ALL_CAR_ADMIN.html", cars=car_groups_arr)


@app.route("/ApprovalAdmin", methods=['GET', 'POST'])
def approval_page_admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        approval_id = request.form.get("approval_id")
        car_merek = request.form.get('car_merek')
        action = request.form.get('action')

        if action == "accept":
            new_mode = "accepted"
            
            cursor.execute("""
                UPDATE mobil
                SET availability = False
                WHERE merek = %s
            """, (car_merek,))

            cursor.execute("""
                SELECT id_user FROM approval
                WHERE approval_id = %s
            """, (approval_id,))
            user_id = cursor.fetchone()
            user_id = user_id[0]

            cursor.execute("""
                UPDATE history
                SET status = 'accepted'
                WHERE user_id = %s
            """, (user_id,))
            conn.commit()

        elif action == "reject":
            new_mode = "rejected"

            cursor.execute("""
                UPDATE mobil
                SET availability = True
                WHERE merek = %s
            """, (car_merek,))

            cursor.execute("""
                SELECT id_user FROM approval
                WHERE approval_id = %s
            """, (approval_id,))
            user_id = cursor.fetchone()
            user_id = user_id[0]

            cursor.execute("""
                UPDATE history
                SET status = 'rejected'
                WHERE user_id = %s
            """, (user_id,))

            conn.commit()

        cursor.execute("""
            UPDATE approval
            SET mode = %s
            WHERE approval_id = %s
        """, (new_mode, approval_id))

        conn.commit()

        cursor.execute("""
            SELECT id FROM user
            WHERE nama_asli = %s
        """, (session.get("username"),))
        user_id = cursor.fetchone()

        obj_to_add = f"Car with merek {car_merek} approval request is {new_mode}"

        cursor.execute("""
            INSERT INTO log (user_id, activity, obj)
            VALUES (%s, %s, %s)
        """, (user_id[0], action, obj_to_add))

        conn.commit()
        cursor.close()
        conn.close()

        flash(f"Request {approval_id} has been {new_mode}!", "success")

        return redirect(url_for("all_car_page_admin"))

    cursor.execute(
        """
        SELECT approval.approval_id, mobil.merek, mobil.description, approval.start_date, approval.end_date
        FROM approval
        JOIN mobil ON approval.mobil_id = mobil.id
        WHERE approval.mode = 'pending'
        """
    )
    requests = cursor.fetchall()

    return render_template("ADMIN_SIDE/APPROVAL_REQUEST.html", requests=requests)


@app.route("/HistoryAdmin")
def History_page_admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT log.log_id, user.nama_asli, log.activity, log.date_changed, log.obj
        FROM log
        JOIN user on (log.user_id = user.id)
    """)
    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("ADMIN_SIDE/VIEW_LOG_CHANGE.html", history=history)


@app.route("/add", methods=['GET', 'POST'])
def add_page():
    if request.method == 'POST':
        nomor_plat = request.form.get("nomor_plat")
        merek = request.form.get('merek')
        jenis = request.form.get('jenis')
        harga = request.form.get('harga')
        stnk = request.form.get('stnk')
        car_desc = request.form.get('car_desc')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check to see if the nomor_plat and the STNK exists or not
        cursor.execute("""
            SELECT merek, stnk FROM mobil
            WHERE nomor_plat = %s AND stnk = %s
        """, (nomor_plat, stnk))
        data = cursor.fetchone()

        if data:
            return render_template('ADMIN_SIDE/ADD.html', error = f"There is a car with the registered plate number and STNK. Please check the details again!")

        file_img = request.files.get('car_image')
        filename = f"{merek.replace(' ', '_').capitalize()}.jpeg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_img.save(filepath)

        db_filepath = f"images/dataset_gambar_mobil/{filename}"

        cursor.execute("""
            INSERT INTO mobil (nomor_plat, merek, availability, jenis, harga, stnk, description, filepath)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nomor_plat, merek, True, jenis, harga, stnk, car_desc, db_filepath))

        conn.commit()

        cursor.execute("""
            SELECT id FROM user
            WHERE nama_asli = %s
        """, (session.get("username"),))
        user_id = cursor.fetchone()

        obj_to_add = f"Car with merek {merek} and plate number {nomor_plat}"

        cursor.execute("""
            INSERT INTO log (user_id, activity, obj)
            VALUES (%s, %s, %s)
        """, (user_id[0], 'add', obj_to_add))

        conn.commit()
        cursor.close()
        conn.close()

        flash(f"Car '{merek}' has been successfully added!", "success")

        return redirect(url_for('all_car_page_admin'))
    

    return render_template("ADMIN_SIDE/ADD.html")


@app.route("/delete", methods=['GET', 'POST'])
def delete_page():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        merek = request.form.get("delete_vehicle")

        cursor.execute("SELECT id FROM mobil WHERE merek = %s", (merek,))
        car_id = cursor.fetchone()
        car_id = car_id[0]

        cursor.execute("DELETE FROM approval WHERE mobil_id = %s", (car_id,))
        
        cursor.execute("DELETE FROM mobil WHERE merek = %s", (merek,))

        cursor.execute("""
            SELECT id FROM user
            WHERE nama_asli = %s
        """, (session.get("username"),))
        user_id = cursor.fetchone()
        
        obj_to_add = f"Car with merek {merek}"

        cursor.execute("""
            INSERT INTO log (user_id, activity, obj)
            VALUES (%s, %s, %s)
        """, (user_id[0], 'delete', obj_to_add))

        conn.commit()
        cursor.close()
        conn.close()

        flash(f"Car '{merek}' has been successfully deleted!", "success")

        return redirect(url_for('all_car_page_admin'))
    
    cursor.execute("""
        SELECT merek FROM mobil
    """)
    data = cursor.fetchall()

    conn.close()
    cursor.close()

    return render_template("ADMIN_SIDE/DELETE.html", data=data)


@app.route("/update", methods=['GET', 'POST'])
def update_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        target_car = request.form.get('update_vehicle')

        # Fetch existing values
        cursor.execute("""
            SELECT id, merek, jenis, harga, stnk, description 
            FROM mobil WHERE merek = %s
        """, (target_car,))
        car = cursor.fetchone()
    
        car_id = car[0]

        new_merek = request.form.get('update_merek') or car[1]
        new_jenis = request.form.get('update_jenis') or car[2]
        new_harga = request.form.get('update_harga') or car[3]
        new_stnk = request.form.get('update_STNK') or car[4]
        new_desc = request.form.get('update_desc') or car[5]

        cursor.execute("""
            UPDATE mobil
            SET merek = %s, jenis = %s, harga = %s, stnk = %s, description = %s
            WHERE id = %s
        """, (new_merek, new_jenis, new_harga, new_stnk, new_desc, car_id))

        cursor.execute("""
            SELECT id FROM user
            WHERE nama_asli = %s
        """, (session.get("username"),))
        user_id = cursor.fetchone()
        
        obj_to_add = f"Car with merek {target_car} to {new_merek}"

        cursor.execute("""
            INSERT INTO log (user_id, activity, obj)
            VALUES (%s, %s, %s)
        """, (user_id[0], 'update', obj_to_add))

        conn.commit()
        cursor.close()
        conn.close()

        flash(f"The car {target_car} has been updated to {new_merek}")

        return redirect(url_for('all_car_page_admin'))
    
    cursor.execute("""
        SELECT merek FROM mobil
    """)
    data = cursor.fetchall()

    conn.close()
    cursor.close()

    return render_template("ADMIN_SIDE/UPDATE.html", data=data)




if __name__ == "__main__":

    result = initialization_database()
    print(result)
            
    app.run()
