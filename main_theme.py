import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# File CSV untuk penyimpanan data
USER_FILE = "users.csv"
TRANSACTION_FILE = "transactions.csv"

# Inisialisasi file CSV jika belum ada
def initialize_files():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "password", "email"])  # Header

def initialize_transaction_file():
    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "type", "description", "amount", "date"])  # Header

# Panggil fungsi untuk inisialisasi
initialize_files()
initialize_transaction_file()

# Fungsi membaca CSV
def read_csv(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)

# Fungsi menulis ke CSV
def write_csv(file_path, data, headers):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
# Fungsi untuk menerapkan tema
def apply_theme(theme):
    if theme == "Default":
        root.configure(bg="#f0f0f0")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="black")
        style.configure("TButton", background="#d9d9d9", foreground="black")
    elif theme == "Dark Mode":
        root.configure(bg="#2c2c2c")
        style.configure("TFrame", background="#2c2c2c")
        style.configure("TLabel", background="#2c2c2c", foreground="white")
        style.configure("TButton", background="#444444", foreground="black")
    elif theme == "Light Mode":
        root.configure(bg="#ffffff")
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="black")
        style.configure("TButton", background="#e0e0e0", foreground="black")
    elif theme == "Coquette Mode":
        root.configure(bg="#FDE8E8")  # Background Utama
        style.configure("TFrame", background="#FFF1F1")  # Background Frame
        style.configure("TLabel", background="#FFF1F1", foreground="#8B5E83")  # Label
        style.configure("TButton", background="#FADADD", foreground="black")  # Button
    elif theme == "Earth Mode":
        root.configure(bg="#D7CCC8")  # Background Utama
        style.configure("TFrame", background="#F5F5F5")  # Background Frame
        style.configure("TLabel", background="#F5F5F5", foreground="#5D4037")  # Label
        style.configure("TButton", background="#A1887F", foreground="black")  # Button
    elif theme == "Sky Mode":
        root.configure(bg="#BBDEFB")  # Background Utama
        style.configure("TFrame", background="#E3F2FD")  # Background Frame
        style.configure("TLabel", background="#E3F2FD", foreground="#0D47A1")  # Label
        style.configure("TButton", background="#64B5F6", foreground="black")  # Button

    # Refresh frame
    clear_frame()
    show_home()
    # Perbarui tampilan
    root.update()

def change_theme(event):
    """Callback untuk mengubah tema saat pengguna memilih tema baru."""
    selected_theme = theme_combobox.get()
    apply_theme(selected_theme)
    show_home()  # Refresh tampilan utama

# Fungsi logout
def logout():
    global current_user
    current_user = None
    show_home()

# Fungsi untuk menampilkan laporan keuangan dalam bentuk tabel
def show_report():
    clear_frame()
    
    ttk.Label(root, text="Laporan Keuangan", font=("Arial", 18)).pack(pady=10)
    
    frame = ttk.Frame(root)
    frame.pack()

    columns = ("type", "description", "amount", "date")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.heading("type", text="Tipe Transaksi")
    tree.heading("description", text="Deskripsi")
    tree.heading("amount", text="Jumlah")
    tree.heading("date", text="Tanggal")
    tree.pack(fill="both", expand=True)

    transactions = read_csv(TRANSACTION_FILE)
    user_transactions = [t for t in transactions if t["username"] == current_user["username"]]

    for transaction in user_transactions:
        tree.insert("", "end", values=(transaction["type"], transaction["description"], transaction["amount"], transaction["date"]))

    ttk.Button(root, text="Kembali", command=show_main_menu).pack(pady=10)

# Fungsi untuk menambah transaksi
def add_transaction():
    def save_transaction():
        t_type = transaction_type.get()
        description = entry_description.get()
        amount = entry_amount.get()
        date = entry_date.get()

        if t_type and description and amount and date:
            try:
                amount = float(amount)
                transactions = read_csv(TRANSACTION_FILE)
                transaction_id = len(transactions) + 1
                transactions.append({
                    "id": transaction_id,
                    "username": current_user["username"],
                    "type": t_type,
                    "description": description,
                    "amount": amount,
                    "date": date
                })
                write_csv(TRANSACTION_FILE, transactions, ["id", "username", "type", "description", "amount", "date"])
                messagebox.showinfo("Success", "Transaksi berhasil disimpan.")
                show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa angka.")
        else:
            messagebox.showerror("Error", "Harap isi semua kolom.")

    clear_frame()
    ttk.Label(root, text="Tambah Transaksi", font=("Arial", 18)).pack(pady=10)

    ttk.Label(root, text="Tipe Transaksi:").pack(pady=5)
    transaction_type = ttk.Combobox(root, values=["Income", "Expense"])
    transaction_type.pack(pady=5)

    ttk.Label(root, text="Deskripsi:").pack(pady=5)
    entry_description = ttk.Entry(root)
    entry_description.pack(pady=5)

    ttk.Label(root, text="Jumlah:").pack(pady=5)
    entry_amount = ttk.Entry(root)
    entry_amount.pack(pady=5)

    ttk.Label(root, text="Tanggal (YYYY-MM-DD):").pack(pady=5)
    entry_date = ttk.Entry(root)
    entry_date.pack(pady=5)

    ttk.Button(root, text="Simpan", command=save_transaction).pack(pady=10)
    ttk.Button(root, text="Kembali", command=show_main_menu).pack(pady=10)

# Fungsi untuk membersihkan frame utama
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Menu utama
def show_main_menu():
    clear_frame()

    ttk.Label(root, text=f"Selamat Datang, {current_user['username']}", font=("Arial", 18)).pack(pady=10)
    ttk.Button(root, text="Tambah Transaksi", command=add_transaction).pack(pady=5)
    ttk.Button(root, text="Lihat Laporan", command=show_report).pack(pady=5)
    ttk.Button(root, text="Logout", command=logout).pack(pady=5)

# Fungsi untuk home
def show_home():
    clear_frame()

    ttk.Label(root, text="Aplikasi Pengelolaan Uang", font=("Arial", 24)).pack(pady=20)
    ttk.Button(root, text="Sign Up", command=sign_up).pack(pady=10)
    ttk.Button(root, text="Sign In", command=sign_in).pack(pady=10)

    ttk.Label(root, text="Pilih Tema", font=("Arial", 18)).pack(pady=10)

    global theme_combobox
    theme_combobox = ttk.Combobox(root, values=["Default", "Dark Mode", "Light Mode", "Earth Mode", "Coquette Mode", "Sky Mode"])
    theme_combobox.set("Default")
    theme_combobox.pack(pady=10)
    theme_combobox.bind("<<ComboboxSelected>>", lambda event: apply_theme(theme_combobox.get()))

    ttk.Button(root, text="Ubah Tema", command=lambda: apply_theme(theme_combobox.get())).pack(pady=10)

# Fungsi sign in
def sign_in():
    def submit_signin():
        username = entry_username.get()
        password = entry_password.get()

        users = read_csv(USER_FILE)
        user = next((u for u in users if u["username"] == username and u["password"] == password), None)

        if user:
            global current_user
            current_user = user
            show_main_menu()
        else:
            messagebox.showerror("Error", "Username atau password salah.")

    clear_frame()
    ttk.Label(root, text="Sign In", font=("Arial", 18)).pack(pady=10)
    ttk.Label(root, text="Username:").pack(pady=5)
    entry_username = ttk.Entry(root)
    entry_username.pack(pady=5)

    ttk.Label(root, text="Password:").pack(pady=5)
    entry_password = ttk.Entry(root, show="*")
    entry_password.pack(pady=5)

    ttk.Button(root, text="Sign In", command=submit_signin).pack(pady=10)
    ttk.Button(root, text="Kembali", command=show_home).pack(pady=10)

# Fungsi sign up
def sign_up():
    def submit_signup():
        username = entry_username.get()
        password = entry_password.get()
        email = entry_email.get()

        if username and password and email:
            users = read_csv(USER_FILE)
            if any(user["username"] == username for user in users):
                messagebox.showerror("Error", "Username sudah terdaftar.")
            elif any(user["email"] == email for user in users):
                messagebox.showerror("Error", "Email sudah terdaftar.")
            else:
                user_id = len(users) + 1
                users.append({"id": user_id, "username": username, "password": password, "email": email})
                write_csv(USER_FILE, users, ["id", "username", "password", "email"])
                messagebox.showinfo("Success", "Registrasi berhasil.")
                show_home()
        else:
            messagebox.showerror("Error", "Harap isi semua kolom.")

    clear_frame()
    ttk.Label(root, text="Sign Up", font=("Arial", 18)).pack(pady=10)

    ttk.Label(root, text="Username:").pack(pady=5)
    entry_username = ttk.Entry(root)
    entry_username.pack(pady=5)

    ttk.Label(root, text="Password:").pack(pady=5)
    entry_password = ttk.Entry(root, show="*")
    entry_password.pack(pady=5)

    ttk.Label(root, text="Email:").pack(pady=5)
    entry_email = ttk.Entry(root)
    entry_email.pack(pady=5)

    ttk.Button(root, text="Register", command=submit_signup).pack(pady=10)
    ttk.Button(root, text="Kembali", command=show_home).pack(pady=10)

# Inisialisasi aplikasi
root = tk.Tk()
root.title("Aplikasi Pengelolaan Uang")
root.geometry("600x400")

# Gaya (Style)
style = ttk.Style()
current_user = None

# Menampilkan halaman awal
show_home()

# Menjalankan aplikasi
root.mainloop()
