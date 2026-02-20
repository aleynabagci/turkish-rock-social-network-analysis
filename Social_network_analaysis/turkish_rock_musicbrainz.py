# =========================================================
# TURKISH ROCK COLLABORATION NETWORK (1970–2000)
# MusicBrainz | Single File | Stable Version
# =========================================================

import time
import pandas as pd
import networkx as nx
import musicbrainzngs as mb

# =========================================================
# 1. MUSICBRAINZ USER AGENT (ZORUNLU)
# =========================================================
mb.set_useragent(
    "TurkishRockNetwork",
    "1.0",
    "@gmail.com"
)

# =========================================================
# 2. RATE LIMIT GÜVENLİ ÇAĞRI
# =========================================================
def safe_mb_call(func, *args, **kwargs):
    while True:
        try:
            time.sleep(1.2)  # MB rate limit
            return func(*args, **kwargs)
        except mb.NetworkError:
            print("⚠️ Network error, retrying in 10s...")
            time.sleep(10)

# =========================================================
# 3. SEED ARTISTS
# =========================================================
seed_artists = [
   "Barış Manço",
    "Cem Karaca",
    "Erkin Koray",
    "Moğollar",
    "Selda Bağcan",
    "Fikret Kızılok",
    "Edip Akbayram",
    "Bunalım",
    "Hardal",
    "Kurtalan Ekspres",
    "Apaşlar",
    "Kardaşlar",
    "3 Hürel",
    "Bulutsuzluk Özlemi",
    "MFÖ",
    "Whisky",
    "Pentagram",
    "Teoman",
    "Şebnem Ferah",
    "Özlem Tekin",
    "Kıraç",
    "Demir Demirkan",
    "Haluk Levent",
    "Duman",
    "Mor ve Ötesi",
    "Athena",
    "Kargo",
    "Çilekeş",
    "Kurban",
    "Kesmeşeker",
    "Mavi Sakal"]
print("\n🎸 Seed sanatçılar bulunuyor...\n")

artist_mbids = {}

for artist in seed_artists:
    res = safe_mb_call(mb.search_artists, artist=artist, limit=1)
    if res["artist-list"]:
        a = res["artist-list"][0]
        artist_mbids[a["id"]] = a["name"]
        print("✔", a["name"])

# =========================================================
# 4. RECORDINGS + YEAR (SADECE recording + artist-credit)
# =========================================================
def get_recordings_with_year(artist_mbid, max_pages=3):
    recordings = []
    offset = 0
    limit = 100

    for _ in range(max_pages):  # hız için sınır
        res = safe_mb_call(
            mb.browse_recordings,
            artist=artist_mbid,
            includes=["artist-credits"],
            limit=limit,
            offset=offset
        )

        for rec in res["recording-list"]:
            year = None

            if "first-release-date" in rec:
                try:
                    year = int(rec["first-release-date"][:4])
                except:
                    pass

            recordings.append({
                "artists": rec.get("artist-credit", []),
                "year": year
            })

        if len(res["recording-list"]) < limit:
            break

        offset += limit

    return recordings

# =========================================================
# 5. COLLABORATION TOPLAMA (1970–2000)
# =========================================================
edges = []

print("\n🔍 İş birlikleri toplanıyor...\n")

for mbid, artist_name in artist_mbids.items():
    print("▶", artist_name)
    recs = get_recordings_with_year(mbid)

    for rec in recs:
        year = rec["year"]

        if year is None or year < 1970 or year > 2000:
            continue

        artist_list = [
            c["artist"]["name"]
            for c in rec["artists"]
            if "artist" in c
        ]

        if len(artist_list) > 1:
            for other in artist_list:
                if other != artist_name:
                    edges.append({
                        "artist_1": artist_name,
                        "artist_2": other,
                        "year": year,
                        "weight": 1
                    })

# =========================================================
# 6. DATAFRAME & KONTROL
# =========================================================
df = pd.DataFrame(edges)

if df.empty:
    print("\n❌ 1970–2000 arası hiç işbirliği bulunamadı.")
    exit()

print("\n✅ Toplam işbirliği kaydı:", len(df))
print(df.head())

# =========================================================
# 7. AGGREGATION
# =========================================================
edge_list = (
    df.groupby(["artist_1", "artist_2"], as_index=False)
      .agg({
          "weight": "sum",
          "year": "min"
      })
)

# =========================================================
# 8. CSV EXPORT
# =========================================================
edge_list.to_csv(
    "turkish_rock_edges_1970_2000.csv",
    index=False,
    encoding="utf-8-sig"
)

# =========================================================
# 9. NETWORK EXPORT (GEPHI)
# =========================================================
G = nx.Graph()

for _, row in edge_list.iterrows():
    G.add_edge(
        row["artist_1"],
        row["artist_2"],
        weight=row["weight"],
        year=row["year"]
    )

nx.write_gexf(G, "turkish_rock_network_1970_2000.gexf")

print("\n🎉 TAMAMLANDI")
print("📁 turkish_rock_edges_1970_2000.csv")
print("📁 turkish_rock_network_1970_2000.gexf")
