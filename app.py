from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Simulasi database di memori
absensi_history = []

@app.route('/')
def siswa_page():
    return render_template('index.html')

@app.route('/guru')
def guru_page():
    return render_template('guru.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    nama_siswa = data.get('nama_siswa')

    if not nama_siswa:
        return jsonify({'status': 'error', 'message': 'Nama siswa tidak ditemukan'}), 400

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    absensi_history.append({'nama': nama_siswa, 'waktu': waktu})

    return jsonify({'status': 'success', 'nama': nama_siswa, 'waktu': waktu})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(absensi_history)
