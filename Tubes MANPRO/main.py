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

if __name__ == '__main__':
    os.makedirs('database', exist_ok=True)
    app.run(debug=True)
