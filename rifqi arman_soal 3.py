import numpy as np

# Fungsi performa pesawat
def performa_p(x1, x2):
    return -(x1 - 10)**2 - (x2 - 5)**2 + 50

# Gradien dari fungsi performa_p
def gradient(x1, x2):
    d_p_x1 = -2 * (x1 - 10)
    d_p_x2 = -2 * (x2 - 5)
    return np.array([d_p_x1, d_p_x2])

# Gradient Descent
def gradient_descent(learning_rate=0.1, tolerance=0.001, max_iterations=1000):
    # Inisialisasi variabel
    x1, x2 = 8.0, 4.0  # Tebakan awal
    iteration = 0
    while iteration < max_iterations:
        # Hitung gradien
        grad = gradient(x1, x2)
        
        # Update nilai x1 dan x2
        x1_new = x1 - learning_rate * grad[0]
        x2_new = x2 - learning_rate * grad[1]
        
        # Jika perubahan nilai sudah kecil, hentikan iterasi
        if np.linalg.norm([x1_new - x1, x2_new - x2]) < tolerance:
            break
        
        # Update nilai x1 dan x2
        x1, x2 = x1_new, x2_new
        iteration += 1
    
    return x1, x2, performa_p(x1, x2), iteration

# Menjalankan gradient descent
x1_opt, x2_opt, p_opt, iters = gradient_descent()

# Output hasil
print(f"Nilai optimal x1 (panjang sayap): {x1_opt}")
print(f"Nilai optimal x2 (sudut serang): {x2_opt}")
print(f"Performa maksimum pesawat: {p_opt}")
print(f"Jumlah iterasi: {iters}")
