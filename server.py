from app import app, create_ssl_context

if __name__ == '__main__':
    # Opsi 1: Menggunakan sertifikat SSL yang sudah ada atau self-signed
    try:
        ssl_context = create_ssl_context()
        if ssl_context:
            print("Starting HTTPS server on https://localhost:5000")
            app.run(
                host='0.0.0.0', 
                port=5000, 
                debug=True,
                ssl_context=ssl_context
            )
        else:
            # Fallback ke adhoc SSL jika pembuatan sertifikat gagal
            print("Starting HTTPS server with adhoc SSL on https://localhost:5000")
            app.run(
                host='0.0.0.0', 
                port=5000, 
                debug=True,
                ssl_context='adhoc'
            )
    except Exception as e:
        print(f"Error starting HTTPS server: {e}")
        print("Starting HTTP server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)