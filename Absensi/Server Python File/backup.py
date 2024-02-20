import os
import sqlite3
from flask import Flask, request, jsonify,render_template,request, redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Inisialisasi Variable yang diperlukan
tempCard  = "000"
newData   = False
# Inisialisasi Database SQLite
db_path = 'absensi.db'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Halaman Utama
@app.route('/')
def index():
    return render_template('index.html')



# Halaman Registrasi
@app.route('/register',methods=('GET','POST'))
def regist():
    global tempCard
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        uname = request.form['name']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], uname+"-"+filename))
            send_from_directory(app.config["UPLOAD_FOLDER"], uname+"-"+filename)
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO data (rfid_data,fullname,photo) VALUES (?,?,?)", (tempCard,uname,uname+"-"+filename))
            connection.commit()
            connection.close()
        tempCard = "000"
        return redirect(url_for('register_success',uname=uname))
    return render_template('forms.html',cards=tempCard,name="bakhti")

# Untuk Memperbaharui Nomor Kartu pada kolom Registrasi
@app.route('/api/card_data')
def get_card_data():
    return jsonify({'card_number': tempCard})

#Menampilakan Selesai Registrasi
@app.route('/register/success/<uname>')
def register_success(uname="done"):
    return 'Registration successful!, thanks '+uname+" back to link <a href='"+url_for('index')+"'>link</a>"


# Fungsi untuk mengambil data absensi dari database
def get_absensi():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT absensi.timestamp, data.fullname, data.photo FROM absensi INNER JOIN data ON absensi.rfid_data = data.rfid_data WHERE absensi.timestamp > data.timestamp ORDER BY absensi.timestamp DESC;")
    rows = cursor.fetchall()
    connection.close()
    return rows
# New Daata Uploaded
@app.route('/api/update')
def updateDashboard():
    global newData
    return jsonify({'update': newData})

# Endpoint untuk tampilan dasbor
@app.route('/dashboard')
def dashboard():
    global newData
    newData = False
    absensi_data = get_absensi()
    return render_template('dashboard.html', absensi_data=absensi_data)

def testing():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT id, fullname, photo FROM data")
    rows = cursor.fetchall()
    connection.close()
    return rows

@app.route('/siswa')
def listSiswa():
    absensi_data = testing()
    return render_template('dashboard.html', absensi_data=absensi_data)

# def tester():
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM absensi")
#     rows = cursor.fetchall()
#     connection.close()
#     return rows

# @app.route('/tester')
# def dashs():
#     absensi_data = tester()
#     return render_template('dashboard.html', absensi_data=absensi_data)


# Membuat tabel jika belum ada
def create_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    # 
            # NISN TEXT,s
            # address TEXT,
            # Gender TEXT,
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rfid_data TEXT NOT NULL,
            fullname TEXT NOT NULL,
            photo TEXT,
            NISN TEXT,
            address TEXT,
            Gender TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rfid_data TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
    ''')
    connection.commit()
    connection.close()


# Endpoint untuk menerima data absensi dari ESP32
@app.route('/absensi', methods=['POST'])
def tambah_absensi():
    global tempCard,newData
    data = request.form.get('rfid_data')
    if not data:
        return jsonify({'status': 'error', 'message': 'Data RFID tidak lengkap'}), 400
    tempCard = data
    newData = True
    # Simpan data ke database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO absensi (rfid_data) VALUES (?)", (data,))
    connection.commit()
    connection.close()
    return jsonify({'status': 'success', 'message': 'Data absensi berhasil disimpan'}), 200


if __name__ == '__main__':
    create_table()
    app.run(host='192.168.1.200',debug=True)