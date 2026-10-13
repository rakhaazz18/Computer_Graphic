
import matplotlib.pyplot as plt

# 1. Koordinat segitiga awal
triangle = {
    "A": (10, 10),
    "B": (30, 10),
    "C": (20, 30)
}

# 2. Fungsi transformasi refleksi
def reflect_x(point):
    x, y = point
    return (x, -y)

def reflect_y(point):
    x, y = point
    return (-x, y)

def reflect_y_eq_x(point):
    x, y = point
    return (y, x)

def reflect_y_eq_neg_x(point):
    x, y = point
    return (-y, -x)

# 3. Terapkan transformasi pada semua titik
transformations = {
    "Sumbu-X": reflect_x,
    "Sumbu-Y": reflect_y,
    "Garis y = x": reflect_y_eq_x,
    "Garis y = -x": reflect_y_eq_neg_x
}

results = {}

for name, function in transformations.items():
    results[name] = {
        point_name: function(coordinate)
        for point_name, coordinate in triangle.items()
    }

# 4. Cetak hasil koordinat
print("KOORDINAT SEGITIGA AWAL")
for name, point in triangle.items():
    print(f"{name} = {point}")

for name, points in results.items():
    print(f"\nREFLEKSI {name}")
    for point_name, coordinate in points.items():
        print(f"{point_name}' = {coordinate}")

# 5. Fungsi untuk menggambar segitiga
def draw_triangle(ax, points, title, color):
    names = list(points.keys())
    coordinates = [points[name] for name in names]

    # Hubungkan A-B-C-A
    closed = coordinates + [coordinates[0]]
    xs = [p[0] for p in closed]
    ys = [p[1] for p in closed]

    ax.plot(xs, ys, marker="o", color=color, linewidth=2)

    # Berikan label koordinat pada setiap titik
    for name, (x, y) in points.items():
        ax.annotate(
            f"{name} ({x}, {y})",
            (x, y),
            xytext=(5, 7),
            textcoords="offset points",
            fontsize=8
        )

    # Sumbu koordinat
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    # Garis-garis referensi refleksi
    limit = 35
    ax.plot(
        [-limit, limit], [-limit, limit],
        "--", color="gray", alpha=0.45, linewidth=1
    )
    ax.plot(
        [-limit, limit], [limit, -limit],
        "--", color="gray", alpha=0.45, linewidth=1
    )

    ax.set_title(title)
    ax.set_xlim(-35, 35)
    ax.set_ylim(-35, 35)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(range(-30, 31, 10))
    ax.set_yticks(range(-30, 31, 10))
    ax.grid(True, alpha=0.25)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

# 6. Visualisasikan segitiga awal dan hasil refleksi
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

draw_triangle(
    axes[0], triangle,
    "Segitiga Awal", "blue"
)

colors = ["red", "green", "purple", "orange"]

for ax, (name, points), color in zip(
    axes[1:],
    results.items(),
    colors
):
    draw_triangle(ax, points, name, color)

# Panel keenam tidak digunakan
axes[5].axis("off")

fig.suptitle(
    "Visualisasi Transformasi Refleksi Segitiga",
    fontsize=16
)
plt.tight_layout()

# Simpan grafik untuk laporan
plt.savefig(
    "hasil_refleksi.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
