# from flask import Flask
# from datetime import datetime  # Tambahkan import ini

# app = Flask(name)

# @app.route('/')  
# def index():
#     now = datetime.now()
#     current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Format waktu
#     return f"This is an index page. Current time: {current_time}"

# @app.route('/hello')
# def hello():
#     return "Hello, Platform Based 2024"

# if name == 'main':
#     app.run(debug=True)

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("main.html")

@app.route('/init-registration')
def init_registration():
    return render_template('form.html')

@app.route('/register',methods=['get'])
def register():
    firstName = request.args.get('first_name')
    lastName = request.args.get('last_name')
    fullName = f"{firstName} {lastName}"
    return f"Registration Approved! {fullName}"

if __name__ == "__main__":
    app.run(debug=True)


# perlu menjalankan cmd: python [nama_python] pastikan nama folder