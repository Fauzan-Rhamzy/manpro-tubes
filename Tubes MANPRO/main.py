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

@app.route('/home')
def home():
    nama = session.get('nama', None)
    role = session.get('role', None)
    if(role == "admin"):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(id) FROM Pengguna")   
        banyakUser = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(id) FROM SetoranPusat")   
        banyakTransaksiPusat = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(id) FROM SetoranMember")   
        banyakTransaksiMember = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(harga) FROM SetoranPusat_detail")   
        banyakPendapatan = cursor.fetchone()[0]
        conn.close()

        if(banyakPendapatan==None):
            banyakPendapatan = 0   

        print(banyakPendapatan)
        return render_template('main-admin.html', name=nama, users=banyakUser, total_transaksi_member=banyakTransaksiMember, total_transaksi_pusat=banyakTransaksiPusat,total_pendapatan=banyakPendapatan)
    if(role=="member"):
        return "<h1>Kamu adalah member</h1>"
    else:
        return redirect(url_for('login'))

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
    return render_template('data-jual-admin.html', setoran_pusat = setoran)

@app.route('/jual_sampah')
def jual_sampah():
    return render_template('penjualan.html')

@app.route('/tpa', methods=['GET'])
def tpa():
    conn = get_db_connection()
    cursor = conn.cursor()
    if(request.args):
        nama_tpa = request.args.get('nama_tpa')
        print(nama_tpa)
        cursor.execute("SELECT * FROM Tpa WHERE LOWER(nama) LIKE LOWER(?)", (f"%{nama_tpa}%",))
        tpa_data = cursor.fetchall()
        conn.close()
    else:
        cursor.execute("SELECT * FROM Tpa")
        tpa_data = cursor.fetchall()
        conn.close() 
    return render_template('tpa-admin.html', tpa=tpa_data)

@app.route('/tambah_tpa', methods=['GET', 'POST'])
def tambahtpa():
    if(request.method=='GET'):
        return render_template('tambah-tpa.html')
    else:
        nama_tpa = request.form.get('nama')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tpa (nama) VALUES (?)",
            ((nama_tpa,))
        )
        conn.commit()
        conn.close()
        print(nama_tpa)
        return redirect(url_for('tpa'))

if __name__ == '__main__':
    os.makedirs('database', exist_ok=True)
    app.run(debug=True)
