from flask import Flask, request, render_template, redirect, url_for, make_response

app = Flask(__name__)

# Halaman utama, menyimpan cookie
@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    # melakukan set terhadap variabel "username" dengan isi Keanrich
    resp.set_cookie('username', 'Keanrich')  # Cookie disimpan selama 1 hari
    return resp

# Mengambil nilai cookie
@app.route('/get-cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
        return f'Hello, {username}!'
    else:
        return 'No cookie found!'

# Menghapus cookie
@app.route('/delete-cookie')
def delete_cookie():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('username')
    return resp

if __name__ == '__main__':
    app.run(debug=True)