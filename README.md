# Patient Management System (Web App)

This is a simple **Patient Management System** built with **Python (Flask) + SQLite**. It provides basic CRUD operations and a clean, responsive UI for managing patients.

## Features

- **Patient Search & Management**
  - Search patients by **Patient ID**, **Patient Name**, **Phone Number**, or **Address**
  - Results shown in a table with all key details
  - Each row has **Edit** and **Delete** actions
  - Delete uses a **confirmation dialog** and removes the record permanently

- **Add New Patient**
  - Form fields:
    - Patient ID (unique)
    - Serial Number
    - Date
    - Patient Name
    - Father/Husband Name
    - Age
    - Phone Number
    - Address
    - Description / Medical Notes
  - Required validation for **Patient ID**, **Patient Name**, and **Date**

- **Database**
  - Uses **SQLite** (`patients.db` created automatically on first run)
  - `patients` table with:
    - `id` (auto-increment primary key)
    - `patient_id` (unique, required)
    - `serial_number`
    - `visit_date`
    - `name` (required)
    - `father_or_husband_name`
    - `age`
    - `phone`
    - `address`
    - `description`

## Tech Stack

- **Backend / Web Framework**: Flask (Python)
- **Database**: SQLite (via Python `sqlite3` standard library)
- **Templating**: Jinja2 (bundled with Flask)
- **UI**: Server-rendered HTML + CSS

## Project Structure

- `backend/`
  - `app.py` — main Flask application
  - `requirements.txt` — Python dependencies
  - `patients.db` — SQLite database file (auto-created)
  - `templates/`
    - `base.html` — layout
    - `index.html` — search, add form, patient list
    - `edit_patient.html` — edit form
  - `static/`
    - `styles.css` — basic modern styling

## How to Run

1. **Install Python 3** (if not already installed).

2. Open a terminal in the project directory:

```bash
cd backend
```

3. (Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

5. **Run the app**:

```bash
python app.py
```

6. Open your browser and go to:

```text
http://localhost:5000
```

## Usage Notes

- The database and table are created automatically on first request.
- **Patient ID** must be unique; trying to reuse it will show a validation error.
- Search filters are optional; you can combine any of them or leave them empty to see all patients.
- Edit and Delete actions are available in the patients table for quick management.

