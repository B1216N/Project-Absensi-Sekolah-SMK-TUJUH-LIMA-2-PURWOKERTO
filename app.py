from flask import Flask, render_template, request, jsonify
from datetime import datetime
from database import init_db, insert_absen, get_today_absen
import ssl
import os

app = Flask(__name__)
init_db()  # Inisialisasi database saat aplikasi mulai

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

    # Simulasi data siswa (seharusnya diambil dari database siswa)
    nis = "20230001"
    jurusan = "Rekayasa Perangkat Lunak"
    kelas = "XII RPL 1"

    insert_absen(nis, nama_siswa, jurusan, kelas, waktu)

    return jsonify({'status': 'success', 'nama': nama_siswa, 'waktu': waktu})

@app.route('/history', methods=['GET'])
def get_history():
    today = datetime.now().strftime("%Y-%m-%d")
    absensi_today = get_today_absen(today)
    result = [
        {
            'nis': row[0],
            'nama': row[1],
            'jurusan': row[2],
            'kelas': row[3],
            'waktu': row[4]
        } for row in absensi_today
    ]
    return jsonify(result)

# Fungsi untuk membuat context SSL
def create_ssl_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    
    # Path ke file sertifikat dan private key
    cert_file = 'certs/cert.pem'
    key_file = 'certs/key.pem'
    
    # Cek apakah file sertifikat ada
    if os.path.exists(cert_file) and os.path.exists(key_file):
        context.load_cert_chain(cert_file, key_file)
        return context
    else:
        print("Warning: SSL certificate files not found. Creating self-signed certificate...")
        create_self_signed_cert()
        context.load_cert_chain(cert_file, key_file)
        return context

def create_self_signed_cert():
    """Membuat self-signed certificate untuk development"""
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.x509.oid import NameOID
        import datetime
        import ipaddress
        
        # Buat direktori certs jika belum ada
        os.makedirs('certs', exist_ok=True)
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Buat certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ID"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Central Java"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Purwokerto"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "School Absensi App"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Simpan private key
        with open("certs/key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Simpan certificate
        with open("certs/cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
            
        print("Self-signed certificate created successfully!")
        
    except ImportError:
        print("Error: cryptography package not installed.")
        print("Install it with: pip install cryptography")
        print("Using adhoc SSL context instead...")
        return None