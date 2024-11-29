import csv
import os

# File CSV untuk penyimpanan data pengguna
USER_FILE = "users.csv"

def initialize_user_file():
    """
    Menginisialisasi file CSV untuk pengguna jika belum ada.
    """
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "password", "email"])  # Header untuk file pengguna

# Panggil fungsi untuk inisialisasi file pengguna
initialize_user_file()

def read_users():
    """
    Membaca semua pengguna dari file CSV.

    :return: List of dictionaries yang berisi data pengguna
    """
    with open(USER_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)  # Mengembalikan list pengguna

def write_users(users):
    """
    Menulis daftar pengguna ke file CSV.

    :param users: List of dictionaries yang berisi data pengguna
    """
    with open(USER_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "username", "password", "email"])
        writer.writeheader()  # Menulis header
        writer.writerows(users)  # Menulis semua pengguna

def sign_up(username, password, email):
    """
    Fungsi untuk mendaftarkan pengguna baru.

    :param username: Nama pengguna yang ingin didaftarkan
    :param password: Kata sandi untuk akun pengguna
    :param email: Alamat email pengguna
    :return: Pesan konfirmasi tentang hasil pendaftaran
    """
    users = read_users()  # Membaca pengguna yang ada
    # Memeriksa apakah username sudah ada
    if any(user["username"] == username for user in users):
        return "Username sudah terdaftar."

    # Memeriksa apakah email sudah ada
    if any(user["email"] == email for user in users):
        return "Email sudah terdaftar."

    # Menambahkan pengguna baru ke daftar
    user_id = len(users) + 1  # Menghitung ID pengguna baru
    users.append({
        "id": user_id,
        "username": username,
        "password": password,  # Dalam aplikasi nyata, kata sandi harus dienkripsi
        "email": email
    })
    write_users(users)  # Menyimpan pengguna baru ke file
    return "Registrasi berhasil!"

def sign_in(username, password):
    """
    Fungsi untuk masuk ke akun pengguna.

    :param username: Nama pengguna yang ingin login
    :param password: Kata sandi untuk akun pengguna
    :return: Informasi pengguna jika login berhasil, atau pesan kesalahan jika gagal
    """
    users = read_users()  # Membaca semua pengguna
    # Mencari pengguna berdasarkan username
    for user in users:
        if user["username"] == username:
            if user["password"] == password:  # Memeriksa kecocokan kata sandi
                return user  # Mengembalikan informasi pengguna jika login berhasil
            else:
                return "Kata sandi salah."  # Pesan kesalahan jika kata sandi salah
    return "Username tidak ditemukan."  # Pesan kesalahan jika username tidak ada

def get_all_users():
    """
    Mengambil semua pengguna yang terdaftar.

    :return: Daftar semua pengguna
    """
    return read_users()  # Mengembalikan daftar pengguna
