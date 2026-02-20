# =========================================================
# TURKISH ROCK COLLABORATION NETWORK (SEED BASED - FINAL)
# =========================================================

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import networkx as nx
import unidecode
import time


# =========================================================
# 1. SPOTIFY API BİLGİLERİ
# =========================================================
CLIENT_ID = ""
CLIENT_SECRET = ""
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ),
    requests_timeout=20,
    retries=10
)


# =========================================================
# 2. SEED ARTIST LİSTESİ
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
    "Kramp",
    "Pentagram",
    "Teoman",
    "Şebnem Ferah",
    "Özlem Tekin",
    "Kıraç",
    "Demir Demirkan",
    "Haluk Levent",
    "İlhan Şeşen",
    "Duman",
    "Mor ve Ötesi",
    "Athena",
    "Kargo",
    "Çilekeş",
    "Kurban",
    "Vega",
    "Kesmeşeker",
    "Mavi Sakal",
    "Erişçi Grubu"
]

normalized_artists = [unidecode.unidecode(a) for a in seed_artists]


# =========================================================
# 3. SEED ARTIST ID'LERİ
# =========================================================
artist_ids = {}

for original, search in zip(seed_artists, normalized_artists):
    time.sleep(0.2)
    result = sp.search(q=search, type="artist", limit=1)
    if result["artists"]["items"]:
        artist = result["artists"]["items"][0]
        artist_ids[artist["id"]] = artist["name"]

print("Seed sanatçılar bulundu:")
for a in artist_ids.values():
    print("-", a)


# =========================================================
# 4. TRACK ÇEKME
# =========================================================
def get_artist_tracks(artist_id):
    tracks = []
    albums = sp.artist_albums(
        artist_id,
        album_type="album,single",
        limit=10
    )

    for album in albums["items"]:
        time.sleep(0.2)
        album_tracks = sp.album_tracks(album["id"])
        tracks.extend(album_tracks["items"])

    return tracks


# =========================================================
# 5. BAĞ TÜRÜ & WEIGHT
# =========================================================
def collaboration_type(track_name):
    name = track_name.lower()
    if "feat" in name:
        return "feat"
    elif "&" in name or "with" in name:
        return "joint"
    else:
        return "album"

def assign_weight(track_name):
    t = collaboration_type(track_name)
    if t == "feat":
        return 3
    elif t == "joint":
        return 2
    else:
        return 1


# =========================================================
# 6. İŞBİRLİKLERİNİ TOPLA
# =========================================================
collaborations = []

for artist_id, artist_name in artist_ids.items():
    tracks = get_artist_tracks(artist_id)

    for track in tracks:
        if len(track["artists"]) > 1:
            for other in track["artists"]:
                if other["name"] != artist_name:
                    collaborations.append({
                        "artist_1": artist_name,
                        "artist_2": other["name"],
                        "track": track["name"],
                        "type": collaboration_type(track["name"]),
                        "weight": assign_weight(track["name"])
                    })


# =========================================================
# 7. CSV ÇIKTILARI
# =========================================================
df = pd.DataFrame(collaborations)

# 🔹 DETAYLI (şarkı bazlı)
df.to_csv(
    "turkish_rock_collaboration_detailed.csv",
    index=False,
    encoding="utf-8-sig"
)

# 🔹 NETWORK ÖZET
edge_list = (
    df.groupby(["artist_1", "artist_2", "type"])["weight"]
    .sum()
    .reset_index()
)

edge_list.to_csv(
    "turkish_rock_collaboration_edges.csv",
    index=False,
    encoding="utf-8-sig"
)


# =========================================================
# 8. GEphi NETWORK
# =========================================================
G = nx.Graph()

for _, row in edge_list.iterrows():
    G.add_edge(
        row["artist_1"],
        row["artist_2"],
        weight=row["weight"],
        type=row["type"]
    )

nx.write_gexf(G, "turkish_rock_collaboration_network.gexf")


print("\n✅ Başarılı!")
print("📁 turkish_rock_collaboration_detailed2.csv (şarkı + bağ türü)")
print("📁 turkish_rock_collaboration_edges2.csv (özet network)")
print("📁 turkish_rock_collaboration_network2.gexf (Gephi)")
