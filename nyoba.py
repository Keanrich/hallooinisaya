from flask import Flask, render_template, make_response, request, redirect, url_for

app = Flask(__name__)
daftar_nama = ["Keanrich", "Reuben", "Alfandi"]

# Route untuk menampilkan form login
@app.route("/login", methods=["GET"])
def login_form():
    return render_template("form.html")

# Route untuk memproses form login
@app.route("/login", methods=["POST"])
def login():
    username = request.form["name"]
    if username in daftar_nama:
        return redirect(url_for("FN_user/MAIN.html"))
    else:
        return 'Kamu belum sign in. <br><a href="/signup">sign in di sini</a>'
    
@app.route("/signup", methods=["GET"])
def signup_form():
    return render_template("register_site.html")

# Route khusus untuk memproses form sign up dengan POST
@app.route("/signup", methods=["POST"])
def signup():
    new_name = request.form["name"]
    daftar_nama.append(new_name)
    return redirect(url_for("login_form"))

# Route setelah berhasil login
@app.route("/main")
def main_html():
    return render_template("main.html")

if __name__ == "__main__":
    app.run()
