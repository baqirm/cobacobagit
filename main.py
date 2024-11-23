import tkinter as tk
from tkinter import messagebox
from user_auth import login_user, sign_up_user
from transactions import tambah_transaksi, tampilkan_laporan
# import database

class KeuanganApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengelolaan Keuangan")
        self.root.geometry("400x300")
        self.username = None
        self.halaman_awal()

    def halaman_awal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Selamat Datang", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Login", command=self.halaman_login, width=20).pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.halaman_signup, width=20).pack(pady=5)
        tk.Button(self.root, text="Keluar", command=self.root.quit, width=20).pack(pady=5)

    def halaman_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login_action():
            username = username_entry.get()
            password = password_entry.get()
            if login_user(username, password):
                self.username = username
                messagebox.showinfo("Login Berhasil", "Selamat datang!")
                self.halaman_utama()
            else:
                messagebox.showerror("Login Gagal", "Username atau password salah.")

        tk.Button(self.root, text="Login", command=login_action).pack(pady=5)
        tk.Button(self.root, text="Kembali", command=self.halaman_awal).pack()

    def halaman_signup(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Sign Up", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def signup_action():
            username = username_entry.get()
            password = password_entry.get()
            if sign_up_user(username, password):
                messagebox.showinfo("Sign Up Berhasil", "Silakan login.")
                self.halaman_login()
            else:
                messagebox.showerror("Sign Up Gagal", "Username sudah digunakan.")

        tk.Button(self.root, text="Sign Up", command=signup_action).pack(pady=5)
        tk.Button(self.root, text="Kembali", command=self.halaman_awal).pack()

    def halaman_utama(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Selamat Datang, {self.username}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Tambah Pemasukan", command=lambda: self.halaman_transaksi("Pemasukan")).pack(pady=5)
        tk.Button(self.root, text="Tambah Pengeluaran", command=lambda: self.halaman_transaksi("Pengeluaran")).pack(pady=5)
        tk.Button(self.root, text="Lihat Laporan", command=self.halaman_laporan).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.halaman_awal).pack(pady=5)

    def halaman_transaksi(self, tipe):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Tambah {tipe}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Nominal").pack()
        nominal_entry = tk.Entry(self.root)
        nominal_entry.pack()
        tk.Label(self.root, text="Deskripsi").pack()
        deskripsi_entry = tk.Entry(self.root)
        deskripsi_entry.pack()

        def tambah_action():
            nominal = int(nominal_entry.get())
            deskripsi = deskripsi_entry.get()
            tambah_transaksi(self.username, tipe, nominal, deskripsi)
            messagebox.showinfo("Sukses", f"{tipe} berhasil ditambahkan.")
            self.halaman_utama()

        tk.Button(self.root, text="Simpan", command=tambah_action).pack(pady=5)
        tk.Button(self.root, text="Kembali", command=self.halaman_utama).pack()

    def halaman_laporan(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        laporan = tampilkan_laporan(self.username)

        tk.Label(self.root, text="Laporan Keuangan", font=("Arial", 16)).pack(pady=10)
        text_widget = tk.Text(self.root, height=15, width=50)
        text_widget.pack()
        text_widget.insert(tk.END, laporan)
        text_widget.config(state=tk.DISABLED)

        tk.Button(self.root, text="Kembali", command=self.halaman_utama).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeuanganApp(root)
    root.mainloop()