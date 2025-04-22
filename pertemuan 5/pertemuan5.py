from flask import Flask, render_template, request
app = Flask(__name__)

class student:
    def __init__(self, name, NIM):
        self.name = name
        self.id = NIM


# @app.route("/students")
# def displayStudents ():
#     student_list = []
#     student_list.append(student("keanrich", "001"))
#     student_list.append(student("alfandi", "002"))
#     student_list.append(student("brian", "003"))
#     student_list.append(student("Devlin", "003"))
#     student_list.append(student("rendi", "003"))

#     return render_template("students.html", students=student_list)


## pakai post memasukan data dari html ke server
@app.route('/')
def form():
    return '''
        <form action="/submit" method="post">
            Nama: <input type="text" name="name"><br>
            Umur: <input type="number" name="age"><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    age = request.form.get('age')
    data = [name, age]
    student_list = []
    student_list.append(student("keanrich", "001"))
    student_list.append(student("alfandi", "002"))
    student_list.append(student("brian", "003"))
    student_list.append(student("Devlin", "003"))
    student_list.append(student("rendi", "003"))

    return render_template("students.html", students=student_list, user=data)

if __name__ == "__main__":
    app.run() 
