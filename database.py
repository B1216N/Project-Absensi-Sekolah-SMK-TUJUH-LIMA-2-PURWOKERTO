import sqlite3

def init_db():
    conn = sqlite3.connect('absensi.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nis TEXT NOT NULL,
            nama TEXT NOT NULL,
            jurusan TEXT NOT NULL,
            kelas TEXT NOT NULL,
            tanggal_hadir TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_absen(nis, nama, jurusan, kelas, tanggal_hadir):
    conn = sqlite3.connect('absensi.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO absensi (nis, nama, jurusan, kelas, tanggal_hadir)
        VALUES (?, ?, ?, ?, ?)
    ''', (nis, nama, jurusan, kelas, tanggal_hadir))
    conn.commit()
    conn.close()

def get_today_absen(tanggal):
    conn = sqlite3.connect('absensi.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nis, nama, jurusan, kelas, tanggal_hadir FROM absensi
        WHERE tanggal_hadir LIKE ?
    ''', (f'{tanggal}%',))
    rows = cursor.fetchall()
    conn.close()
    return rows
