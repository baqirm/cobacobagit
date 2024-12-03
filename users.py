import csv
import os

# File CSV untuk penyimpanan data pengguna
USER_FILE = "users.csv"

# Menginisialisasi file CSV untuk pengguna jika belum ada.
def initialize_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "password", "email"])  # Header untuk file pengguna

# Panggil fungsi untuk inisialisasi file pengguna
initialize_user_file()

def read_users():
    with open(USER_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)  # Mengembalikan list pengguna

def write_users(users):
    with open(USER_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "username", "password", "email"])
        writer.writeheader()  # Menulis header
        writer.writerows(users)  # Menulis semua pengguna

def sign_up(username, password, email):
    users = read_users()  # Membaca pengguna yang ada
    if any(user["username"] == username for user in users):
        return "Username sudah terdaftar."

    if any(user["email"] == email for user in users):
        return "Email sudah terdaftar."

    # Menambahkan pengguna baru ke daftar
    user_id = len(users) + 1  # Menghitung ID pengguna baru
    users.append({
        "id": user_id,
        "username": username,
        "password": password, 
        "email": email
    })
    write_users(users)  # Menyimpan pengguna baru ke file
    return "Registrasi berhasil!"

def sign_in(username, password):
    users = read_users()  # Membaca semua pengguna
    for user in users:
        if user["username"] == username:
            if user["password"] == password: 
                return user  # Mengembalikan informasi pengguna jika login berhasil
            else:
                return "Kata sandi salah."
    return "Username tidak ditemukan."

def get_all_users():
    return read_users()  # Mengembalikan daftar pengguna
