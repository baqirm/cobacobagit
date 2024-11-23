def tampilkan_laporan(username):
    data_transaksi = database.baca_data_transaksi()
    laporan = "Tanggal\t\tDeskripsi\tNominal\t\tTipe\n"
    laporan += "-" * 50 + "\n"
    saldo = 0

    for t in data_transaksi:
        if t['username'] == username:
            saldo += t['nominal']
            laporan += f"{t['tanggal']}\t{t['deskripsi']}\tRp {abs(t['nominal']):,}\t{t['tipe']}\n"

    laporan += "-" * 50 + "\n"
    laporan += f"Total Saldo: Rp {saldo:,}\n"
    return laporan