import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import users as us
import transactions as ts

current_user = None

# Inisialisasi aplikasi
root = tk.Tk()
root.title("Aplikasi Pengelolaan Uang")
root.geometry("800x600")  

# Membuat Canvas untuk gambar latar
background = tk.Canvas(root, width=800, height=600)
background.place(x=0, y=0, relwidth=1, relheight=1)  # Gunakan place untuk mengisi seluruh area
root.tk.call("lower", background._w) # Pastikan canvas berada di bawah semua elemen

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
    ttk.Label(root, text="Sign In", font=("Arial", 18)).pack(pady=10)
    ttk.Label(root, text="Username:").pack(pady=5)
    entry_username = ttk.Entry(root)
    entry_username.pack(pady=5)

    ttk.Label(root, text="Password:").pack(pady=5)
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
    ttk.Label(root, text="Tambah Transaksi", font=("Arial", 18)).pack(pady=10)

    ttk.Label(root, text="Tipe Transaksi: ").pack(pady=5)
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

    transactions = ts.get_user_transactions(current_user["username"])  # Memanggil fungsi dari modul transactions

    for transaction in transactions:
        tree.insert("", "end", values=(transaction["type"], transaction["description"], transaction["amount"], transaction["date"]))

    ttk.Button(root, text="Kembali", command=show_main_menu).pack(pady=10)

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def show_main_menu():
    clear_frame()

    ttk.Label(root, text=f"Selamat Datang, {current_user['username']}", font=("Arial", 18)).pack(pady=10)
    ttk.Button(root, text="Tambah Transaksi", command=add_transaction_user).pack(pady=5)  # Memanggil add_transaction_user
    ttk.Button(root, text="Lihat Laporan", command=show_report).pack(pady=5)
    ttk.Button(root, text="Logout", command=logout).pack(pady=5)

def show_home():
    clear_frame()

    ttk.Label(root, text="Aplikasi Pengelolaan Uang", font=("Arial", 24)).pack(pady=20)
    ttk.Button(root, text="Sign Up", command=sign_up_user).pack(pady=10)  # Memanggil sign_up_user
    ttk.Button(root, text="Sign In", command=sign_in_user).pack(pady=10)  # Memanggil sign_in_user

    ttk.Label(root, text="Pilih Tema", font=("Arial", 18)).pack(pady=10)

    global theme_combobox
    theme_combobox = ttk.Combobox(root, values=["Default", "Dark Mode", "Light Mode", "Earth Mode", "Coquette Mode", "Sky Mode"])
    theme_combobox.set("Default")
    theme_combobox.pack(pady=10)
    theme_combobox.bind("<<ComboboxSelected>>", lambda event: apply_theme(theme_combobox.get()))

    ttk.Button(root, text="Ubah Tema", command=lambda: apply_theme(theme_combobox.get())).pack(pady=10)

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
    try:
        bg_image = ImageTk.PhotoImage(Image.open(image_path).resize((800, 600)))
        background.create_image(0, 0, anchor="nw", image=bg_image)
        background.image = bg_image  # Simpan referensi gambar untuk mencegah garbage collection
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memuat gambar: {e}")

    theme_colors = {
        "Default": {"fg": "#000", "button_bg": "#4CAF50", "button_fg": "#fff"},
        "Dark Mode": {"fg": "#333", "button_bg": "#5C6BC0", "button_fg": "#fff"},
        "Light Mode": {"fg": "#000", "button_bg": "#03A9F4", "button_fg": "#fff"},
        "Coquette Mode": {"fg": "#3E3E3E", "button_bg": "#E91E63", "button_fg": "#fff"},
        "Earth Mode": {"fg": "#3E3E3E", "button_bg": "#795548", "button_fg": "#fff"},
        "Sky Mode": {"fg": "#1A237E", "button_bg": "#1E88E5", "button_fg": "#fff"},
    }

    colors = theme_colors.get(theme, theme_colors["Default"])
    style.configure("TLabel", foreground=colors["fg"], font=("Arial", 14))
    style.configure("TButton", background=colors["button_bg"], foreground=colors["button_fg"], font=("Arial", 12))

    # Refresh frame
    clear_frame()
    show_home()
    # Perbarui tampilan
    root.update()

# Gaya (Style)
style = ttk.Style()

# Menampilkan halaman awal
show_home()

# Menjalankan aplikasi
root.mainloop() 
