import csv
import os

# File CSV untuk penyimpanan transaksi
TRANSACTION_FILE = "transactions.csv"

# Menginisialisasi file CSV untuk transaksi jika belum ada.
def initialize_transaction_file():
    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "type", "description", "amount", "date"])  # Header

# Panggil fungsi untuk inisialisasi file transaksi
initialize_transaction_file()

def read_transactions():
    with open(TRANSACTION_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)  # Mengembalikan list transaksi

def write_transactions(transactions):
    with open(TRANSACTION_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "username", "type", "description", "amount", "date"])
        writer.writeheader()  # Menulis header
        writer.writerows(transactions)  # Menulis semua transaksi

def add_transaction(username, t_type, description, amount, date):
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
    transactions = read_transactions()  # Membaca semua transaksi
    return [t for t in transactions if t["username"] == username]  # Mengembalikan transaksi yang sesuai

def get_user_balance(username):
    transactions = get_user_transactions(username)
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        amount =float(transaction["amount"])
        if transaction["type"] == "Income":
            total_income += amount
        elif transaction["type"] == "Expense":
            total_expense += amount
            
    total_balance = total_income - total_expense
    return total_income, total_expense, total_balance