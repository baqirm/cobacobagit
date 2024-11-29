import csv
import os

# File CSV untuk penyimpanan transaksi
TRANSACTION_FILE = "transactions.csv"

def initialize_transaction_file():
    """
    Menginisialisasi file CSV untuk transaksi jika belum ada.
    """
    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "type", "description", "amount", "date"])  # Header

# Panggil fungsi untuk inisialisasi file transaksi
initialize_transaction_file()

def read_transactions():
    """
    Membaca semua transaksi dari file CSV.

    :return: List of dictionaries yang berisi data transaksi
    """
    with open(TRANSACTION_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)  # Mengembalikan list transaksi

def write_transactions(transactions):
    """
    Menulis daftar transaksi ke file CSV.

    :param transactions: List of dictionaries yang berisi data transaksi
    """
    with open(TRANSACTION_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "username", "type", "description", "amount", "date"])
        writer.writeheader()  # Menulis header
        writer.writerows(transactions)  # Menulis semua transaksi

def add_transaction(username, t_type, description, amount, date):
    """
    Menambah transaksi baru ke file CSV.

    :param username: Nama pengguna yang melakukan transaksi
    :param t_type: Tipe transaksi (Income/Expense)
    :param description: Deskripsi transaksi
    :param amount: Jumlah uang yang terlibat dalam transaksi
    :param date: Tanggal transaksi
    """
    transactions = read_transactions()  # Membaca transaksi yang ada
    transaction_id = len(transactions) + 1  # Menghitung ID transaksi baru
    transactions.append({
        "id": transaction_id,
        "username": username,
        "type": t_type,
        "description": description,
        "amount": amount,
        "date": date
    })
    write_transactions(transactions)  # Menyimpan transaksi yang diperbarui

def get_user_transactions(username):
    """
    Mengambil semua transaksi untuk pengguna tertentu.

    :param username: Nama pengguna yang transaksi-nya ingin diambil
    :return: List of dictionaries yang berisi transaksi pengguna
    """
    transactions = read_transactions()  # Membaca semua transaksi
    return [t for t in transactions if t["username"] == username]  # Mengembalikan transaksi yang sesuai
