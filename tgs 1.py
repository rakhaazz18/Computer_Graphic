"""Aplikasi simulasi Clipping Garis (Cohen-Sutherland & Liang-Barsky) dengan Tkinter."""
import tkinter as tk
from tkinter import colorchooser, ttk
from dataclasses import dataclass
from typing import Optional

Titik = tuple[float, float]
Segmen = tuple[Titik, Titik]


# ---------------------------------------------------------------- Model data
@dataclass
class Garis:
    x1: float
    y1: float
    x2: float
    y2: float
    warna: str = "#0000cc"
    tebal: int = 2


@dataclass
class Area:
    xmin: float
    ymin: float
    xmax: float
    ymax: float


# ---------------------------------------------------------------- Algoritma
INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8


def _kode(x: float, y: float, a: Area) -> int:
    """Hitung outcode Cohen-Sutherland (sumbu y kanvas mengarah ke bawah)."""
    kode = INSIDE
    if x < a.xmin:
        kode |= LEFT
    elif x > a.xmax:
        kode |= RIGHT
    if y < a.ymin:
        kode |= TOP
    elif y > a.ymax:
        kode |= BOTTOM
    return kode


def cohen_sutherland(g: Garis, a: Area) -> Optional[Segmen]:
    x1, y1, x2, y2 = g.x1, g.y1, g.x2, g.y2
    k1, k2 = _kode(x1, y1, a), _kode(x2, y2, a)
    while True:
        if not (k1 | k2):          # keduanya di dalam
            return (x1, y1), (x2, y2)
        if k1 & k2:                # keduanya di sisi luar yang sama
            return None
        k = k1 or k2
        if k & TOP:
            x = x1 + (x2 - x1) * (a.ymin - y1) / (y2 - y1)
            y = a.ymin
        elif k & BOTTOM:
            x = x1 + (x2 - x1) * (a.ymax - y1) / (y2 - y1)
            y = a.ymax
        elif k & RIGHT:
            y = y1 + (y2 - y1) * (a.xmax - x1) / (x2 - x1)
            x = a.xmax
        else:  # LEFT
            y = y1 + (y2 - y1) * (a.xmin - x1) / (x2 - x1)
            x = a.xmin
        if k == k1:
            x1, y1, k1 = x, y, _kode(x, y, a)
        else:
            x2, y2, k2 = x, y, _kode(x, y, a)


def liang_barsky(g: Garis, a: Area) -> Optional[Segmen]:
    dx, dy = g.x2 - g.x1, g.y2 - g.y1
    p = (-dx, dx, -dy, dy)
    q = (g.x1 - a.xmin, a.xmax - g.x1, g.y1 - a.ymin, a.ymax - g.y1)
    u1, u2 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if pi == 0:
            if qi < 0:
                return None        # sejajar dan di luar
        else:
            u = qi / pi
            if pi < 0:
                if u > u2:
                    return None
                u1 = max(u1, u)
            else:
                if u < u1:
                    return None
                u2 = min(u2, u)
    return ((g.x1 + u1 * dx, g.y1 + u1 * dy),
            (g.x1 + u2 * dx, g.y1 + u2 * dy))


# ---------------------------------------------------------------- Aplikasi
class AplikasiClipping(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Clipping Garis")
        self.geometry("1000x600")
        self.minsize(900, 520)

        # State
        self.daftar_garis: list[Garis] = []
        self.area: Optional[Area] = None
        self.bentuk: list[tuple[str, tuple[float, float, float, float], str, int]] = []
        self.urutan_alat: list[str] = []      # alat yang dicentang, terakhir = aktif
        self.titik_awal: Optional[Titik] = None
        self.warna = "#0000cc"

        # Variabel widget
        self.var_alat = {n: tk.BooleanVar() for n in
                         ("garis", "area", "kotak", "lingkaran")}
        self.var_algo = tk.StringVar(value="cohen")
        self.var_tebal = tk.IntVar(value=2)

        self._bangun_ui()

    # ------------------------------------------------------------ UI
    def _bangun_ui(self) -> None:
        luar = ttk.Frame(self, padding=8)
        luar.pack(fill="both", expand=True)
        luar.columnconfigure(0, weight=1)
        luar.columnconfigure(1, weight=1)
        luar.columnconfigure(2, weight=1, minsize=280)
        luar.rowconfigure(1, weight=1)
        luar.rowconfigure(2, weight=1)

        # Grup "Buat" (checkbox)
        g_buat = ttk.LabelFrame(luar, text="Buat", padding=4)
        g_buat.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        label_alat = [("garis", "Garis"), ("area", "Area Clipping"),
                      ("kotak", "Kotak (opsional)"),
                      ("lingkaran", "Lingkaran (opsional)")]
        for kunci, teks in label_alat:
            ttk.Checkbutton(
                g_buat, text=teks, variable=self.var_alat[kunci],
                command=lambda k=kunci: self._alat_berubah(k),
            ).pack(anchor="w")

        # Grup "Algoritma" (radio)
        g_algo = ttk.LabelFrame(luar, text="Algoritma", padding=4)
        g_algo.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        for nilai, teks in (("cohen", "Cohen-Sutherland"),
                            ("liang", "Liang-Barsky")):
            ttk.Radiobutton(g_algo, text=teks, value=nilai,
                            variable=self.var_algo,
                            command=self._gambar_ulang).pack(anchor="w", pady=2)

        # Grup atribut warna & ketebalan
        g_atribut = ttk.LabelFrame(luar, text="Atribut Warna dan Ketebalan",
                                   padding=4)
        g_atribut.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
        baris = ttk.Frame(g_atribut)
        baris.pack(anchor="w")
        self.tombol_warna = tk.Button(baris, text="Warna", width=8,
                                      bg=self.warna, fg="white",
                                      command=self._pilih_warna)
        self.tombol_warna.pack(side="left", padx=2)
        ttk.Label(baris, text="Tebal:").pack(side="left", padx=(8, 2))
        ttk.Spinbox(baris, from_=1, to=10, width=4,
                    textvariable=self.var_tebal).pack(side="left")
        ttk.Button(g_atribut, text="Hapus Semua",
                   command=self._hapus_semua).pack(anchor="w", pady=(6, 0), padx=2)

        # Kanvas
        self.kanvas = tk.Canvas(luar, bg="white", highlightthickness=1,
                                highlightbackground="#555")
        self.kanvas.grid(row=1, column=0, columnspan=2, rowspan=2,
                         sticky="nsew", padx=2, pady=2)
        self.kanvas.bind("<ButtonPress-1>", self._mouse_tekan)
        self.kanvas.bind("<B1-Motion>", self._mouse_geser)
        self.kanvas.bind("<ButtonRelease-1>", self._mouse_lepas)

        # Daftar sebelum & sesudah clipping
        self.lb_sebelum = self._buat_daftar(luar, "Daftar Garis sebelum Clipping", 1)
        self.lb_sesudah = self._buat_daftar(luar, "Daftar Garis setelah Clipping", 2)

    @staticmethod
    def _buat_daftar(induk: ttk.Frame, judul: str, baris: int) -> tk.Listbox:
        grup = ttk.LabelFrame(induk, text=judul, padding=4)
        grup.grid(row=baris, column=2, sticky="nsew", padx=2, pady=2)
        grup.rowconfigure(0, weight=1)
        grup.columnconfigure(0, weight=1)
        lb = tk.Listbox(grup, height=6, activestyle="none")
        sb = ttk.Scrollbar(grup, orient="vertical", command=lb.yview)
        lb.configure(yscrollcommand=sb.set)
        lb.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        return lb

    # ------------------------------------------------------------ Event
    def _alat_berubah(self, kunci: str) -> None:
        """Perbarui urutan alat: alat aktif = yang terakhir dicentang."""
        if self.var_alat[kunci].get():
            self.urutan_alat.append(kunci)
        elif kunci in self.urutan_alat:
            self.urutan_alat.remove(kunci)

    def _alat_aktif(self) -> Optional[str]:
        return self.urutan_alat[-1] if self.urutan_alat else None

    def _pilih_warna(self) -> None:
        hasil = colorchooser.askcolor(color=self.warna, title="Pilih warna")
        if hasil[1]:
            self.warna = hasil[1]
            self.tombol_warna.configure(bg=self.warna)

    def _hapus_semua(self) -> None:
        self.daftar_garis.clear()
        self.bentuk.clear()
        self.area = None
        self._gambar_ulang()

    def _mouse_tekan(self, e: tk.Event) -> None:
        if self._alat_aktif():
            self.titik_awal = (e.x, e.y)

    def _mouse_geser(self, e: tk.Event) -> None:
        if not self.titik_awal or not self._alat_aktif():
            return
        self.kanvas.delete("pratinjau")
        self._gambar_bentuk(self._alat_aktif(), self.titik_awal, (e.x, e.y),
                            self.warna, self.var_tebal.get(), "pratinjau",
                            putus=True)

    def _mouse_lepas(self, e: tk.Event) -> None:
        alat = self._alat_aktif()
        if not self.titik_awal or not alat:
            return
        (x1, y1), (x2, y2) = self.titik_awal, (e.x, e.y)
        self.titik_awal = None
        self.kanvas.delete("pratinjau")
        if (x1, y1) == (x2, y2):
            return
        tebal = max(1, self.var_tebal.get())
        if alat == "garis":
            self.daftar_garis.append(Garis(x1, y1, x2, y2, self.warna, tebal))
        elif alat == "area":
            self.area = Area(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        else:
            self.bentuk.append((alat, (x1, y1, x2, y2), self.warna, tebal))
        self._gambar_ulang()

    # ------------------------------------------------------------ Gambar
    def _gambar_bentuk(self, alat: str, p1: Titik, p2: Titik, warna: str,
                       tebal: int, tag: str, putus: bool = False) -> None:
        opsi = dict(fill="", outline=warna, width=tebal, tags=tag)
        if putus:
            opsi["dash"] = (4, 3)
        if alat == "garis":
            self.kanvas.create_line(*p1, *p2, fill=warna, width=tebal, tags=tag,
                                    dash=(4, 3) if putus else None)
        elif alat in ("area", "kotak"):
            self.kanvas.create_rectangle(*p1, *p2, **opsi)
        elif alat == "lingkaran":
            r = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
            self.kanvas.create_oval(p1[0] - r, p1[1] - r, p1[0] + r, p1[1] + r,
                                    **opsi)

    def _clip(self, g: Garis) -> Optional[Segmen]:
        fungsi = cohen_sutherland if self.var_algo.get() == "cohen" else liang_barsky
        return fungsi(g, self.area)

    def _gambar_ulang(self) -> None:
        self.kanvas.delete("all")
        self.lb_sebelum.delete(0, "end")
        self.lb_sesudah.delete(0, "end")

        for alat, (x1, y1, x2, y2), warna, tebal in self.bentuk:
            self._gambar_bentuk(alat, (x1, y1), (x2, y2), warna, tebal, "bentuk")

        if self.area:
            a = self.area
            self.kanvas.create_rectangle(a.xmin, a.ymin, a.xmax, a.ymax,
                                         outline="#d00000", width=2, dash=(6, 3))

        for i, g in enumerate(self.daftar_garis, start=1):
            self.lb_sebelum.insert(
                "end", f"G{i}: ({g.x1:.0f},{g.y1:.0f}) - ({g.x2:.0f},{g.y2:.0f})")
            if not self.area:
                self.kanvas.create_line(g.x1, g.y1, g.x2, g.y2,
                                        fill=g.warna, width=g.tebal)
                continue
            # Garis asli (redup) lalu bagian hasil clipping (tebal berwarna)
            self.kanvas.create_line(g.x1, g.y1, g.x2, g.y2,
                                    fill="#b0b0b0", dash=(3, 3))
            hasil = self._clip(g)
            if hasil:
                (cx1, cy1), (cx2, cy2) = hasil
                self.kanvas.create_line(cx1, cy1, cx2, cy2,
                                        fill=g.warna, width=g.tebal)
                self.lb_sesudah.insert(
                    "end", f"G{i}: ({cx1:.0f},{cy1:.0f}) - ({cx2:.0f},{cy2:.0f})")
            else:
                self.lb_sesudah.insert("end", f"G{i}: di luar area")


if __name__ == "__main__":
    AplikasiClipping().mainloop()