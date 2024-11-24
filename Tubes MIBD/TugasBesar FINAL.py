import pyodbc
import os
import datetime

"""
    KODE KONEKSI TABEL MS SQL KE PYTHON
    
    ANGGOTA KELOMPOK :
        Axel Darmaputra             - Teknik Informatika            - 6182201053
        Nazarene Bena Elohim        - Teknik Informatika            - 6182201075
        Fauzan Rhamzy               - Teknik Informatika            - 6182201081
        Jason Kelvin Agung          - Teknik Informatika            - 6182201082
"""

# Fungsi untuk membuat koneksi ke database
def create_connection():
    server = 'LAPTOP-KJFFUFJB\\SQLEXPRESS'
    database = 'TugasBesar'
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
    conn = pyodbc.connect(conn_str)
    print("Koneksi berhasil!")
    return conn

# ------------------------------ DML QUERIES ------------------------------ #
# Fungsi untuk menambahkan pengguna
def add_pengguna(conn, nama, email, username, password, peran, telp, alamat, kelurahan):
    try:
        cursor = conn.cursor()

        # cari id dari nama kelurahan yang dimasukkan
        cursor.execute('''
            SELECT id_kelurahan FROM Kelurahan WHERE nama = ?
        ''', (kelurahan,))
        result = cursor.fetchone()

        # jika nama kelurahan ada, maka masukkan ke dalam tabel
        if result:
            id_kelurahan = result[0]
            cursor.execute('''
                INSERT INTO Pengguna (nama, email, username, password, peran, no_telp, alamat, id_kelurahan)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nama, email, username, password, peran, telp, alamat, id_kelurahan))
            conn.commit()
            print("Pengguna berhasil ditambahkan.")
        # jika tidak ada, berikan pesan bahwa nama kelurahan tersebut tidak ada
        else:
            print(f"Kelurahan dengan nama '{kelurahan}' tidak ditemukan.")
        
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk menambahkan rekord Sampah
def add_sampah(conn, nama, unit):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Sampah (nama, unit)
            VALUES (?, ?)
        ''', (nama, unit))
        conn.commit()
        print("Sampah berhasil ditambahkan.")
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk menambahkan rekord Harga
def add_Harga(conn, nama_sampah, harga, tgl_perubahan):
    try:
        cursor = conn.cursor()

        # cari id dari nama sampah yang dimasukkan dalam database
        cursor.execute('''
            SELECT id_sampah FROM Sampah WHERE nama = ?
        ''', (nama_sampah,))
        result = cursor.fetchone()

        # jika sampah ditemukan dalam database, insert ke dalam tabel
        if result:
            id_sampah = result[0]
            cursor.execute('''
                INSERT INTO Harga (id_sampah, harga, tanggal_perubahan)
                VALUES (?, ?, ?)
            ''', (id_sampah, harga, tgl_perubahan))
            conn.commit()
            print("Harga berhasil ditambahkan.")
        # jika tidak, berikan pesan bahwa sampah yang dimasukkan tidak ditemukan
        else:
            print(f"Sampah dengan nama '{nama_sampah}' tidak ditemukan.")
        
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk menambahkan rekord Kecamatan
def add_kecamatan(conn, nama):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Kecamatan (nama)
            VALUES (?)
        ''', (nama,))
        conn.commit()
        print("Kecamatan berhasil ditambahkan.")
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk menambahkan rekord Kelurahan
def add_kelurahan(conn, nama, nama_kecamatan):
    try:
        cursor = conn.cursor()

        # cari id dari nama kecamtan yang dimasukkan
        cursor.execute('''
            SELECT id_kecamatan FROM Kecamatan WHERE nama = ?
        ''', (nama_kecamatan,))
        result = cursor.fetchone()

        # jika kecamatan tersebut ada dalam database, masukkan datanya
        if result:
            id_kecamatan = result[0]
            cursor.execute('''
                INSERT INTO Kelurahan (nama, id_kecamatan)
                VALUES (?, ?)
            ''', (nama, id_kecamatan))
            conn.commit()
            print("Kelurahan berhasil ditambahkan.")
        # jika tidak, keluarkan pesan bahwa nama kecamatan yang dimasukkan tidak ada
        else:
            print(f"Kecamatan dengan nama '{nama_kecamatan}' tidak ditemukan.")
        
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk menambahkan rekord TPA
def add_TPA(conn, nama):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO TPA (nama)
            VALUES (?)
        ''', (nama,))
        conn.commit()
        print("TPA berhasil ditambahkan.")
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk menambahkan rekord Setoran Member
def add_setoranMember(conn, nama_member, nama_sampah, kuantitas, tgl):
    try:
        cursor = conn.cursor()

        # cari id dari nama member dan nama sampah yang dimasukkan
        cursor.execute('''
            SELECT id FROM Pengguna WHERE nama = ?
        ''', (nama_member,))
        resultMember = cursor.fetchone()

        cursor.execute('''
            SELECT id_sampah FROM Sampah WHERE nama = ?
        ''', (nama_sampah,))
        resultSampah = cursor.fetchone()

        # jika kedua nama member dan sampah ditemukan dalam database, masukkan datanya
        if resultMember and resultSampah:
            id_member = resultMember[0]
            id_sampah = resultSampah[0]
            cursor.execute('''
                INSERT INTO SetoranMember (id_member, id_sampah, kuantitas_sampah, tgl_transaksi)
                VALUES (?, ?, ?, ?)
            ''', (id_member, id_sampah, kuantitas, tgl))
            conn.commit()
            print("Setoran member berhasil ditambahkan.")
        # jika tidak, keluarkan pesan menyatakan objek mana yang tidak ditemukan
        elif resultMember == None:
            print(f"Nama member {nama_member} tidak ditemukan.")
        elif resultSampah == None:
            print(f"Sampah {nama_sampah} tidak ditemukan.")
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk menambahkan rekord Setoran Pusat
def add_setoranPusat(conn, nama_TPA, nama_sampah, kuantitas, tgl):
    try:
        cursor = conn.cursor()

        # cari id dari nama TPA dan nama sampah yang dimasukkan
        cursor.execute('''
            SELECT id_TPA FROM TPA WHERE nama = ?
        ''', (nama_TPA,))
        resultTPA = cursor.fetchone()

        cursor.execute('''
            SELECT id_sampah FROM Sampah WHERE nama = ?
        ''', (nama_sampah,))
        resultSampah = cursor.fetchone()

        # jika kedua nama TPA dan sampah ditemukan dalam database, masukkan datanya
        if resultTPA and resultSampah:
            id_TPA = resultTPA[0]
            id_sampah = resultSampah[0]
            cursor.execute('''
                INSERT INTO SetoranPusat (id_TPA, id_sampah, kuantitas_sampah, tgl_transaksi)
                VALUES (?, ?, ?, ?)
            ''', (id_TPA, id_sampah, kuantitas, tgl))
            conn.commit()
            print("Setoran pusat berhasil ditambahkan.")
        # jika tidak, keluarkan pesan menyatakan objek mana yang tidak ditemukan
        elif resultTPA == None:
            print(f"Nama TPA {nama_TPA} tidak ditemukan.")
        elif resultSampah == None:
            print(f"Nama sampah {nama_sampah} tidak ditemukan.")
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# ------------------------------ USER AUTHENTICATION ------------------------------ #

# screen yang meminta user untuk register atau login
def loginOrRegister(conn):
    registerAtauLogin = input("(R)egister atau (L)ogin: ")
    while registerAtauLogin.lower() != 'r' and registerAtauLogin.lower() != 'l':
        os.system('cls')
        registerAtauLogin = input("(R)egister atau (L)ogin: ")

    if registerAtauLogin.lower() == 'r':
        print('')
        register(conn)
    elif registerAtauLogin.lower() == 'l':
        print('')
        login(conn)

# Fungsi login
def login(conn):
    print("Silakan Login!")
    print("")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    authentication(conn, username, password)

# Fungsi register
def register(conn):
    nama = input("Masukkan nama: ")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    alamat = input("Masukkan alamat: ")
    telp = input("Masukkan nomor telepon: ")
    email = input("Masukkan email: ")
    kelurahan = input("Masukkan nama kelurahan: ")
    add_pengguna(conn, nama, email, username, password, "member", telp, alamat, kelurahan)
    os.system("cls")
    login(conn)

# Fungsi autentikasi
def authentication(conn, username, password):
    try:
        cursor = conn.cursor()

        # cari username dan password yang dimasukkan di dalam database
        cursor.execute('''
            SELECT peran FROM Pengguna WHERE username = ? AND password = ?
        ''', (username, password))
        result = cursor.fetchone()

        # jika username dan passwordnya ada, dan perannya adalah admin
        if result and "admin" in result[0]:
            os.system("cls")

            print("Login berhasil. Selamat datang, " + username + "!")
            adminScreen(conn)
        # jika username dan passwordnya ada, dan perannya adalah member
        elif result and "member" in result[0]:
            # ambil ID dari member tersebut
            cursor.execute('''
                SELECT id FROM Pengguna WHERE username = ? AND password = ?
            ''', (username, password))
            hasil = cursor.fetchone()
            id_member = hasil[0]
            os.system("cls")
            print("Login berhasil. Selamat datang, " + username + "!")
            memberScreen(conn, id_member)
        # jika username dan/atau password salah
        else:
            print("\nUsername atau password salah.\n")
            restart = input("Apakah anda ingin mencoba ulang (Y/N)? ")
            if restart.lower() != 'n':
                login(conn)
            else:
                conn.close()
    except pyodbc.Error as e:
        print("Error:", e)
        return False

# ------------------------------ USER INTERFACE ------------------------------ #
# Fungsi untuk menampilkan layar admin
def adminScreen(conn):
    exit_command = 'y'
    while exit_command.lower() != 'n':
        print('''
        List tindakan:
            1. Melihat daftar member
            2. Melihat setoran sampah
            3. Melihat setoran pusat
            4. Edit data tabel
            5. Log out
        ''')
        action_choice = int(input("Pilih tindakan yang ingin dilakukan: "))

        match action_choice:
            case 1:
                view_members(conn)
            case 2:
                view_setoran_sampah(conn)
            case 3:
                view_setoran_pusat(conn)
            case 4:
                edit_data_table(conn)
            case 5:
                os.system("cls")
                loginOrRegister(conn)

        exit_command = input("Masih ingin melakukan tindakan lain? (Y/N): ")
        os.system('cls')

        if exit_command.lower() == 'n':
            conn.close()

# Fungsi untuk menampilkan layar member
def memberScreen(conn, member_id):
    exit_command = 'y'
    while exit_command.lower() != 'n':
        # List tindakan yang bisa dilakukan oleh member
        print('''
        List tindakan:
            1. Melihat daftar harga jual sampah
            2. Melihat histori setoran sampah
            3. Melihat laporan pendapatan hasil setoran sampah dalam rentang waktu tertentu
            4. Log out
        ''')
        # input pilihan tindakan yang akan dilakukan
        action_choice = int(input("Pilih tindakan yang ingin dilakukan: "))

        match action_choice:
            case 1:
                view_harga(conn)
            case 2:
                view_setoran_member(conn, member_id)
            case 3:
                tgl_mulai = input("Masukkan tanggal mulai (YYYY-MM-DD): ")
                tgl_selesai = input("Masukkan tanggal selesai (YYYY-MM-DD): ")
                view_pendapatan_member(conn, member_id, tgl_mulai, tgl_selesai)
            case 4:
                os.system("cls")
                loginOrRegister(conn)

        exit_command = input("Masih ingin melakukan tindakan lain? (Y/N): ")
        os.system('cls')

        if exit_command.lower() == 'n':
            conn.close()

# ------------------------------ FITUR MEMBER ------------------------------ #
# Fungsi untuk melihat daftar harga beli sampah
def view_harga(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM [HargaView]')

        rows = cursor.fetchall()
        print("\nDaftar Harga Beli Sampah:")
        for row in rows:
            hasil = (f"Nama Sampah: {row[0]}, Harga: Rp{row[1]:.0f}, Tanggal Perubahan: {row[2]}")
            print(hasil)
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk melihat histori setoran sampah
def view_setoran_member(conn, member_id):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM [SetoranMemberView] WHERE id_member = ?', (member_id,))

        rows = cursor.fetchall()
        print("\nHistori Setoran Sampah:")
        for row in rows:
            print(f"ID Transaksi: {row[0]}, Nama Sampah: {row[4]}, Kuantitas Sampah: {row[5]}, Tanggal Transaksi: {row[6]}")
        print('')
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

def view_pendapatan_member(conn, member_id, tgl_mulai, tgl_selesai):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(Harga.harga * SetoranMember.kuantitas_sampah)
            FROM SetoranMember
            JOIN Harga ON SetoranMember.id_sampah = Harga.id_sampah
            WHERE SetoranMember.id_member = ? AND SetoranMember.tgl_transaksi BETWEEN ? AND ?
        ''', (member_id, tgl_mulai, tgl_selesai))

        total_pendapatan = cursor.fetchone()[0]

        if total_pendapatan is None:
            total_pendapatan = 0

        print(f"\nTotal Pendapatan dari {tgl_mulai} sampai {tgl_selesai}: Rp{total_pendapatan:.0f}\n")
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# ------------------------------ FITUR ADMIN ------------------------------ #
# Fungsi untuk melihat daftar member
def view_members(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Pengguna')

        rows = cursor.fetchall()
        print("\nDaftar Member:")
        for row in rows:
            hasil = (f"Id: {row[0]}\nNama: {row[1]}\nEmail: {row[2]}\nUsername: {row[3]}\nPassword: {row[4]}\nPeran: {row[5]}\nNo Telepon: {row[6]}\nAlamat: {row[7]}\nId Kelurahan: {row[8]}")
            print(hasil)
            print("==================================")
    except pyodbc.Error as e:
        print("Error:", e)
        print('')

# Fungsi untuk melihat setoran sampah dari member
def view_setoran_sampah(conn):
    print('''
    Pilihan:
        1. Melihat seluruh setoran sampah
        2. Melihat setoran sampah dalam rentang waktu tertentu
    ''')
    choice = int(input("Pilih opsi: "))

    if choice == 1:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM [SetoranMemberView]')
            
            rows = cursor.fetchall()
            print("\nDaftar Setoran Sampah:")
            for row in rows:
                print(f"ID Transaksi: {row[0]}, Nama Member: {row[2]}, Nama Sampah: {row[4]}, Kuantitas Sampah: {row[5]}, Tanggal Transaksi: {row[6]}")
            print('')
        except pyodbc.Error as e:
            print("Error:", e)
            print('')
    elif choice == 2:
        tgl_mulai = input("Masukkan tanggal mulai (YYYY-MM-DD): ")
        tgl_selesai = input("Masukkan tanggal selesai (YYYY-MM-DD): ")
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM [SetoranMemberView]
                WHERE Tanggal BETWEEN ? AND ?
            ''', (tgl_mulai, tgl_selesai))

            rows = cursor.fetchall()
            print(f"\nDaftar Setoran Sampah dari {tgl_mulai} sampai {tgl_selesai}:")
            for row in rows:
                print(f"ID Transaksi: {row[0]}, Nama Member: {row[2]}, Nama Sampah: {row[4]}, Kuantitas Sampah: {row[5]}, Tanggal Transaksi: {row[6]}")
            print('')
        except pyodbc.Error as e:
            print("Error:", e)
            print('')

# Fungsi untuk melihat setoran sampah ke TPA
def view_setoran_pusat(conn):
    print('''
    Pilihan:
        1. Melihat seluruh setoran pusat
        2. Melihat setoran pusat dalam rentang waktu tertentu
    ''')
    choice = int(input("Pilih opsi: "))

    if choice == 1:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM [SetoranPusatView]')
            
            rows = cursor.fetchall()
            print("\nDaftar Setoran Pusat:")
            for row in rows:
                print(f"ID Transaksi: {row[0]}, Nama TPA: {row[1]}, Nama Sampah: {row[2]}, Kuantitas Sampah: {row[3]}, Tanggal Transaksi: {row[4]}")
            print('')
        except pyodbc.Error as e:
            print("Error:", e)
            print('')
    elif choice == 2:
        tgl_mulai = input("Masukkan tanggal mulai (YYYY-MM-DD): ")
        tgl_selesai = input("Masukkan tanggal selesai (YYYY-MM-DD): ")
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM [SetoranPusatView]
                WHERE Tanggal BETWEEN ? AND ?
            ''', (tgl_mulai, tgl_selesai))

            rows = cursor.fetchall()
            print(f"\nDaftar Setoran Pusat dari {tgl_mulai} sampai {tgl_selesai}:")
            for row in rows:
                print(f"ID Transaksi: {row[0]}, Nama TPA: {row[1]}, Nama Sampah: {row[2]}, Kuantitas Sampah: {row[3]}, Tanggal Transaksi: {row[4]}")
            print('')
        except pyodbc.Error as e:
            print("Error:", e)
            print('')

# Fungsi untuk mengedit data tabel
def edit_data_table(conn):
    # Import tanggal sekarang, dan format sesuai ketentuan SQL
    x = datetime.datetime.now()
    year = x.year
    month = x.month
    day = x.day
    tgl_format = f"{year}-{month}-{day}"

    exit_command = 'y'
    # List tabel yang tersedia
    while exit_command.lower() != 'n':
        os.system('cls')
        print('''
        List tabel:
            1. Kecamatan
            2. Kelurahan
            3. Sampah
            4. Harga
            5. TPA
            6. Setoran Member
            7. Setoran Pusat
            8. Admin
        ''')
        
        table_choice = int(input("Ingin memasukkan data ke tabel yang mana? : "))

        # Minta data yang sesuai dengan tabel yang dipilih
        match table_choice:
            case 1:
                nama = input("Masukkan nama kecamatan: ")
                add_kecamatan(conn, nama)
            case 2:
                nama = input("Masukkan nama kelurahan: ")
                nama_kecamatan = input("Masukkan nama kecamatan: ")
                add_kelurahan(conn, nama, nama_kecamatan)
            case 3:
                nama = input("Masukkan nama sampah: ")
                unit = input("Masukkan unit sampah: ")
                add_sampah(conn, nama, unit)
            case 4:
                nama_sampah = input("Masukkan nama sampah: ")
                harga = input("Masukkan harga sampah: ")
                add_Harga(conn, nama_sampah, harga, tgl_format)
            case 5:
                nama = input("Masukkan nama TPA: ")
                add_TPA(conn, nama)
            case 6:
                nama_member = input("Masukkan nama member: ")
                nama_sampah = input("Masukkan nama sampah: ")
                kuantitas = input("Masukkan kuantitas sampah: ")
                add_setoranMember(conn, nama_member, nama_sampah, kuantitas, tgl_format)
            case 7:
                nama_TPA = input("Masukkan nama TPA: ")
                nama_sampah = input("Masukkan nama sampah: ")
                kuantitas = input("Masukkan kuantitas sampah: ")
                add_setoranPusat(conn, nama_TPA, nama_sampah, kuantitas, tgl_format)
            case 8:
                print("Silakan masukkan informasi admin baru!")
                nama = input("Masukkan nama: ")
                username = input("Masukkan username: ")
                password = input("Masukkan password: ")
                alamat = input("Masukkan alamat: ")
                telp = input("Masukkan nomor telepon: ")
                email = input("Masukkan email: ")
                kelurahan = input("Masukkan nama kelurahan: ")
                add_pengguna(conn, nama, email, username, password, "admin", telp, alamat, kelurahan)
        
        exit_command = input("Masih ingin memasukkan data? (Y/N): ")

if __name__ == "__main__":
    conn = create_connection()
    os.system('cls')
    loginOrRegister(conn)