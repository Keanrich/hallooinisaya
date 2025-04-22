from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Digunakan untuk mengenkripsi session

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return f'Halo, {username}! <br><a href="/logout">Logout</a>'
    return 'Kamu belum login. <br><a href="/login">Login di sini</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():     
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p>Masukkan Username:</p>
            <input type="text" name="username">
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
