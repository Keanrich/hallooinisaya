from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)


def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Smart321!!"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS students")
    conn.commit()
    cursor.close()
    conn.close()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(255),
            NIM VARCHAR(255),
            date_of_birth DATE
        )
    ''')

    # cursor.execute("select * from user")

    conn.commit()
    cursor.close()
    conn.close()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Smart321!!",  # ganti jika berbeda
        database="students"
    )

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nama = request.form.get("nama")
        nim = request.form.get("nim")
        dob = request.form.get("dob")  # format: YYYY-MM-DD

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO user (nama, NIM, date_of_birth) VALUES (%s, %s, %s)"
        val = (nama, nim, dob)
        cursor.execute(sql, val)

        conn.commit()
        cursor.close()
        conn.close()

        return render_template("terimakasih.html")

    return render_template("form_lab.html")

@app.route("/load", methods=["GET", "POST"])
def mahasiswa():
    if request.method == "POST":
        nim = request.form.get("nim")
        nama_baru = request.form.get("nama")
        dob_baru = request.form.get("dob")

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "UPDATE user SET nama = %s, date_of_birth = %s WHERE NIM = %s"
        val = (nama_baru, dob_baru, nim)
        cursor.execute(sql, val)

        conn.commit()
        cursor.close()
        conn.close()

        return render_template("terimakasih.html")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("select * from user")
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    return render_template("form_lab.html", data=data)


@app.route("/delete", methods=["POST"])
def delete_mahasiswa():
    nim = request.form.get("nim")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM user WHERE NIM = %s", (nim,))

    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for("mahasiswa"))



if __name__ == '__main__':
    create_database()
    init_db()  
    app.run(debug=True)
