from flask import Flask, render_template, request, redirect, url_for
from Algorithm.banker import BankerAlgorithm
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Halaman utama dengan form input"""
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    """Proses simulasi algoritma Banker"""
    try:
        # Ambil data dari form
        n_processes = int(request.form.get('n_processes'))
        n_resources = int(request.form.get('n_resources'))
        
        # Parse matriks Allocation
        allocation = []
        for i in range(n_processes):
            row = []
            for j in range(n_resources):
                val = int(request.form.get(f'allocation_{i}_{j}', 0))
                row.append(val)
            allocation.append(row)
        
        # Parse matriks Max
        max_matrix = []
        for i in range(n_processes):
            row = []
            for j in range(n_resources):
                val = int(request.form.get(f'max_{i}_{j}', 0))
                row.append(val)
            max_matrix.append(row)
        
        # Parse vektor Available
        available = []
        for j in range(n_resources):
            val = int(request.form.get(f'available_{j}', 0))
            available.append(val)
        
        # Jalankan algoritma Banker
        banker = BankerAlgorithm(n_processes, n_resources, allocation, max_matrix, available)
        is_safe, safe_sequence, steps = banker.check_safety()
        need_matrix = banker.calculate_need()
        
        # Kirim hasil ke halaman result
        return render_template('result.html',
                             n_processes=n_processes,
                             n_resources=n_resources,
                             allocation=allocation,
                             max_matrix=max_matrix,
                             need=need_matrix,
                             available=available,
                             is_safe=is_safe,
                             safe_sequence=safe_sequence,
                             steps=steps)
    
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Simulasi Algoritma Banker - Sistem Operasi 2025")
    print("=" * 60)
    print("📌 Server berjalan di: http://localhost:5000")
    print("📌 Tekan Ctrl+C untuk menghentikan server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)