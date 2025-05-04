import tkinter as tk
from tkinter import messagebox
import pyodbc

class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy System")

        self.conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=ABUOELHASSAN\\SQLEXPRESS;"
            "DATABASE=PharmacySystem;"
            "UID=sa;"
            "PWD=My1052004;"
            "TrustServerCertificate=yes;"
            "Connection Timeout=30;"
            "Encrypt=yes;"
        )

        # شاشة تسجيل الدخول
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=5, pady=5)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Entry(self.root, textvariable=self.username_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill all fields!")
            return

        try:
            connection = pyodbc.connect(self.conn_str)
            cursor = connection.cursor()

            # تحقق من المسؤولين
            cursor.execute("SELECT * FROM Admins WHERE Username = ? AND Password = ?", (username, password))
            admin = cursor.fetchone()
            if admin:
                self.show_admin_screen()
                cursor.close()
                connection.close()
                return

            # تحقق من المرضى
            cursor.execute("SELECT * FROM Patients WHERE Username = ? AND Password = ?", (username, password))
            patient = cursor.fetchone()
            if patient:
                self.show_patient_screen()
                cursor.close()
                connection.close()
                return

            messagebox.showerror("Login Failed", "Invalid username or password!")
            cursor.close()
            connection.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_admin_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Dashboard").grid(row=0, column=0, columnspan=2, pady=10)

        # إضافة صيدلية
        tk.Label(self.root, text="Add Pharmacy").grid(row=1, column=0, columnspan=2)
        tk.Label(self.root, text="Name:").grid(row=2, column=0)
        tk.Label(self.root, text="Address:").grid(row=3, column=0)
        tk.Label(self.root, text="Phone:").grid(row=4, column=0)

        self.pharmacy_name_var = tk.StringVar()
        self.pharmacy_address_var = tk.StringVar()
        self.pharmacy_phone_var = tk.StringVar()

        tk.Entry(self.root, textvariable=self.pharmacy_name_var).grid(row=2, column=1)
        tk.Entry(self.root, textvariable=self.pharmacy_address_var).grid(row=3, column=1)
        tk.Entry(self.root, textvariable=self.pharmacy_phone_var).grid(row=4, column=1)

        tk.Button(self.root, text="Add Pharmacy", command=self.add_pharmacy).grid(row=5, column=0, columnspan=2, pady=5)

        # إضافة دواء
        tk.Label(self.root, text="Add Medicine").grid(row=6, column=0, columnspan=2)
        tk.Label(self.root, text="Medicine Name:").grid(row=7, column=0)
        tk.Label(self.root, text="Pharmacy ID:").grid(row=8, column=0)
        tk.Label(self.root, text="Available:").grid(row=9, column=0)

        self.medicine_name_var = tk.StringVar()
        self.medicine_pharmacy_id_var = tk.StringVar()
        self.medicine_available_var = tk.BooleanVar()

        tk.Entry(self.root, textvariable=self.medicine_name_var).grid(row=7, column=1)
        tk.Entry(self.root, textvariable=self.medicine_pharmacy_id_var).grid(row=8, column=1)
        tk.Checkbutton(self.root, variable=self.medicine_available_var).grid(row=9, column=1)

        tk.Button(self.root, text="Add Medicine", command=self.add_medicine).grid(row=10, column=0, columnspan=2, pady=5)

    def add_pharmacy(self):
        name = self.pharmacy_name_var.get()
        address = self.pharmacy_address_var.get()
        phone = self.pharmacy_phone_var.get()

        if name and address:
            try:
                connection = pyodbc.connect(self.conn_str)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO Pharmacies (Name, Address, Phone) VALUES (?, ?, ?)",
                    (name, address, phone)
                )
                connection.commit()
                messagebox.showinfo("Success", "Pharmacy added successfully!")
                cursor.close()
                connection.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill Name and Address!")

    def add_medicine(self):
        name = self.medicine_name_var.get()
        pharmacy_id = self.medicine_pharmacy_id_var.get()
        available = self.medicine_available_var.get()

        if name:
            try:
                connection = pyodbc.connect(self.conn_str)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO Medicines (Name, PharmacyID, Available) VALUES (?, ?, ?)",
                    (name, int(pharmacy_id) if pharmacy_id else None, 1 if available else 0)
                )
                connection.commit()
                messagebox.showinfo("Success", "Medicine added successfully!")
                cursor.close()
                connection.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill Medicine Name!")

    def show_patient_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Patient Dashboard").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="Medicine Name:").grid(row=1, column=0, padx=5, pady=5)
        self.search_medicine_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.search_medicine_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Search Medicine", command=self.search_medicine).grid(row=2, column=0, columnspan=2, pady=5)

        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def search_medicine(self):
        medicine_name = self.search_medicine_var.get()
        if not medicine_name:
            messagebox.showwarning("Input Error", "Please enter a medicine name!")
            return

        try:
            connection = pyodbc.connect(self.conn_str)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT m.Name, m.Available, p.Name AS PharmacyName, p.Address
                FROM Medicines m
                LEFT JOIN Pharmacies p ON m.PharmacyID = p.PharmacyID
                WHERE m.Name LIKE ?
                """,
                (f"%{medicine_name}%",)
            )
            rows = cursor.fetchall()
            self.result_text.delete(1.0, tk.END)

            if not rows:
                self.result_text.insert(tk.END, "Medicine not found!\n")
            else:
                for row in rows:
                    if row.Available:
                        self.result_text.insert(tk.END, f"Medicine: {row.Name}\nAvailable: Yes\nPharmacy: {row.PharmacyName}\nAddress: {row.Address}\n\n")
                    else:
                        self.result_text.insert(tk.END, f"Medicine: {row.Name}\nAvailable: No\n\n")
            cursor.close()
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()