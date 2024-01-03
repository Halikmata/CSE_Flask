from flask import Flask, make_response, jsonify, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "jhayzkeller9122"
app.config["MYSQL_DB"] = "cse_final"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["SECRET_KEY"] = "29900eb78c15dad2e9d691e4041160d1"

mysql = MySQL(app)

users = {'localhost': 'root'}
#try
def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def home():
    if session.get("username"):
        return redirect(url_for("get_church"))
    return render_template("base.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('get_church'))

    return render_template("base.html", message="Invalid credentials")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/church", methods=["GET"])
def get_church():
    data = data_fetch("""select * from church""")
    return make_response(jsonify(data), 200)


@app.route("/church/<int:id>", methods=["GET"])
def get_player_by_id(id):
    data = data_fetch("""SELECT * FROM church where player_id = {}""".format(id))
    return make_response(jsonify(data), 200)


@app.route("/church", methods=["POST"])
def add_church():
    cur = mysql.connection.cursor()
    info = request.get_json()
    conference_id = info["conference_id"]
    details = info["details"]

    cur.execute(
        """
        INSERT INTO church 
        (conference_id, details) 
        VALUES (%s, %s)
        """,
        (conference_id, details),
    )
    mysql.connection.commit()
    print("row(s) affected: {}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()

    return make_response(
        jsonify(
            {"message": "church added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/church/<int:id>", methods=["PUT"])
def update_church(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    conference_id = info["conference_id"]
    details = info["details"]

    cur.execute(
        """
        UPDATE church 
        SET conference_id = %s, details = %s
        WHERE id = %s
        """,
        (conference_id, details, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(
        jsonify(
            {"message": "church updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )



@app.route("/church/<int:id>", methods=["DELETE"])
def delete_church(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM church WHERE id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(
        jsonify(
            {"message": "church deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
