from flask import Flask, render_template, request, redirect, url_for
from database import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return redirect(url_for("students"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        course = request.form.get("course")

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO students (name, email, phone, course)
            VALUES (%s, %s, %s, %s)
        """

        values = (name, email, phone, course)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("students"))

    return render_template("register.html")


@app.route("/students")
def students():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("students.html", students=students)


@app.route("/delete/<int:id>")
def delete_student(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("students"))


if __name__ == "__main__":
    app.run(debug=True)