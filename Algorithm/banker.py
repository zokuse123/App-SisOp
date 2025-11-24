"""
File: algorithms/banker.py
Deskripsi: Implementasi lengkap Banker's Algorithm untuk deadlock avoidance
Author: Sistem Operasi 2025
"""

class BankerAlgorithm:
    """
    Kelas untuk mengimplementasikan Banker's Algorithm
    """
    
    def __init__(self, n_processes, n_resources, allocation, max_matrix, available):
        """
        Inisialisasi data sistem
        
        Parameters:
        - n_processes: Jumlah proses
        - n_resources: Jumlah tipe resource
        - allocation: Matriks alokasi saat ini (n x m)
        - max_matrix: Matriks kebutuhan maksimum (n x m)
        - available: Vektor resource yang tersedia (m)
        """
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.allocation = [row[:] for row in allocation]  # Deep copy
        self.max_matrix = [row[:] for row in max_matrix]
        self.available = available[:]
        
    def calculate_need(self):
        """
        Menghitung matriks Need = Max - Allocation
        
        Returns:
        - need: Matriks need (n x m)
        """
        need = []
        for i in range(self.n_processes):
            need_row = []
            for j in range(self.n_resources):
                need_val = self.max_matrix[i][j] - self.allocation[i][j]
                need_row.append(need_val)
            need.append(need_row)
        return need
    
    def check_safety(self):
        """
        Safety Algorithm: Mengecek apakah sistem dalam safe state
        
        Returns:
        - is_safe: Boolean, True jika sistem aman
        - safe_sequence: List urutan proses yang aman
        - steps: List detail langkah-langkah eksekusi
        """
        # Inisialisasi
        work = self.available[:]  # Copy available ke work
        finish = [False] * self.n_processes
        safe_sequence = []
        steps = []
        need = self.calculate_need()
        
        # Catat langkah awal
        steps.append({
            'step': 0,
            'work': work[:],
            'finish': finish[:],
            'message': 'Inisialisasi: Work = Available, Finish = [False, ...]'
        })
        
        # Algoritma utama
        step_count = 1
        while len(safe_sequence) < self.n_processes:
            found = False
            
            for i in range(self.n_processes):
                if not finish[i]:
                    # Cek apakah Need[i] <= Work
                    can_execute = True
                    for j in range(self.n_resources):
                        if need[i][j] > work[j]:
                            can_execute = False
                            break
                    
                    if can_execute:
                        # Proses i dapat dieksekusi
                        for j in range(self.n_resources):
                            work[j] += self.allocation[i][j]
                        
                        finish[i] = True
                        safe_sequence.append(i)
                        found = True
                        
                        steps.append({
                            'step': step_count,
                            'process': i,
                            'need': need[i][:],
                            'work_before': [work[j] - self.allocation[i][j] for j in range(self.n_resources)],
                            'allocation': self.allocation[i][:],
                            'work_after': work[:],
                            'message': f'Proses P{i} dapat dieksekusi (Need <= Work). Work = Work + Allocation[{i}]'
                        })
                        step_count += 1
                        break
            
            # Jika tidak ada proses yang bisa dieksekusi, sistem tidak aman
            if not found:
                return False, [], steps
        
        # Jika semua proses selesai, sistem aman
        return True, safe_sequence, steps
    
    def display_matrices(self):
        """
        Utility function untuk menampilkan matriks dalam format string
        """
        need = self.calculate_need()
        
        result = "=" * 70 + "\n"
        result += "MATRIKS SISTEM\n"
        result += "=" * 70 + "\n\n"
        
        result += "Allocation Matrix:\n"
        for i, row in enumerate(self.allocation):
            result += f"P{i}: {row}\n"
        
        result += "\nMax Matrix:\n"
        for i, row in enumerate(self.max_matrix):
            result += f"P{i}: {row}\n"
        
        result += "\nNeed Matrix:\n"
        for i, row in enumerate(need):
            result += f"P{i}: {row}\n"
        
        result += f"\nAvailable: {self.available}\n"
        result += "=" * 70 + "\n"
        
        return result


# Testing function (untuk test manual)
def test_banker():
    """
    Fungsi test dengan data contoh dari soal
    """
    print("🧪 Testing Banker's Algorithm")
    print("=" * 70)
    
    # Data contoh
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    
    available = [3, 3, 2]
    
    banker = BankerAlgorithm(5, 3, allocation, max_matrix, available)
    
    print(banker.display_matrices())
    
    is_safe, safe_seq, steps = banker.check_safety()
    
    if is_safe:
        print("✅ Sistem dalam kondisi AMAN (Safe State)")
        print(f"Safe Sequence: P{' → P'.join(map(str, safe_seq))}")
    else:
        print("❌ Sistem dalam kondisi TIDAK AMAN (Unsafe State)")
    
    print("\n📋 Detail Langkah-langkah:")
    for step in steps:
        print(f"\nStep {step['step']}: {step['message']}")
        if 'work_after' in step:
            print(f"  Work: {step['work_after']}")


if __name__ == "__main__":
    test_banker()