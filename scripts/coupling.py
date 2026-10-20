stok, analitik, email_terkirim = [], [], []
email = {"down": True}  # status layanan email

def kurangi_stok(e): stok.append(e["id"])
def catat_analitik(e): analitik.append(e["id"])
def kirim_email(e):
    if email["down"] and e["id"] == 2:
        raise ConnectionError("layanan email down")
    email_terkirim.append(e["id"])

# Desain A: tightly coupled (order service memanggil semuanya langsung)
def buat_pesanan_tight(e):
    kurangi_stok(e); kirim_email(e); catat_analitik(e)

# Desain B: loosely coupled (producer -> router -> consumer)
class Router:
    def __init__(self):
        self.pelanggan, self.dlq = {}, []
        self.selesai = set()  # pasangan (nama handler, id event) yang sudah sukses

    def subscribe(self, topik, handler):
        self.pelanggan.setdefault(topik, []).append(handler)

    def _jalankan(self, h, event):
        kunci = (h.__name__, event["id"])
        if kunci in self.selesai:  # idempotent: sudah pernah sukses, lewati
            return
        try:
            h(event)
            self.selesai.add(kunci)
        except Exception as err:
            self.dlq.append({"handler": h.__name__, "event": event, "error": str(err)})

    def publish(self, topik, event):
        for h in self.pelanggan.get(topik, []):
            self._jalankan(h, event)

    def ulang_dlq(self, topik):
        """Coba ulang HANYA handler yang gagal, bukan seluruh consumer."""
        antrean, self.dlq = self.dlq, []
        for item in antrean:
            h = next(x for x in self.pelanggan[topik] if x.__name__ == item["handler"])
            self._jalankan(h, item["event"])  # gagal lagi -> kembali ke DLQ

router = Router()
for h in (kurangi_stok, kirim_email, catat_analitik):
    router.subscribe("pesanan_baru", h)

print("== Desain A ==")
for i in (1, 2, 3):
    try:
        buat_pesanan_tight({"id": i}); print(f"pesanan {i}: sukses")
    except Exception as err:
        print(f"pesanan {i}: GAGAL ({err})")
print("stok:", stok, "| analitik:", analitik)

stok.clear(); analitik.clear(); email_terkirim.clear()

print("== Desain B ==")
for i in (1, 2, 3):
    router.publish("pesanan_baru", {"id": i}); print(f"pesanan {i}: diterima")
print("stok:", stok, "| analitik:", analitik)
print("dead-letter:", router.dlq)

print("== Tugas 5: ulang_dlq ==")
print("email masih down  ->", "email:", email_terkirim, "| dlq:", len(router.dlq))
router.ulang_dlq("pesanan_baru")
print("ulang_dlq (down)  ->", "email:", email_terkirim, "| dlq:", len(router.dlq))
email["down"] = False  # layanan email diperbaiki
router.ulang_dlq("pesanan_baru")
print("ulang_dlq (pulih) ->", "email:", email_terkirim, "| dlq:", len(router.dlq))
print("stok:", stok, "| analitik:", analitik)

print("== Uji idempotent: publish ulang pesanan 2 ==")
router.publish("pesanan_baru", {"id": 2})
router.ulang_dlq("pesanan_baru")
print("stok:", stok, "| analitik:", analitik, "| email:", email_terkirim)

# --- Consumer baru: cek_fraud ---
def cek_fraud(e):
    if e["id"] % 2 == 0:
        print(f"PERINGATAN: pesanan {e['id']} dicurigai fraud (id genap)")

print("== Desain B + cek_fraud ==")
router.subscribe("pesanan_baru", cek_fraud)
for i in (4, 5, 6):
    router.publish("pesanan_baru", {"id": i}); print(f"pesanan {i}: diterima")
