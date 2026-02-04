import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash


DB_PATH = os.environ.get("DB_PATH") or os.path.join(os.path.dirname(__file__), "patients.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL UNIQUE,
            serial_number TEXT,
            visit_date TEXT,
            name TEXT NOT NULL,
            father_or_husband_name TEXT,
            age INTEGER,
            phone TEXT,
            address TEXT,
            description TEXT
        )
        """
    )
    conn.commit()
    conn.close()


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    # Handle patient creation
    if request.method == "POST" and request.form.get("form_type") == "create":
        return handle_create_patient()

    # Handle search
    query_params = {
        "patient_id": request.args.get("patient_id", "").strip(),
        "name": request.args.get("name", "").strip(),
        "phone": request.args.get("phone", "").strip(),
        "address": request.args.get("address", "").strip(),
    }

    conn = get_db_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM patients WHERE 1=1"
    values = []

    if query_params["patient_id"]:
        sql += " AND patient_id LIKE ?"
        values.append(f"%{query_params['patient_id']}%")
    if query_params["name"]:
        sql += " AND name LIKE ?"
        values.append(f"%{query_params['name']}%")
    if query_params["phone"]:
        sql += " AND phone LIKE ?"
        values.append(f"%{query_params['phone']}%")
    if query_params["address"]:
        sql += " AND address LIKE ?"
        values.append(f"%{query_params['address']}%")

    sql += " ORDER BY id DESC"

    cur.execute(sql, values)
    patients = cur.fetchall()
    conn.close()

    return render_template(
        "index.html",
        patients=patients,
        search=query_params,
        today=datetime.today().strftime("%Y-%m-%d"),
    )


def handle_create_patient():
    patient_id = request.form.get("patient_id", "").strip()
    serial_number = request.form.get("serial_number", "").strip()
    visit_date = request.form.get("visit_date", "").strip()
    name = request.form.get("name", "").strip()
    father_or_husband_name = request.form.get("father_or_husband_name", "").strip()
    age = request.form.get("age", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    description = request.form.get("description", "").strip()

    # Basic validation
    errors = []
    if not patient_id:
        errors.append("Patient ID is required.")
    if not name:
        errors.append("Patient Name is required.")
    if not visit_date:
        errors.append("Date is required.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("index"))

    try:
        age_value = int(age) if age else None
    except ValueError:
        flash("Age must be a number.", "error")
        return redirect(url_for("index"))

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO patients (
                patient_id, serial_number, visit_date, name,
                father_or_husband_name, age, phone, address, description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                serial_number,
                visit_date,
                name,
                father_or_husband_name,
                age_value,
                phone,
                address,
                description,
            ),
        )
        conn.commit()
        flash("Patient created successfully.", "success")
    except sqlite3.IntegrityError:
        flash("Patient ID must be unique.", "error")
    finally:
        conn.close()

    return redirect(url_for("index"))


@app.route("/patients/<int:id>/edit", methods=["GET", "POST"])
def edit_patient(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        return handle_update_patient(id, conn, cur)

    cur.execute("SELECT * FROM patients WHERE id = ?", (id,))
    patient = cur.fetchone()
    conn.close()

    if not patient:
        flash("Patient not found.", "error")
        return redirect(url_for("index"))

    return render_template("edit_patient.html", patient=patient)


def handle_update_patient(id, conn, cur):
    patient_id = request.form.get("patient_id", "").strip()
    serial_number = request.form.get("serial_number", "").strip()
    visit_date = request.form.get("visit_date", "").strip()
    name = request.form.get("name", "").strip()
    father_or_husband_name = request.form.get("father_or_husband_name", "").strip()
    age = request.form.get("age", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    description = request.form.get("description", "").strip()

    errors = []
    if not patient_id:
        errors.append("Patient ID is required.")
    if not name:
        errors.append("Patient Name is required.")
    if not visit_date:
        errors.append("Date is required.")

    if errors:
        for e in errors:
            flash(e, "error")
        conn.close()
        return redirect(url_for("edit_patient", id=id))

    try:
        age_value = int(age) if age else None
    except ValueError:
        flash("Age must be a number.", "error")
        conn.close()
        return redirect(url_for("edit_patient", id=id))

    try:
        cur.execute(
            """
            UPDATE patients
            SET patient_id = ?, serial_number = ?, visit_date = ?, name = ?,
                father_or_husband_name = ?, age = ?, phone = ?, address = ?, description = ?
            WHERE id = ?
            """,
            (
                patient_id,
                serial_number,
                visit_date,
                name,
                father_or_husband_name,
                age_value,
                phone,
                address,
                description,
                id,
            ),
        )
        conn.commit()
        flash("Patient updated successfully.", "success")
    except sqlite3.IntegrityError:
        flash("Patient ID must be unique.", "error")
    finally:
        conn.close()

    return redirect(url_for("index"))


@app.route("/patients/<int:id>/delete", methods=["POST"])
def delete_patient(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id = ?", (id,))
    patient = cur.fetchone()
    if not patient:
        conn.close()
        flash("Patient not found.", "error")
        return redirect(url_for("index"))

    cur.execute("DELETE FROM patients WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Patient deleted successfully.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)

