import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import users as us
import transactions as ts
     
def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "Anda berhasil logout")
    show_home()

def sign_up_user():
    def submit_signup():
        username = entry_username.get()
        password = entry_password.get()
        email = entry_email.get()

        if username and password and email:
            result = us.sign_up(username, password, email)
            messagebox.showinfo("Info", result)
            show_home()
        else:
            messagebox.showerror("Error", "Harap isi semua kolom.")
            
    clear_frame()
    ttk.Label(root, text="Sign Up", font=("Obra Letra", 40)).pack(pady=10)

    ttk.Label(root, text="Username:", font=("Obra Letra", 25)).pack(pady=7)
    entry_username = ttk.Entry(root)
    entry_username.pack(pady=5)

    ttk.Label(root, text="Password:", font=("Obra Letra", 25)).pack(pady=7)
    entry_password = ttk.Entry(root, show="*")
    entry_password.pack(pady=5)

    ttk.Label(root, text="Email:", font=("Obra Letra", 25)).pack(pady=7)
    entry_email = ttk.Entry(root)
    entry_email.pack(pady=5)

    ttk.Button(root, text="Register", command=submit_signup).pack(pady=10)
    ttk.Button(root, text="Kembali", command=show_home).pack(pady=10)

def sign_in_user():
    def submit_signin():
        username = entry_username.get()
        password = entry_password.get()

        user = us.sign_in(username, password)
        if isinstance(user, dict):
            global current_user
            current_user = user
            show_main_menu()
        else:
            messagebox.showerror("Error", user)

    clear_frame()
    ttk.Label(root, text="Sign In", font=("Obra Letra", 40)).pack(pady=10)
    ttk.Label(root, text="Username:", font=("Obra Letra", 25)).pack(pady=7)
    entry_username = ttk.Entry(root)
    entry_username.pack(pady=5)

    ttk.Label(root, text="Password:", font=("Obra Letra", 25)).pack(pady=7)
    entry_password = ttk.Entry(root, show="*")
    entry_password.pack(pady=5)
    
    ttk.Button(root, text="Sign In", command=submit_signin).pack(pady=10)
    ttk.Button(root, text="Kembali", command=show_home).pack(pady=10)

def add_transaction_user():
    def save_transaction():
        t_type = transaction_type.get()
        description = entry_description.get()
        amount = entry_amount.get()
        date = entry_date.get()

        if t_type and description and amount and date:
            try:
                amount = float(amount)
                ts.add_transaction(current_user["username"], t_type, description, amount, date)
                messagebox.showinfo("Success", "Transaksi berhasil disimpan.")
                show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa angka.")
        else:
            messagebox.showerror("Error", "Harap isi semua kolom.")
            

    clear_frame()
    ttk.Label(root, text="Tambah Transaksi", font=("Obra Letra", 40)).pack(pady=10)

    ttk.Label(root, text="Tipe Transaksi: ", font=("Obra Letra", 25)).pack(pady=5)
    transaction_type = ttk.Combobox(root, values=["Income", "Expense"])
    transaction_type.pack(pady=5)

    ttk.Label(root, text="Deskripsi:", font=("Obra Letra", 25)).pack(pady=5)
    entry_description = ttk.Entry(root)
    entry_description.pack(pady=5)

    ttk.Label(root, text="Jumlah:", font=("Obra Letra", 25)).pack(pady=5)
    entry_amount = ttk.Entry(root)
    entry_amount.pack(pady=5)

    ttk.Label(root, text="Tanggal (YYYY-MM-DD):", font=("Obra Letra", 25)).pack(pady=5)
    entry_date = ttk.Entry(root)
    entry_date.pack(pady=5)

    ttk.Button(root, text="Simpan", command=save_transaction).pack(pady=10)
    ttk.Button(root, text="Kembali", command=show_main_menu).pack(pady=10)

# Fungsi untuk menampilkan laporan keuangan dalam bentuk tabel
def show_report():
    clear_frame()

    ttk.Label(root, text="Laporan Keuangan", font=("Obra Letra", 45)).pack(pady=10)

    frame = ttk.Frame(root)
    frame.pack()
    
    # Membuat style untuk Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Times New Roman", 12))  # Ganti ukuran font di sini
    style.configure("Treeview.Heading", font=("Times New Roman", 18, "bold"), foreground="blue")  # Ganti ukuran font heading di sini

    columns = ("type", "description", "amount", "date")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.heading("type", text="Tipe Transaksi")
    tree.heading("description", text="Deskripsi")
    tree.heading("amount", text="Jumlah")
    tree.heading("date", text="Tanggal")
    tree.pack(fill="both", expand=True)

    transactions = ts.get_user_transactions(current_user["username"])  # Memanggil fungsi dari modul transactions

    for transaction in transactions:
        tree.insert("", "end", values=(transaction["type"], transaction["description"], transaction["amount"], transaction["date"]))

    # Menghitung dan menampilkan saldo
    total_income, total_expense, total_balance = ts.get_user_balance(current_user["username"])  # Memanggil fungsi dari modul transactions
   
    # Format total_income, total_expense, dan total_balance
    formatted_income = f"{total_income:,.0f}".replace(',', '.')
    formatted_expense = f"{total_expense:,.0f}".replace(',', '.')
    formatted_balance = f"{total_balance:,.0f}".replace(',', '.')
   
    # Validasi total_balance
    if total_balance is None:
        ttk.Label(frame, text="Kesalahan: Total saldo tidak ditemukan.", foreground="orange").pack(pady=10)
    elif not isinstance(total_balance, (int, float)):
        ttk.Label(frame, text="Kesalahan: Total saldo tidak valid.", foreground="orange").pack(pady=10)
    elif total_balance < 0:
        ttk.Label(frame, text="Peringatan: Saldo negatif.", foreground="red").pack(pady=10)
    else:
        # Tampilkan total income, expense, dan balance dengan format yang diinginkan
        ttk.Label(frame, text=f"Total Pemasukan: {formatted_income}", font=("Times New Roman", 16, "bold"), foreground="green").pack(pady=10)
        ttk.Label(frame, text=f"Total Pengeluaran: {formatted_expense}", font=("Times New Roman", 16, "bold"), foreground="purple").pack(pady=10)
        ttk.Label(frame, text=f"Saldo Akhir: {formatted_balance}", font=("Times New Roman", 16, "bold"), foreground="brown").pack(pady=10)
  
    ttk.Button(frame, text="Kembali", command=show_main_menu).pack(pady=10)
    
# Fungsi untuk membersihkan frame utama
def clear_frame():
    for widget in root.winfo_children():
        if widget != background:
            widget.destroy()
            
# Fungsi untuk menerapkan tema
def apply_theme(theme):
    global bg_image  # Simpan referensi gambar latar
    theme_images = {
        "Default": "default.jpg",
        "Dark Mode": "dark_mode.jpeg",
        "Light Mode": "light_mode.jpg",
        "Coquette Mode": "coquette_mode.jpg",
        "Earth Mode": "earth_mode.jpg",
        "Sky Mode": "sky_mode.jpg",
    }

    image_path = theme_images.get(theme, "default.jpg")
    bg_image = ImageTk.PhotoImage(Image.open(image_path).resize((1500, 800)))
    background.create_image(0, 0, anchor="nw", image=bg_image)
    background.image = bg_image  # Simpan referensi gambar untuk mencegah garbage collection

    theme_colors = {
        "Default": {"label_fg": "#000", "button_bg": "#3ecf7d", "button_fg": "#000"},
        "Dark Mode": {"label_fg": "#000", "button_bg": "#75e8fa", "button_fg": "#000"},
        "Light Mode": {"label_fg": "#000", "button_bg": "#c82bd6", "button_fg": "#000"},
        "Coquette Mode": {"label_fg": "#8B5E83", "button_bg": "#96265c", "button_fg": "#000"},
        "Earth Mode": {"label_fg": "#5D4037", "button_bg": "#bd9179", "button_fg": "#000"},
        "Sky Mode": {"label_fg": "#0D47A1", "button_bg": "#0b388c", "button_fg": "#000"},
    }

    colors = theme_colors.get(theme, theme_colors["Default"])
    style.configure("TLabel", foreground=colors["label_fg"], font=("Celandine", 50))
    style.configure("TButton", background=colors["button_bg"], foreground=colors["button_fg"], font=("Obra Letra", 16))
    global button_style
    button_style = colors
    clear_frame()
    show_home()

# Menu utama
def show_main_menu():
    clear_frame()

    ttk.Label(root, text=f"Selamat Datang, {current_user['username']}", font=("Celandine", 52, "bold")).pack(pady=10)
    ttk.Button(root, text="Tambah Transaksi", command=add_transaction_user).pack(pady=5)  # Memanggil add_transaction_user
    ttk.Button(root, text="Laporan Saldo", command=show_report).pack(pady=5)
    ttk.Button(root, text="Logout", command=logout).pack(pady=5)

# Fungsi untuk home
def show_home():
    clear_frame()

    ttk.Label(root, text="Aplikasi Pengelolaan Uang", font=("Celandine", 60, "bold")).pack(pady=20)
    ttk.Button(root, text="Sign Up", command=sign_up_user).pack(pady=10)
    ttk.Button(root, text="Sign In", command=sign_in_user).pack(pady=10) 

    ttk.Label(root, text="Pilih Tema", font=("Obra Letra", 22)).pack(pady=10)

    theme_combobox = ttk.Combobox(root, values=["Default", "Dark Mode", "Light Mode", "Earth Mode", "Coquette Mode", "Sky Mode"], state="readonly")
    theme_combobox.set("Default")
    theme_combobox.pack(pady=10)
    theme_combobox.bind("<<ComboboxSelected>>", lambda event: apply_theme(theme_combobox.get()))

# Inisialisasi aplikasi
root = tk.Tk()
root.title("Aplikasi Pengelolaan Uang")
root.geometry("1600x900")

# Tambahkan canvas untuk latar belakang
background = tk.Canvas(root, width=1600, height=900)
background.place(x=0, y=0, relwidth=1, relheight=1)  # Gunakan place untuk mengisi seluruh area
root.tk.call("lower", background._w) # Pastikan canvas berada di bawah semua elemen

# Gaya (Style)
style = ttk.Style()
button_style = {}

# Komponen tema
theme_combobox = ttk.Combobox(root, values=["Default", "Dark Mode", "Light Mode", "Earth Mode", "Coquette Mode", "Sky Mode"], style="TCombobox")
theme_combobox.set("Default")

# Variabel pengguna
current_user = None

# Menampilkan halaman awal
apply_theme("Default")
show_home()

# Menjalankan aplikasi
try:
    root.mainloop()
except Exception as e:
    print(f"Terjadi kesalahan : {e}")