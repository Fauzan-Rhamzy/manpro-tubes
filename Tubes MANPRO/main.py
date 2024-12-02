from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
    conn = sqlite3.connect('database/database.db') 
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/kecamatan', methods=['GET'])
def kecamatan():
    conn = get_db_connection()
    cursor = conn.cursor()
    if(request.args):
        nama_kecamatan = request.args.get('nama_kecamatan')
        print(nama_kecamatan)
        cursor.execute("SELECT * FROM Kecamatan WHERE LOWER(nama) LIKE LOWER(?)", (f"%{nama_kecamatan}%",))
        kecamatan_data = cursor.fetchall()
        conn.close()
    else:
        cursor.execute("SELECT * FROM Kecamatan")
        kecamatan_data = cursor.fetchall()
        conn.close() 
    return render_template('kecamatan-admin.html', kecamatan=kecamatan_data)

@app.route('/tambah_kecamatan', methods=['GET', 'POST'])
def tembahKecamatan():
    if(request.method=='GET'):
        return render_template('tambah-kecamatan.html')
    else:
        nama_kecamatan = request.form.get('nama')
        print(nama_kecamatan)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Kecamatan (nama) VALUES (?)",
            ((nama_kecamatan,))
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('kecamatan'))
    
@app.route('/pengguna', methods=['GET'])
def pengguna():
    conn = get_db_connection()
    cursor = conn.cursor()
    if(request.args):
        nama_pengguna = request.args.get('nama_pengguna')
        print(nama_pengguna)
        cursor.execute("SELECT * FROM penggunaView WHERE LOWER(nama) LIKE LOWER(?)", (f"%{nama_pengguna}%",))
        pengguna_data = cursor.fetchall()
        conn.close()
    else:
        cursor.execute("SELECT * FROM penggunaView")
        pengguna_data = cursor.fetchall()
        conn.close()
    return render_template('admin/pengguna-admin.html', pengguna=pengguna_data)

@app.route('/tambah_pengguna', methods=['GET', 'POST'])
def tambahpengguna():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        # Ambil semua data kecamatan
        cursor.execute("SELECT * FROM Kecamatan")
        kecamatan_data = cursor.fetchall()

        # Ambil data kelurahan jika ada kecamatan yang dipilih
        kecamatan_id = request.args.get('kecamatan')
        data_kelurahan = []
        if kecamatan_id:
            cursor.execute("SELECT * FROM Kelurahan WHERE id_kecamatan=?", (kecamatan_id,))
            data_kelurahan = cursor.fetchall()

        conn.close()
        return render_template(
            'admin/tambah-pengguna.html',
            kecamatan=kecamatan_data,
            kelurahan=data_kelurahan
        )
    else:
        nama = request.form['nama']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        telepon = request.form['telepon']
        alamat = request.form['alamat']
        kelurahan_id = request.form['kelurahan']
        print(f"nama")
        print(f"email")
        print(f"username")
        print(f"password")
        print(f"role")
        print(f"telepon")
        print(f"alamat")
        print(f"Kecamatan ID yang diterima: {kelurahan_id}")

        nama_pengguna = request.form.get('nama')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pengguna (nama, email, username, password, role, telepon, alamat, id_kelurahan) VALUES (?,?,?,?,?,?,?,?)",
            ((nama,email, username, password, role, telepon, alamat, kelurahan_id))
        )
        conn.commit()
        conn.close()
        print(nama_pengguna)
        return redirect(url_for('pengguna'))

@app.route('/edit_pengguna', methods=['GET', 'POST'])
def edit_pengguna():
    id_user = request.args.get('id')
    if(request.method == 'GET'):
        print(id)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pengguna WHERE id=?",(id_user,))
        data_pengguna = cursor.fetchone()
        cursor.execute("SELECT * FROM Kecamatan")
        kecamatan_data = cursor.fetchall()

        data_kelurahan = []

        cursor.execute("select kecamatan.id as id_camat, kelurahan.id as id_lurah from kecamatan join kelurahan on kecamatan.id = kelurahan.id_kecamatan where id_lurah = ?" , (data_pengguna[8],))
        kecamatan_ids = cursor.fetchone()
        conn.close()

        if kecamatan_ids:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Kelurahan WHERE id_kecamatan=?", (kecamatan_ids[0],))
            data_kelurahan = cursor.fetchall()
        print(data_pengguna[0])
        return render_template('admin/edit-pengguna.html', data = data_pengguna, kecamatan=kecamatan_data, kelurahan=data_kelurahan, kecamatan_id=kecamatan_ids)
    else:
        print("tes")
        conn = get_db_connection()
        cursor = conn.cursor()
        if(request.is_json):
            print("tes2")
            data = request.json
            id_kecamatan = data.get('kecamatan', None)
            print(id_kecamatan)
            cursor.execute("SELECT * FROM Kelurahan WHERE id_kecamatan=?", (id_kecamatan,))
            data_kelurahan = cursor.fetchall()
            data_kelurahan_dict = [dict(row) for row in data_kelurahan]
            print(data_kelurahan_dict)
            return jsonify(data_kelurahan_dict)
        else:
            nama = request.form['nama']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']
            telepon = request.form['telepon']
            alamat = request.form['alamat']
            kelurahan_id = request.form['kelurahan']
            print(f"nama")
            print(f"email")
            print(f"username")
            print(f"password")
            print(f"role")
            print(f"telepon")
            print(f"alamat")
            print(f"Kecamatan ID yang diterima: {kelurahan_id}")

            nama_pengguna = request.form.get('nama')
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Pengguna SET nama = ?, email = ?, password= ?, role = ?, telepon = ?, alamat = ?, id_kelurahan= ? WHERE id = ?;",
                ((nama,email, password, role, telepon, alamat, kelurahan_id, id_user))
            )
            conn.commit()
            conn.close()
            print(nama_pengguna)
            return redirect(url_for('pengguna'))

@app.route('/sampah', methods=['GET'])
def dataSampah():
    conn = get_db_connection()
    cursor = conn.cursor()
    nama = session.get('nama', None)
    role = session.get('role', None)
    if(request.args):
        nama_sampah = request.args.get('nama_sampah')
        print(nama_sampah)
        cursor.execute("SELECT * FROM Sampah WHERE LOWER(nama) LIKE LOWER(?)", (f"%{nama_sampah}%",))
        sampah_data = cursor.fetchall()
        conn.close()
    else:
        cursor.execute("SELECT * FROM Sampah")
        sampah_data = cursor.fetchall()
        conn.close() 
    if(role == 'admin'):
        return render_template('admin/sampah-admin.html', sampah=sampah_data)
    else:
        return render_template('member/sampah-member.html', sampah=sampah_data)
    
@app.route('/data_penjualan_sampah')
def data_penjualan_sampah():
    conn = get_db_connection()
    cursor = conn.cursor()
    if(request.args):
        mulai = request.args.get('tgl-mulai')
        akhir = request.args.get('tgl-akhir')

        date_object_mulai = datetime.strptime(mulai, "%Y-%m-%d")
        month_str_mulai = str(date_object_mulai.month).zfill(2)
        day_str_mulai = str(date_object_mulai.day).zfill(2)
        tanggal_mulai = str(date_object_mulai.year) + "" + month_str_mulai + "" + day_str_mulai

        date_object_akhir = datetime.strptime(akhir, "%Y-%m-%d")
        month_str_akhir = str(date_object_akhir.month).zfill(2)
        day_str_akhir = str(date_object_akhir.day).zfill(2)
        tanggal_akhir = str(date_object_akhir.year) + "" + month_str_akhir + "" + day_str_akhir

        print(tanggal_mulai)
        print(tanggal_akhir)
        cursor.execute("SELECT * FROM DataJualSampahView WHERE tanggal >= ? AND tanggal <= ?", (tanggal_mulai, tanggal_akhir))
        setoran = cursor.fetchall()
        conn.close()
    else:
        cursor.execute("SELECT * FROM DataJualSampahView")
        setoran = cursor.fetchall()
        conn.close()
    return render_template('admin/data-jual-admin.html', setoran_pusat = setoran)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if(request.method=='GET'):
        cursor.execute("SELECT * FROM Kecamatan")
        kecamatan_data = cursor.fetchall()

        kecamatan_id = request.args.get('kecamatan')
        data_kelurahan = []
        if kecamatan_id:
            cursor.execute("SELECT * FROM Kelurahan WHERE id_kecamatan=?", (kecamatan_id,))
            data_kelurahan = cursor.fetchall()

        conn.close()
        return render_template(
            'register.html',
            kecamatan=kecamatan_data,
            kelurahan=data_kelurahan
        )
    else:
        if(request.is_json):
            conn = get_db_connection()
            cursor = conn.cursor()
            data = request.get_json()
            kecamatanId = data.get('kecamatanId')
            username = data.get('username')
            if(kecamatanId):
                cursor.execute("SELECT * FROM Kelurahan WHERE id_kecamatan=?", (kecamatanId,))
                data_kelurahan = cursor.fetchall()
                data_kelurahan_dict = [dict(row) for row in data_kelurahan]
                return jsonify(data_kelurahan_dict)
            if(username):
                cursor.execute("SELECT username FROM Pengguna WHERE username=?", (username,))
                dataDB = cursor.fetchone()
                print(dataDB)
                if(dataDB is None):
                    user_db = 'None'    
                else:
                    user_db = "found"
                return jsonify(user_db)
        else:
            nama = request.form.get('nama')
            email = request.form.get('email')
            telepon = request.form.get('telepon')
            username = request.form.get('username')
            password = request.form.get('password')
            alamat = request.form.get('alamat')
            id_kelurahan = request.form.get('kelurahan')
            print(id_kelurahan)
            cursor.execute("INSERT INTO Pengguna (nama, email, username, password, role, telepon, alamat, id_kelurahan) VALUES (?,?,?,?,?,?,?,?)", (nama, email, username, password, 'member', telepon, alamat, id_kelurahan,))
            conn.commit()
            return render_template('login.html', info="Registrasi berhasil, silakan login!")


if __name__ == '__main__':
    os.makedirs('database', exist_ok=True)
    app.run(debug=True)
