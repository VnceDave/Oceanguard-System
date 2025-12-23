This `README.md` is formatted to provide a professional overview of your project, perfect for a GitHub repository or a project submission.

---

# Oceanguard Waste Reporting System

**Oceanguard** is a specialized desktop application designed for environmental waste reporting, specifically focusing on marine conservation efforts. Built with a modular 3-layer architecture, it allows users to log waste incidents, manage records, and contribute to environmental data tracking.

## 👤 Project Information

* **Developer:** Maneja, Vince Dave C.
* **Course:** IT-2112 (Advanced Computer Programming)
* **Academic Year:** 2025

---

## 🚀 Features

* **Secure Authentication:** User registration and login with SHA-256 password hashing.
* **CRUD Operations:** Create, Read, Update, and Delete waste reports.
* **Data Validation:** Strict input checking for dates (MM/DD/YYYY) and required fields.
* **SDG 14 Integration:** Dedicated section for "Life Below Water" Sustainable Development Goals information.
* **Data Persistence:** Local SQLite database storage for offline reliability.

---

## 🏗️ System Architecture

The application follows a modular architecture to separate concerns and ensure maintainability:

1. **Presentation Layer (`app.py`):** Handles the Tkinter GUI and user events.
2. **Logic Layer (`my_utils.py`):** Performs data validation and business rules.
3. **Data Layer (`db.py`):** Manages SQLite connections and SQL queries.

---

## 📂 Project Structure

```text
Oceanguard/
│── app.py          # Main application entry point & GUI logic
│── db.py           # Database schema and CRUD functions
│── my_utils.py     # Validation and utility functions
│── oceanguard.db   # SQLite database file (generated on first run)
└── bg.png          # UI background assets

```

---

## 🛠️ Module Documentation

### `db.py` — Database Management

Responsible for all interactions with the SQLite database.

* **`initialize()`**: Sets up the `users` and `reports` tables.
* **`hash_password(password)`**: Encrypts user credentials for security.
* **`add_report(...)`**: Saves a new waste entry linked to the logged-in user.
* **`get_all_reports()`**: Fetches all records using SQL JOINS to link reports to usernames.

### `app.py` — User Interface

Built using Python's **Tkinter** library.

* **Navigation:** Uses Frames to switch between Login, Sign Up, Dashboard, and Record View.
* **Components:** Utilizes `TreeView` for displaying report lists and custom dialogs for record deletion.

### `my_utils.py` — Validation

Ensures data integrity before database insertion.

* **`validate(location, waste, date)`**:
* Ensures required fields are not empty.
* Strictly validates the `MM/DD/YYYY` date format.



---

## 🗃️ Database Schema

### `users` Table

| Field | Type | Description |
| --- | --- | --- |
| `id` | INTEGER | Primary Key |
| `username` | TEXT | Unique Username |
| `password` | TEXT | SHA-256 Hashed Password |

### `reports` Table

| Field | Type | Description |
| --- | --- | --- |
| `id` | INTEGER | Primary Key |
| `user_id` | INTEGER | Foreign Key to users.id |
| `location` | TEXT | Waste Location |
| `waste_type` | TEXT | Category of Waste |
| `date_reported` | TEXT | Formatted Date |

---

## 🔧 Installation & Usage

1. **Prerequisites:** Ensure you have Python 3.x installed.
2. **Clone/Download:** Copy the project files to your local machine.
3. **Run Application:**
```bash
python app.py

```


4. **Workflow:**
* Register a new account.
* Login to access the Dashboard.
* Use the "Add New Report" form to submit waste data.
* View or Edit records in the "Waste Records" table.



---

