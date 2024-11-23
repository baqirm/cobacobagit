def login_user(username, password):
    data_pengguna = database.baca_data_pengguna()
    for pengguna in data_pengguna:
        if pengguna['username'] == username and pengguna['password'] == password:
            return True
    return False

def sign_up_user(username, password):
    data_pengguna = database.baca_data_pengguna()
    for pengguna in data_pengguna:
        if pengguna['username'] == username:
            return False
    database.tambah_pengguna(username, password)
    return True