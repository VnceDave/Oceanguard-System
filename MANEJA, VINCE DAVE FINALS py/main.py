# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import db
import utils
import sqlite3

BG_IMAGE_FILE = "bg.png"
BG_WIDTH = 1000
BG_HEIGHT = 650


class OceanguardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Oceanguard - Marine Waste Reporting System")
        self.geometry(f"{BG_WIDTH}x{BG_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg="#0a1628")

        # Color scheme
        self.PRIMARY_COLOR = "#005B96"
        self.SECONDARY_COLOR = "#03568D"
        self.ACCENT_COLOR = "#00A8E8"
        self.BG_COLOR = "#0a1628"
        self.TEXT_COLOR = "white"

        self.current_user_id = None
        self.bg_photo = None
        try:
            img = Image.open(BG_IMAGE_FILE)
            img = img.resize((BG_WIDTH, BG_HEIGHT), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
        except:
            print("Background image not found!")

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        try:
            # initialize will create DB & tables if needed
            db.initialize()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        self.show_splash()

    # ============ SPLASH SCREEN (START PAGE) ============
    def show_splash(self):
        self.clear_frame()
        self.draw_bg()

        content = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        content.pack(expand=True, fill="both")

        tk.Label(
            content,
            text=" OCEANGUARD ",
            font=("Arial Black", 60, "bold"),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        ).pack(pady=80)

        tk.Label(
            content,
            text="Welcome to Oceanguard",
            font=("Arial", 20, "italic"),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        ).pack(pady=20)

        tk.Label(
            content,
            text="Marine Waste Reporting System",
            font=("Arial", 16),
            fg="#B0B0B0",
            bg=self.BG_COLOR
        ).pack(pady=10)

        btn_style = {
            "bg": self.SECONDARY_COLOR,
            "fg": self.TEXT_COLOR,
            "font": ("Arial", 14, "bold"),
            "activebackground": self.ACCENT_COLOR,
            "activeforeground": self.BG_COLOR,
            "relief": "raised",
            "bd": 2,
            "padx": 40,
            "pady": 15
        }

        tk.Button(content, text="▶ START", width=20, height=2,
                  command=self.show_login, **btn_style).pack(pady=60)

    # ============ LOGIN SCREEN ============
    def show_login(self):
        self.clear_frame()
        self.draw_bg()

        content = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        content.pack(expand=True, fill="both")

        login_box = tk.Frame(content, bg=self.SECONDARY_COLOR, relief="ridge", bd=3)
        login_box.pack(pady=50, padx=100)

        tk.Label(
            login_box,
            text="🔐 LOGIN",
            font=("Arial Black", 28, "bold"),
            fg=self.ACCENT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(pady=20)

        tk.Label(login_box, text="Username:", font=("Arial", 12, "bold"),
                 bg=self.SECONDARY_COLOR, fg=self.ACCENT_COLOR).pack(anchor="w", padx=20, pady=(10, 5))

        self.username_entry = tk.Entry(login_box, width=35, bg="#1a2f4a", fg=self.TEXT_COLOR,
                                       insertbackground=self.ACCENT_COLOR, relief="sunken", bd=2, font=("Arial", 11))
        self.username_entry.pack(padx=20, pady=5, ipady=8)

        tk.Label(login_box, text="Password:", font=("Arial", 12, "bold"),
                 bg=self.SECONDARY_COLOR, fg=self.ACCENT_COLOR).pack(anchor="w", padx=20, pady=(15, 5))

        self.password_entry = tk.Entry(login_box, width=35, show="•", bg="#1a2f4a", fg=self.TEXT_COLOR,
                                       insertbackground=self.ACCENT_COLOR, relief="sunken", bd=2, font=("Arial", 11))
        self.password_entry.pack(padx=20, pady=5, ipady=8)

        def login():
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()

            if not username or not password:
                messagebox.showwarning("Validation", "Please fill in all fields.")
                return

            user_id = db.login_user(username, password)
            if user_id:
                self.current_user_id = user_id
                messagebox.showinfo("Success", f"Welcome, {username}!")
                self.show_home()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        btn_frame = tk.Frame(login_box, bg=self.SECONDARY_COLOR)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="✓ LOGIN", bg=self.ACCENT_COLOR, fg=self.BG_COLOR,
                  width=15, height=2, font=("Arial", 11, "bold"),
                  command=login).pack(side="left", padx=10)

        tk.Button(btn_frame, text="← BACK", bg="#555555", fg=self.TEXT_COLOR,
                  width=15, height=2, font=("Arial", 11, "bold"),
                  command=self.show_splash).pack(side="left", padx=10)

        tk.Label(login_box, text="Don't have an account?", font=("Arial", 10),
                 bg=self.SECONDARY_COLOR, fg="#B0B0B0").pack(pady=(10, 0))

        tk.Button(login_box, text="Sign Up Here", bg=self.SECONDARY_COLOR, fg=self.ACCENT_COLOR,
                  font=("Arial", 10, "bold"), relief="flat", bd=0, cursor="hand2",
                  command=self.show_signup).pack(pady=5)

    # ============ SIGN UP SCREEN ============
    def show_signup(self):
        self.clear_frame()
        self.draw_bg()

        content = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        content.pack(expand=True, fill="both")

        signup_box = tk.Frame(content, bg=self.SECONDARY_COLOR, relief="ridge", bd=3)
        signup_box.pack(pady=50, padx=100)

        tk.Label(
            signup_box,
            text="📝 SIGN UP",
            font=("Arial Black", 28, "bold"),
            fg=self.ACCENT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(pady=20)

        tk.Label(signup_box, text="Username:", font=("Arial", 12, "bold"),
                 bg=self.SECONDARY_COLOR, fg=self.ACCENT_COLOR).pack(anchor="w", padx=20, pady=(10, 5))

        self.new_username_entry = tk.Entry(signup_box, width=35, bg="#1a2f4a", fg=self.TEXT_COLOR,
                                           insertbackground=self.ACCENT_COLOR, relief="sunken", bd=2, font=("Arial", 11))
        self.new_username_entry.pack(padx=20, pady=5, ipady=8)

        tk.Label(signup_box, text="Password:", font=("Arial", 12, "bold"),
                 bg=self.SECONDARY_COLOR, fg=self.ACCENT_COLOR).pack(anchor="w", padx=20, pady=(15, 5))

        self.new_password_entry = tk.Entry(signup_box, width=35, show="•", bg="#1a2f4a", fg=self.TEXT_COLOR,
                                           insertbackground=self.ACCENT_COLOR, relief="sunken", bd=2, font=("Arial", 11))
        self.new_password_entry.pack(padx=20, pady=5, ipady=8)

        tk.Label(signup_box, text="Confirm Password:", font=("Arial", 12, "bold"),
                 bg=self.SECONDARY_COLOR, fg=self.ACCENT_COLOR).pack(anchor="w", padx=20, pady=(15, 5))

        self.confirm_password_entry = tk.Entry(signup_box, width=35, show="•", bg="#1a2f4a", fg=self.TEXT_COLOR,
                                              insertbackground=self.ACCENT_COLOR, relief="sunken", bd=2, font=("Arial", 11))
        self.confirm_password_entry.pack(padx=20, pady=5, ipady=8)

        def register():
            username = self.new_username_entry.get().strip()
            password = self.new_password_entry.get().strip()
            confirm_pw = self.confirm_password_entry.get().strip()

            if not username or not password or not confirm_pw:
                messagebox.showwarning("Validation", "Please fill in all fields.")
                return

            if len(password) < 6:
                messagebox.showwarning("Validation", "Password must be at least 6 characters long.")
                return

            if password != confirm_pw:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            try:
                db.register_user(username, password)
                messagebox.showinfo("Success", "Account created! You can now login.")
                self.show_login()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        btn_frame = tk.Frame(signup_box, bg=self.SECONDARY_COLOR)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="✓ SIGN UP", bg=self.ACCENT_COLOR, fg=self.BG_COLOR,
                  width=15, height=2, font=("Arial", 11, "bold"),
                  command=register).pack(side="left", padx=10)

        tk.Button(btn_frame, text="← BACK", bg="#555555", fg=self.TEXT_COLOR,
                  width=15, height=2, font=("Arial", 11, "bold"),
                  command=self.show_login).pack(side="left", padx=10)

    # ============ HOME SCREEN ============
    def show_home(self):
        self.clear_frame()
        self.draw_bg()

        content = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        content.pack(pady=30, expand=True)

        tk.Label(
            content,
            text="🌊 OCEANGUARD 🌊",
            font=("Arial Black", 48, "bold"),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        ).pack(pady=10)

        tk.Label(
            content,
            text="Marine Waste Reporting System",
            font=("Arial", 18, "italic"),
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        ).pack(pady=5)

        divider = tk.Frame(content, bg=self.ACCENT_COLOR, height=2)
        divider.pack(pady=20, fill="x", padx=100)

        tk.Label(
            content,
            text="Protect Our Oceans • Report Marine Waste • Support SDG 14",
            font=("Arial", 12),
            fg="#B0B0B0",
            bg=self.BG_COLOR
        ).pack(pady=10)

        btn_frame = tk.Frame(content, bg=self.BG_COLOR)
        btn_frame.pack(pady=30)

        btn_style = {
            "bg": self.SECONDARY_COLOR,
            "fg": self.TEXT_COLOR,
            "font": ("Arial", 11, "bold"),
            "activebackground": self.ACCENT_COLOR,
            "activeforeground": self.BG_COLOR,
            "relief": "raised",
            "bd": 2
        }

        tk.Button(btn_frame, text="📝 REPORT WASTE", width=28, height=2,
                  command=self.show_report_form, **btn_style).pack(pady=12)
        tk.Button(btn_frame, text="📋 VIEW RECORDS", width=28, height=2,
                  command=self.show_records, **btn_style).pack(pady=12)
        tk.Button(btn_frame, text="🌍 ABOUT SDG 14", width=28, height=2,
                  command=self.show_sdg, **btn_style).pack(pady=12)
        tk.Button(btn_frame, text="🚪 LOGOUT", width=28, height=2,
                  bg="#D32F2F", fg=self.TEXT_COLOR, font=("Arial", 11, "bold"),
                  activebackground="#FF6B6B", command=self.logout).pack(pady=12)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user_id = None
            self.show_login()

    # ============ REPORT FORM ============
    def show_report_form(self):
        self.clear_frame()
        self.draw_bg()

        header = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        header.pack(fill="x", pady=(20, 10))

        tk.Label(header, text="📝 REPORT WASTE",
                 font=("Arial Black", 28, "bold"), bg=self.BG_COLOR,
                 fg=self.ACCENT_COLOR).pack()

        form = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        form.pack(pady=10, padx=50)

        fields = [
            ("Location:", "location_entry"),
            ("Type of Waste:", "waste_entry"),
            ("Description:", "desc_text"),
            ("Date (MM/DD/YYYY):", "date_entry")
        ]

        entry_style = {"bg": "#1a2f4a", "fg": self.TEXT_COLOR, "insertbackground": self.ACCENT_COLOR,
                       "relief": "sunken", "bd": 2}

        for i, (label_text, var_name) in enumerate(fields):
            tk.Label(form, text=label_text, bg=self.BG_COLOR, fg=self.ACCENT_COLOR,
                     font=("Arial", 11, "bold")).grid(row=i * 2, column=0, sticky="w", pady=5)

            if var_name == "desc_text":
                widget = tk.Text(form, width=45, height=5, **entry_style, font=("Arial", 10))
            else:
                widget = tk.Entry(form, width=45, **entry_style, font=("Arial", 10))

            widget.grid(row=i * 2 + 1, column=0, pady=8, ipady=8)
            setattr(self, var_name, widget)

        btn_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        btn_frame.pack(pady=20)

        btn_common = {"font": ("Arial", 11, "bold"), "width": 15, "height": 2}

        tk.Button(btn_frame, text="✓ SUBMIT", bg=self.ACCENT_COLOR, fg=self.BG_COLOR,
                  command=self.submit_report, **btn_common).pack(side="left", padx=10)
        tk.Button(btn_frame, text="← BACK", bg="#555555", fg=self.TEXT_COLOR,
                  command=self.show_home, **btn_common).pack(side="left", padx=10)

    def submit_report(self):
        loc = self.location_entry.get().strip()
        waste = self.waste_entry.get().strip()
        desc = self.desc_text.get("1.0", tk.END).strip()
        date = self.date_entry.get().strip()

        # validation: date optional
        if not utils.validate(loc, waste, date):
            return messagebox.showwarning("Validation", "Fill required fields correctly. Date must be MM/DD/YYYY if provided.")

        try:
            new_id = db.add_report(loc, waste, desc, date, self.current_user_id)
        except Exception as e:
            return messagebox.showerror("Error", str(e))

        messagebox.showinfo("Success", f"Report submitted (ID: {new_id})")
        # go directly to records so user sees the saved report
        self.show_records()

    # ============ RECORDS LIST ============
    def show_records(self):
        self.clear_frame()
        self.draw_bg()

        header = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        header.pack(fill="x", pady=(20, 10))

        tk.Label(header, text="📋 WASTE RECORDS",
                 font=("Arial Black", 28, "bold"), bg=self.BG_COLOR,
                 fg=self.ACCENT_COLOR).pack()

        table_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1a2f4a", foreground=self.TEXT_COLOR,
                        fieldbackground="#1a2f4a", font=("Arial", 10))
        style.configure("Treeview.Heading", background=self.PRIMARY_COLOR, foreground=self.TEXT_COLOR,
                        font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", self.ACCENT_COLOR)])

        cols = ("ID", "Location", "Waste Type", "User")
        self.table = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)
        self.table.column("ID", width=60, anchor=tk.CENTER)
        self.table.column("Location", width=350, anchor=tk.W)
        self.table.column("Waste Type", width=300, anchor=tk.W)
        self.table.column("User", width=150, anchor=tk.W)

        for col in cols:
            self.table.heading(col, text=col)

        self.table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.config(yscrollcommand=scrollbar.set)

        # Clear any previous rows (if any)
        for i in self.table.get_children():
            self.table.delete(i)

        # Load rows from DB. Be defensive about the returned row shape.
        rows = db.get_all_reports()
        for row in rows:
            # possible row shapes:
            # - (id, location, waste_type, description, date_reported, username)
            # - (id, location, waste_type, description, date_reported, user_id)
            # - (id, location, waste_type, description, date_reported)   <- no user
            try:
                _id = row[0]
                loc = row[1] if len(row) > 1 else "-"
                waste = row[2] if len(row) > 2 else "-"
                # try to obtain username if present
                username = "-"
                if len(row) > 5:
                    possible = row[5]
                    # if the DB returned username already (string), use it
                    if isinstance(possible, str):
                        username = possible
                    else:
                        # user_id given; try to get username from db module if available
                        if hasattr(db, "get_username"):
                            try:
                                uname = db.get_username(possible)
                                username = uname if uname else "-"
                            except Exception:
                                username = "-"
                        else:
                            # fallback: attempt a direct query to users table (best-effort)
                            try:
                                conn = sqlite3.connect(getattr(db, "DB_FILE", "oceanguard.db"))
                                cur = conn.cursor()
                                cur.execute("SELECT username FROM users WHERE id = ?", (possible,))
                                r = cur.fetchone()
                                conn.close()
                                username = r[0] if r else "-"
                            except Exception:
                                username = "-"
                elif len(row) == 5:
                    # no username column returned
                    username = "-"
                else:
                    username = "-"

                self.table.insert("", tk.END, values=(_id, loc, waste, username))
            except Exception:
                # defensive: skip broken row but don't crash UI
                continue

        btn_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        btn_frame.pack(pady=15)

        btn_small = {"width": 12, "height": 2, "font": ("Arial", 10, "bold")}

        tk.Button(btn_frame, text="👁 VIEW", bg=self.ACCENT_COLOR, fg=self.BG_COLOR,
                  command=self.view_record, **btn_small).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="✏ EDIT", bg="#FF9500", fg=self.TEXT_COLOR,
                  command=self.edit_record, **btn_small).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="🗑 DELETE", bg="#D32F2F", fg=self.TEXT_COLOR,
                  command=self.delete_record, **btn_small).grid(row=0, column=2, padx=8)
        tk.Button(btn_frame, text="← BACK", bg="#555555", fg=self.TEXT_COLOR,
                  command=self.show_home, **btn_small).grid(row=0, column=3, padx=8)

    # ============ VIEW RECORD ============
    def view_record(self):
        sel = self.table.selection()
        if not sel:
            return messagebox.showwarning("Warning", "Select a record.")
        record_id = self.table.item(sel[0])["values"][0]

        record = db.get_report(record_id)
        if not record:
            return messagebox.showerror("Error", "Record not found.")

        # record may or may not include username at index 5
        date = record[4] if len(record) > 4 else "-"
        location = record[1] if len(record) > 1 else "-"
        waste_type = record[2] if len(record) > 2 else "-"
        description = record[3] if len(record) > 3 else "-"
        username = record[5] if len(record) > 5 and isinstance(record[5], str) else "-"

        self.clear_frame()
        self.draw_bg()

        header = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        header.pack(fill="x", pady=(20, 10))

        tk.Label(header, text="👁 VIEW RECORD",
                 font=("Arial Black", 28, "bold"), bg=self.BG_COLOR,
                 fg=self.ACCENT_COLOR).pack()

        frame = tk.Frame(self.main_frame, bg=self.SECONDARY_COLOR, relief="ridge", bd=2)
        frame.pack(pady=10, padx=50)

        labels = ["Date:", "Location:", "Waste Type:", "Description:", "User:"]
        values = [date, location, waste_type, description, username]

        for i, (lbl, val) in enumerate(zip(labels, values)):
            tk.Label(frame, text=lbl, font=("Arial", 12, "bold"),
                     bg=self.SECONDARY_COLOR, fg=self.ACCENT_COLOR).grid(row=i, column=0, sticky="nw", pady=10, padx=15)

            if lbl == "Description:":
                txt = tk.Text(frame, width=50, height=8, bg="#1a2f4a", fg=self.TEXT_COLOR,
                               font=("Arial", 10), insertbackground=self.ACCENT_COLOR)
                txt.insert("1.0", val if val else "")
                txt.config(state="disabled")
                txt.grid(row=i, column=1, pady=10, padx=20, sticky="nw")
            else:
                tk.Label(frame, text=val if val else "-", font=("Arial", 11),
                         bg=self.SECONDARY_COLOR, fg=self.TEXT_COLOR).grid(row=i, column=1, sticky="w", padx=20)

        tk.Button(self.main_frame, text="← BACK", bg="#555555", fg=self.TEXT_COLOR,
                  width=15, height=2, font=("Arial", 11, "bold"),
                  command=self.show_records).pack(pady=15)

    # ============ EDIT RECORD ============
    def edit_record(self):
        sel = self.table.selection()
        if not sel:
            return messagebox.showwarning("Warning", "Select a record first.")
        record_id = self.table.item(sel[0])["values"][0]

        record = db.get_report(record_id)
        if not record:
            return messagebox.showerror("Error", "Record not found.")

        # build safe values
        location_val = record[1] if len(record) > 1 else ""
        waste_val = record[2] if len(record) > 2 else ""
        desc_val = record[3] if len(record) > 3 else ""
        date_val = record[4] if len(record) > 4 else ""

        self.clear_frame()
        self.draw_bg()

        header = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        header.pack(fill="x", pady=(20, 10))

        tk.Label(header, text="✏ EDIT RECORD",
                 font=("Arial Black", 28, "bold"), bg=self.BG_COLOR,
                 fg=self.ACCENT_COLOR).pack()

        form = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        form.pack(pady=10, padx=50)

        labels = ["Location:", "Waste Type:", "Description:", "Date:"]
        widgets = []

        entry_style = {"bg": "#1a2f4a", "fg": self.TEXT_COLOR, "insertbackground": self.ACCENT_COLOR,
                       "relief": "sunken", "bd": 2}

        for i, text in enumerate(labels):
            tk.Label(form, text=text, bg=self.BG_COLOR, fg=self.ACCENT_COLOR,
                     font=("Arial", 11, "bold")).grid(row=i * 2, column=0, sticky="w", pady=5)

            if text == "Description:":
                w = tk.Text(form, width=45, height=5, **entry_style, font=("Arial", 10))
                w.insert("1.0", desc_val)
            else:
                w = tk.Entry(form, width=45, **entry_style, font=("Arial", 10))
                if i == 0:
                    w.insert(0, location_val)
                elif i == 1:
                    w.insert(0, waste_val)
                elif i == 3:
                    w.insert(0, date_val)

            w.grid(row=i * 2 + 1, column=0, pady=8, ipady=8)
            widgets.append(w)

        def save():
            loc = widgets[0].get().strip()
            waste = widgets[1].get().strip()
            desc = widgets[2].get("1.0", tk.END).strip()
            date = widgets[3].get().strip()

            if not utils.validate(loc, waste, date):
                return messagebox.showwarning("Validation", "Fill required fields correctly. Date must be MM/DD/YYYY if provided.")

            try:
                db.update_report(record_id, loc, waste, desc, date)
            except Exception as e:
                return messagebox.showerror("Error", str(e))

            messagebox.showinfo("Success", "Record updated!")
            self.show_records()

        btn_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="✓ SAVE", bg=self.ACCENT_COLOR, fg=self.BG_COLOR,
                  width=15, height=2, font=("Arial", 11, "bold"),
                  command=save).pack(side="left", padx=10)
        tk.Button(btn_frame, text="← BACK", bg="#555555", fg=self.TEXT_COLOR,
                  width=15, height=2, font=("Arial", 11, "bold"),
                  command=self.show_records).pack(side="left", padx=10)

    # ============ DELETE RECORD ============
    def delete_record(self):
        sel = self.table.selection()
        if not sel:
            return messagebox.showwarning("Warning", "Select a record first.")
        record_id = self.table.item(sel[0])["values"][0]

        if messagebox.askyesno("Confirm", "Delete this record?"):
            try:
                db.delete_report(record_id)
            except Exception as e:
                return messagebox.showerror("Error", str(e))
            messagebox.showinfo("Deleted", "Record deleted.")
            self.show_records()

    # ============ SDG SCREEN ============
    def show_sdg(self):
        self.clear_frame()
        self.draw_bg()

        header = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        header.pack(fill="x", pady=(20, 10))

        tk.Label(header, text="🌍 ABOUT SDG 14 - LIFE BELOW WATER",
                 font=("Arial Black", 26, "bold"), bg=self.BG_COLOR,
                 fg=self.ACCENT_COLOR).pack()

        text = """
    Sustainable Development Goal 14 focuses on:
    "The conservation and sustainable use of oceans, seas,
    and marine resources for sustainable development."

    Oceanguard supports SDG 14 by:
      • Recording marine waste reports
      • Encouraging public environmental awareness
      • Helping organizations plan cleanup operations
      • Promoting protection of marine biodiversity
    """

        tk.Label(self.main_frame, text=text, font=("Arial", 13),
                 justify="left", bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(
            padx=50, pady=20, fill="both", expand=True)

        tk.Button(self.main_frame, text="← BACK", width=15, height=2,
                  bg="#555555", fg=self.TEXT_COLOR, font=("Arial", 11, "bold"),
                  command=self.show_home).pack(pady=15)

    # ============ HELPERS ============
    def draw_bg(self):
        if self.bg_photo:
            bg = tk.Label(self.main_frame, image=self.bg_photo)
            bg.place(x=0, y=0, relwidth=1, relheight=1)
            bg.image = self.bg_photo

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = OceanguardApp()
    app.mainloop()
