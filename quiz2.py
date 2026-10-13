import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# 1. Definisi titik sudut segitiga awal dalam Koordinat Homogen [x, y, 1]^T
# Setiap kolom merepresentasikan satu titik sudut: A(10,10), B(30,10), C(20,30)
labels = ['A', 'B', 'C']
triangle_orig = np.array([
    [10, 30, 20],  # Koordinat X
    [10, 10, 30],  # Koordinat Y
    [ 1,  1,  1]   # Faktor Homogen (w = 1)
], dtype=float)

# Parameter Shear sesuai soal
sh_x = 1.5
sh_y = 0.5

# 2. Penyusunan Matriks Transformasi Homogen (3x3)
M_shear_x = np.array([
    [1,    sh_x, 0],
    [0,    1,    0],
    [0,    0,    1]
])

M_shear_y = np.array([
    [1,    0,    0],
    [sh_y, 1,    0],
    [0,    0,    1]
])

M_shear_xy = np.array([
    [1,    sh_x, 0],
    [sh_y, 1,    0],
    [0,    0,    1]
])

# 3. Eksekusi Perkalian Matriks: P' = M @ P
triangle_shx  = M_shear_x  @ triangle_orig
triangle_shy  = M_shear_y  @ triangle_orig
triangle_shxy = M_shear_xy @ triangle_orig

# Cetak hasil koordinat ke konsol/terminal
def print_coords(title, matrix, suffix=""):
    print(f"=== {title} ===")
    for i, label in enumerate(labels):
        x, y = matrix[0, i], matrix[1, i]
        print(f"  {label}{suffix} = ({x:.1f}, {y:.1f})")
    print()

print_coords("Objek Segitiga Awal", triangle_orig)
print_coords("Hasil Shear Sumbu-X (shx = 1.5)", triangle_shx, "'")
print_coords("Hasil Shear Sumbu-Y (shy = 0.5)", triangle_shy, "''")
print_coords("Hasil Shear Simultan X & Y", triangle_shxy, "'''")

# 4. Fungsi Pembantu untuk Menggambar Segitiga pada Bidang Kartesius
def plot_triangle(ax, pts_orig, pts_trans, title, color_trans, suffix="'"):
    # Mengambil pasangan (x, y) untuk poligon
    xy_orig  = pts_orig[:2, :].T
    xy_trans = pts_trans[:2, :].T
    
    # Gambar poligon awal (biru putus-putus) dan hasil transformasi
    poly_orig = Polygon(xy_orig, closed=True, fill=True, facecolor='skyblue', 
                        edgecolor='navy', alpha=0.4, linestyle='--', linewidth=1.8, label='Objek Awal')
    poly_trans = Polygon(xy_trans, closed=True, fill=True, facecolor=color_trans, 
                         edgecolor='black', alpha=0.6, linewidth=2, label='Hasil Shear')
    
    ax.add_patch(poly_orig)
    ax.add_patch(poly_trans)
    
    # Plot titik sudut dan anotasi koordinat
    for i, lbl in enumerate(labels):
        # Titik awal
        ox, oy = xy_orig[i]
        ax.plot(ox, oy, 'bo', markersize=5)
        ax.annotate(f"{lbl}({int(ox)},{int(oy)})", (ox, oy), textcoords="offset points", 
                    xytext=(0, -14), ha='center', fontsize=8.5, color='navy')
        
        # Titik hasil transformasi
        tx, ty = xy_trans[i]
        ax.plot(tx, ty, 'ko', markersize=5)
        ax.annotate(f"{lbl}{suffix}({int(tx)},{int(ty)})", (tx, ty), textcoords="offset points", 
                    xytext=(0, 8), ha='center', fontsize=9, fontweight='bold')

    ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
    ax.set_xlim(0, 75)
    ax.set_ylim(0, 50)
    ax.set_xlabel("Sumbu-X")
    ax.set_ylabel("Sumbu-Y")
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.set_aspect('equal', adjustable='box')
    ax.legend(loc='upper left', fontsize=8.5)

# 5. Render Visualisasi dalam 3 Subplot
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Visualisasi Quiz #2: Transformasi Shear 2D pada Segitiga", fontsize=14, fontweight='bold')

plot_triangle(axes[0], triangle_orig, triangle_shx, 
              "1. Shear terhadap Sumbu-X (shx = 1.5)", 'salmon', "'")
plot_triangle(axes[1], triangle_orig, triangle_shy, 
              "2. Shear terhadap Sumbu-Y (shy = 0.5)", 'lightgreen', "''")
plot_triangle(axes[2], triangle_orig, triangle_shxy, 
              "3. Shear Simultan Sumbu X & Y", 'gold', "'''")

plt.tight_layout()
plt.show()