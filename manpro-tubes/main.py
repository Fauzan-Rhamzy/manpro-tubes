from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import date
import sqlite3
import os
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
    conn = sqlite3.connect('database/database.db') 
    conn.row_factory = sqlite3.Row 
    return conn


@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'static']
    if 'nama' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username, role, nama, id FROM Pengguna WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            nama = user[2]
            role = user[1]
            id = user[3]

            session['nama'] = nama
            session['role'] = role
            session['id'] = id
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Username atau password salah!")
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    nama = session.get('nama', None)
    role = session.get('role', None)
    id = session.get('id', None)
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
        return render_template('admin/main-admin.html', name=nama, users=banyakUser, total_transaksi_member=banyakTransaksiMember, total_transaksi_pusat=banyakTransaksiPusat,total_pendapatan=banyakPendapatan)
    elif(role=="member"):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(id) FROM SetoranMember WHERE id_member = ?", (id,))   
        banyakTransaksiMember = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(harga) FROM PendapatanMemberView WHERE id_member=?", (id,))   
        banyakPendapatan = cursor.fetchone()[0]
        conn.close()

        if(banyakPendapatan==None):
            banyakPendapatan = 0 

        return render_template('member/main-member.html', nama=nama, total_transaksi=banyakTransaksiMember, total_pendapatan=banyakPendapatan)
    else:
        return redirect(url_for('login'))

@app.route('/histori')
def histori():
    nama = session.get('nama', None)
    role = session.get('role', None)
    id = session.get('id', None)
    conn = get_db_connection()
    cursor = conn.cursor()
    if(role == 'admin'):
        return render_template('<h1>Kamu adalah admin<h1>')
    else:
        if(request.args):
            mulai = request.args.get('tgl-mulai')
            akhir = request.args.get('tgl-akhir')
            
            if(mulai == "" and akhir != ""):
                date_object_akhir = datetime.strptime(akhir, "%Y-%m-%d")
                month_str_akhir = str(date_object_akhir.month).zfill(2)
                day_str_akhir = str(date_object_akhir.day).zfill(2)
                tanggal_akhir = str(date_object_akhir.year) + "" + month_str_akhir + "" + day_str_akhir
                cursor.execute('SELECT *, tanggal FROM SetoranMember WHERE id_member=? AND tanggal<=?',(id, tanggal_akhir,))
                transaksi = cursor.fetchall()
                conn.close()
                return render_template('member/histori-member.html', transaksi=transaksi)
            elif(mulai != "" and akhir == ""):
                date_object_mulai = datetime.strptime(mulai, "%Y-%m-%d")
                month_str_mulai = str(date_object_mulai.month).zfill(2)
                day_str_mulai = str(date_object_mulai.day).zfill(2)
                tanggal_mulai = str(date_object_mulai.year) + "" + month_str_mulai + "" + day_str_mulai
                cursor.execute('SELECT *, tanggal FROM SetoranMember WHERE id_member=? AND tanggal>=?',(id, tanggal_mulai,))
                transaksi = cursor.fetchall()
                return render_template('member/histori-member.html', transaksi=transaksi)
            elif(mulai == "" and akhir == ""):
                cursor.execute("SELECT * FROM SetoranMember WHERE id_member=?", (id,))
                transaksi = cursor.fetchall()
                conn.close()
            else:
                date_object_mulai = datetime.strptime(mulai, "%Y-%m-%d")
                month_str_mulai = str(date_object_mulai.month).zfill(2)
                day_str_mulai = str(date_object_mulai.day).zfill(2)
                tanggal_mulai = str(date_object_mulai.year) + "" + month_str_mulai + "" + day_str_mulai
                date_object_akhir = datetime.strptime(akhir, "%Y-%m-%d")
                month_str_akhir = str(date_object_akhir.month).zfill(2)
                day_str_akhir = str(date_object_akhir.day).zfill(2)
                tanggal_akhir = str(date_object_akhir.year) + "" + month_str_akhir + "" + day_str_akhir
                cursor.execute('SELECT *, tanggal FROM SetoranMember WHERE id_member=? AND tanggal>=? AND tanggal<=?',(id, tanggal_mulai, tanggal_akhir,))
                transaksi = cursor.fetchall()
                return render_template('member/histori-member.html', transaksi=transaksi)
        else:
            cursor.execute('SELECT *, tanggal FROM SetoranMember WHERE id_member=?',(id,))
            transaksi = cursor.fetchall()
            conn.close()
        return render_template('member/histori-member.html', transaksi=transaksi)


@app.route('/histori_detail', methods=['GET'])
def histori_detail():
    id_transaksi = request.args.get('id')
    print("id transaksi adalah " +  id_transaksi)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PendapatanMemberView WHERE id_transaksi=?", (id_transaksi,))
    sampah_data = cursor.fetchall()
    total = 0
    for item in sampah_data:
        total = total + item['harga']
    return render_template('member/histori-detail.html', detail=sampah_data, total=total)

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

        
@app.route('/laporan')
def laporan():
    nama = session.get('nama', None)
    role = session.get('role', None)
    id = session.get('id', None)
    conn = get_db_connection()
    cursor = conn.cursor()
    if(role == 'admin'):
        return render_template('<h1>Kamu adalah admin<h1>')
    else:
        if(request.args):
            mulai = request.args.get('tgl-mulai')
            akhir = request.args.get('tgl-akhir')
            
            if(mulai == "" and akhir != ""):
                date_object_akhir = datetime.strptime(akhir, "%Y-%m-%d")
                month_str_akhir = str(date_object_akhir.month).zfill(2)
                day_str_akhir = str(date_object_akhir.day).zfill(2)
                tanggal_akhir = str(date_object_akhir.year) + "" + month_str_akhir + "" + day_str_akhir
                cursor.execute('SELECT *, tanggal FROM LaporanMember WHERE id_member=? AND tanggal<=?',(id, tanggal_akhir,))
                transaksi = cursor.fetchall()
                conn.close()
            elif(mulai != "" and akhir == ""):
                date_object_mulai = datetime.strptime(mulai, "%Y-%m-%d")
                month_str_mulai = str(date_object_mulai.month).zfill(2)
                day_str_mulai = str(date_object_mulai.day).zfill(2)
                tanggal_mulai = str(date_object_mulai.year) + "" + month_str_mulai + "" + day_str_mulai
                cursor.execute('SELECT *, tanggal FROM LaporanMember WHERE id_member=? AND tanggal>=?',(id, tanggal_mulai,))
                transaksi = cursor.fetchall()
            elif(mulai == "" and akhir == ""):
                cursor.execute("SELECT * FROM LaporanMember WHERE id_member=?", (id,))
                transaksi = cursor.fetchall()
                conn.close()
            else:
                date_object_mulai = datetime.strptime(mulai, "%Y-%m-%d")
                month_str_mulai = str(date_object_mulai.month).zfill(2)
                day_str_mulai = str(date_object_mulai.day).zfill(2)
                tanggal_mulai = str(date_object_mulai.year) + "" + month_str_mulai + "" + day_str_mulai
                date_object_akhir = datetime.strptime(akhir, "%Y-%m-%d")
                month_str_akhir = str(date_object_akhir.month).zfill(2)
                day_str_akhir = str(date_object_akhir.day).zfill(2)
                tanggal_akhir = str(date_object_akhir.year) + "" + month_str_akhir + "" + day_str_akhir
                cursor.execute('SELECT *, tanggal FROM LaporanMember WHERE id_member=? AND tanggal>=? AND tanggal<=?',(id, tanggal_mulai, tanggal_akhir,))
                transaksi = cursor.fetchall()
        else:
            cursor.execute('SELECT *, tanggal FROM LaporanMember WHERE id_member=?',(id,))
            transaksi = cursor.fetchall()
            conn.close()
        total = 0
        for item in transaksi:
            total = total + item['total']
        return render_template('member/pendapatan-member.html', transaksi=transaksi, total = total)


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
    return render_template('admin/kecamatan-admin.html', kecamatan=kecamatan_data)

@app.route('/tambah_kecamatan', methods=['GET', 'POST'])
def tembahKecamatan():
    if(request.method=='GET'):
        return render_template('admin/tambah-kecamatan.html')
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


@app.route('/kelurahan', methods=['GET'])
def kelurahan():
    conn = get_db_connection()
    cursor = conn.cursor()
    if(request.args):
        nama_kelurahan = request.args.get('nama_kelurahan')
        print(nama_kelurahan)
        cursor.execute("SELECT * FROM kelurahanJoinKecamatan WHERE LOWER(nama_kelurahan) LIKE LOWER(?)", (f"%{nama_kelurahan}%",))
        kelurahan_data = cursor.fetchall()
        conn.close()
    else:
        cursor.execute("SELECT * FROM kelurahanJoinKecamatan")
        kelurahan_data = cursor.fetchall()
        conn.close() 
    return render_template('admin/kelurahan-admin.html', kelurahan=kelurahan_data)

@app.route('/tambah_kelurahan', methods=['GET', 'POST'])
def tambahKelurahan():
    if(request.method=='GET'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Kecamatan")
        kecamatan_data = cursor.fetchall()
        conn.close()
        return render_template('admin/tambah-kelurahan.html', kecamatan=kecamatan_data)
    else:
        nama_kelurahan = request.form.get('nama')
        id_kecamatan = request.form['kecamatan']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Kelurahan (nama, id_kecamatan) VALUES (?,?)",
            ((nama_kelurahan,id_kecamatan,))
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('kelurahan'))



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
    return render_template('admin/tpa-admin.html', tpa=tpa_data)

@app.route('/tambah_tpa', methods=['GET', 'POST'])
def tambahtpa():
    if(request.method=='GET'):
        return render_template('admin/tambah-tpa.html')
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

@app.route('/data_pembelian_sampah')
def data_pembelian_sampah():
    conn = get_db_connection()
    cursor = conn.cursor()
    if(request.args):
        mulai = request.args.get('tgl-mulai')
        akhir = request.args.get('tgl-akhir')
        
        if(mulai == "" and akhir != ""):
            date_object_akhir = datetime.strptime(akhir, "%Y-%m-%d")
            month_str_akhir = str(date_object_akhir.month).zfill(2)
            day_str_akhir = str(date_object_akhir.day).zfill(2)
            tanggal_akhir = str(date_object_akhir.year) + "" + month_str_akhir + "" + day_str_akhir
            cursor.execute('SELECT *, tanggal FROM DataBeliSampahView WHERE tanggal<=?',(tanggal_akhir,))
            setoran = cursor.fetchall()
            conn.close()
        elif(mulai != "" and akhir == ""):
            date_object_mulai = datetime.strptime(mulai, "%Y-%m-%d")
            month_str_mulai = str(date_object_mulai.month).zfill(2)
            day_str_mulai = str(date_object_mulai.day).zfill(2)
            tanggal_mulai = str(date_object_mulai.year) + "" + month_str_mulai + "" + day_str_mulai
            cursor.execute('SELECT *, tanggal FROM DataBeliSampahView WHERE tanggal>=?',(tanggal_mulai,))
            setoran = cursor.fetchall()
        elif(mulai == "" and akhir == ""):
            cursor.execute("SELECT * FROM DataBeliSampahView")
            setoran = cursor.fetchall()
            conn.close()
        else:
            date_object_mulai = datetime.strptime(mulai, "%Y-%m-%d")
            month_str_mulai = str(date_object_mulai.month).zfill(2)
            day_str_mulai = str(date_object_mulai.day).zfill(2)
            tanggal_mulai = str(date_object_mulai.year) + "" + month_str_mulai + "" + day_str_mulai
            date_object_akhir = datetime.strptime(akhir, "%Y-%m-%d")
            month_str_akhir = str(date_object_akhir.month).zfill(2)
            day_str_akhir = str(date_object_akhir.day).zfill(2)
            tanggal_akhir = str(date_object_akhir.year) + "" + month_str_akhir + "" + day_str_akhir
            cursor.execute('SELECT *, tanggal FROM DataBeliSampahView WHERE tanggal>=? AND tanggal<=?',(tanggal_mulai, tanggal_akhir,))
            setoran = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM DataBeliSampahView")
        setoran = cursor.fetchall()
        conn.close()
    return render_template('admin/data-beli-admin.html', setoran_member=setoran)

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

@app.route('/beli_sampah', methods=['GET', 'POST'])
def beli_sampah():
    conn = get_db_connection()
    cursor = conn.cursor()
    if(request.method == 'GET'):
        cursor.execute("SELECT * FROM Sampah")
        sampah_data = cursor.fetchall()
        conn.close()
        return render_template('admin/pembelian.html', sampah = sampah_data)
    else:
        if request.is_json:
            data = request.get_json()
            
            if data.get('username'):
                username = data.get('username')
                print(f"Received username: {username}")

                cursor.execute("SELECT username FROM Pengguna WHERE username = ?", (username,))
                if cursor.fetchall():
                    return jsonify("found") 
                else:
                    return jsonify("None")
            else:
                cursor.execute("SELECT harga FROM Sampah")
                harga_sampah = cursor.fetchall()
                kuantitas_data = data.get('data') 
                items = []
                
                for item in kuantitas_data:
                    print(f"Name: {item['name']}, Value: {item['value']}")
                    match = re.search(r'\d+', item['name'])
                    if (item['value'] == ''):
                        item['value'] = 0
                    items.append({
                        'name': item['name'],
                        'id' : int(match.group()),
                        'value': item['value']
                    })
                total = 0
                for i in range(0, len(items)):
                    total = total + int(harga_sampah[i][0]) * int(items[i]['value'])
                print(total)

                return jsonify(total)
        
        else:
            print("Handling form data")

            username = request.form.get('username')
            if username:
                items = []
                cursor.execute("SELECT * FROM Sampah")
                sampah_data = cursor.fetchall()

                for item in sampah_data:
                    kuantitas_key = f"kuantitas{item[0]}"
                    kuantitas = request.form.get(kuantitas_key)
                    if kuantitas:
                        kuantitas = int(kuantitas)
                        items.append({
                            'id': item[0],
                            'nama': item[1],
                            'kuantitas': kuantitas
                        })

                for i in range(0, len(items)):
                    print(items[i])

                cursor.execute("SELECT * FROM Pengguna WHERE username=?", (username,))
                pengguna_id = cursor.fetchall()

                if pengguna_id:
                    print(pengguna_id[0][0])
                    tanggal = date.today()
                    tanggal_format = tanggal.strftime("%Y%m%d")
                    cursor.execute("INSERT INTO SetoranMember (id_member, tanggal) VALUES (?, ?)", (pengguna_id[0][0], tanggal_format))
                    conn.commit()

                    cursor.execute("SELECT MAX(id) FROM SetoranMember")
                    id_transaksi = cursor.fetchall()
                    print("id transaksi: " + str(id_transaksi[0][0]))

                    for item in items:
                        if(item['kuantitas'] != 0):
                            cursor.execute("SELECT harga FROM Sampah WHERE id = ?", (item['id'],))
                            harga_sampah = cursor.fetchall()
                            harga = harga_sampah[0][0] * item['kuantitas']
                            print("id sampah: " + str(item['id']))
                            print("kuantitas sampah: " + str(item['kuantitas']))
                            print("harga sampah: " + str(harga))
                            cursor.execute("INSERT INTO SetoranMember_detail (id_setoran_member, id_sampah, kuantitas, harga) VALUES (?, ?, ?, ?)", (id_transaksi[0][0], item['id'], item['kuantitas'], harga,))
                            conn.commit()

                    conn.close()
                    return redirect(url_for('data_pembelian_sampah'))
                else:
                    print("Pengguna tidak ditemukan.")
            else:
                print("Username tidak ditemukan di form.")
                return jsonify({"error": "Username is required"})


@app.route('/pembelian_sampah_detail', methods=['GET'])
def pembelian_sampah_detail():
    id_transaksi = request.args.get('id')
    print("id tpa adalah " +  id_transaksi)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BeliDetailView WHERE id_transaksi=?", (id_transaksi,))
    sampah_data = cursor.fetchall()
    total = 0
    for item in sampah_data:
        total = total + item['harga']
    return render_template('admin/beli-detail.html', detail=sampah_data, total=total)

@app.route('/penjualan_sampah_detail', methods=['GET'])
def penjualan_sampah_detail():
    id_transaksi = request.args.get('id')
    print("id tpa adalah " + id_transaksi)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JualDetailView WHERE id_transaksi=?", (id_transaksi,))
    sampah_data = cursor.fetchall()
    total = 0
    for item in sampah_data:
        total = total + item['harga']
    return render_template('admin/jual-detail.html', detail=sampah_data, total=total)

@app.route('/jual_sampah', methods=['GET', 'POST'])
def jual_sampah():
    conn = get_db_connection()
    cursor = conn.cursor()
    if(request.method == 'GET'):
        cursor.execute("SELECT * FROM Sampah")
        sampah_data = cursor.fetchall()
        conn.close()
        return render_template('admin/penjualan.html', sampah = sampah_data)
    else:
        if request.is_json:
            data = request.get_json()
            tpa_id = data.get('id_tpa')
            print(tpa_id)
            if data.get('id_tpa'):
                id_tpa = data.get('id_tpa')
                print(f"Received id: {id_tpa}")

                cursor.execute("SELECT nama FROM TPA WHERE id = ?", (id_tpa,))
                nama_tpa = cursor.fetchone()
                if nama_tpa:
                    print(nama_tpa[0])
                    return jsonify(nama_tpa[0])
                else:
                    print("Data tidak ditemukan.")
                    return jsonify('None')

            else:
                cursor.execute("SELECT harga FROM Sampah")
                harga_sampah = cursor.fetchall()
                kuantitas_data = data.get('data') 
                items = []
                
                for item in kuantitas_data:
                    print(f"Name: {item['name']}, Value: {item['value']}")
                    match = re.search(r'\d+', item['name'])
                    if (item['value'] == ''):
                        item['value'] = 0
                    items.append({
                        'name': item['name'],
                        'id' : int(match.group()),
                        'value': item['value']
                    })
                total = 0
                for i in range(0, len(items)):
                    total = total + int(harga_sampah[i][0]) * int(items[i]['value'])
                print(total)

                return jsonify(total)
        
        else:
            print("Handling form data")

            id_tpa = request.form.get('id_tpa')
            if id_tpa:
                items = []
                cursor.execute("SELECT * FROM Sampah")
                sampah_data = cursor.fetchall()

                for item in sampah_data:
                    kuantitas_key = f"kuantitas{item[0]}"
                    kuantitas = request.form.get(kuantitas_key)
                    if kuantitas:
                        kuantitas = int(kuantitas)
                        items.append({
                            'id': item[0],
                            'nama': item[1],
                            'kuantitas': kuantitas
                        })

                for i in range(0, len(items)):
                    print(items[i])

                tanggal = date.today()
                tanggal_format = tanggal.strftime("%Y%m%d")
                cursor.execute("INSERT INTO SetoranPusat (id_tpa, tanggal) VALUES (?, ?)", (id_tpa[0][0], tanggal_format))
                conn.commit()

                cursor.execute("SELECT MAX(id) FROM SetoranPusat")
                id_transaksi = cursor.fetchall()
                print("id transaksi: " + str(id_transaksi[0][0]))

                for item in items:
                    if(item['kuantitas'] != 0):
                        cursor.execute("SELECT harga FROM Sampah WHERE id = ?", (item['id'],))
                        harga_sampah = cursor.fetchall()
                        harga = harga_sampah[0][0] * item['kuantitas']
                        print("id sampah: " + str(item['id']))
                        print("kuantitas sampah: " + str(item['kuantitas']))
                        print("harga sampah: " + str(harga))
                        cursor.execute("INSERT INTO SetoranPusat_detail (id_setoran_pusat, id_sampah, kuantitas, harga) VALUES (?, ?, ?, ?)", (id_transaksi[0][0], item['id'], item['kuantitas'], harga,))
                        conn.commit()

                conn.close()
                return redirect(url_for('data_penjualan_sampah'))


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

@app.route('/tambah_sampah', methods=['GET', 'POST'])
def tembahSampah():
    if(request.method=='GET'):
        return render_template('admin/tambah-sampah.html')
    else:
        nama_sampah = request.form.get('nama')
        unit_sampah = request.form.get('unit')
        harga_sampah = request.form.get('harga')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Sampah (nama, unit, harga) VALUES (?, ?, ?)",
            (nama_sampah, unit_sampah, harga_sampah)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('dataSampah'))

@app.route('/edit_sampah', methods=['GET', 'POST'])
def edit_sampah():
    id = request.args.get('id')
    if(request.method == 'GET'):
        print(id)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sampah WHERE id=?",(id))
        data_sampah = cursor.fetchone()
        return render_template('admin/edit-sampah.html', data=data_sampah)
    else:
        nama = request.form.get('nama')
        unit = request.form.get('unit')
        harga = request.form.get('harga')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "update Sampah set nama = ?, unit = ?, harga = ? WHERE id = ?",
            (nama, unit, harga, id)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('dataSampah'))

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
if __name__ == '__main__':
    os.makedirs('database', exist_ok=True)
    app.run(debug=True)
