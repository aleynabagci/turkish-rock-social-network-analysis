import pandas as pd
import networkx as nx
from unidecode import unidecode

# =========================
# 1. Yardımcı fonksiyonlar
# =========================

def normalize_name(name):
    """
    İsimleri tek tipe indirger:
    - Baştaki/sondaki boşlukları siler
    - Türkçe karakterleri korur
    - Büyük/küçük harf tutarlılığı sağlar
    """
    name = name.strip()
    name = " ".join(name.split())  # fazla boşlukları sil
    return name.title()

# =========================
# 2. CSV'yi oku ve temizle
# =========================

df = pd.read_csv("turkish_rock_edges.csv")

df["artist_1"] = df["artist_1"].apply(normalize_name)
df["artist_2"] = df["artist_2"].apply(normalize_name)

# =========================
# 3. Yönsüz ve birleşmiş edge yapısı
# =========================

edge_weights = {}

for _, row in df.iterrows():
    a, b, w = row["artist_1"], row["artist_2"], row["weight"]

    if a == b:
        continue  # kendisiyle işbirliği varsa atla

    key = tuple(sorted([a, b]))  # (A,B) == (B,A)
    edge_weights[key] = edge_weights.get(key, 0) + w

# =========================
# 4. Graph oluştur
# =========================

G = nx.Graph()

for (a, b), w in edge_weights.items():
    G.add_edge(a, b, weight=w)

print(f"Toplam node sayısı: {G.number_of_nodes()}")
print(f"Toplam edge sayısı: {G.number_of_edges()}")

# =========================
# 5. Merkeziyet ölçümleri
# =========================

degree = dict(G.degree())
weighted_degree = dict(G.degree(weight="weight"))
betweenness = nx.betweenness_centrality(G, weight="weight")
closeness = nx.closeness_centrality(G)

# =========================
# 6. Node tablosu oluştur
# =========================

nodes_df = pd.DataFrame({
    "artist": list(G.nodes()),
    "degree": [degree[n] for n in G.nodes()],
    "weighted_degree": [weighted_degree[n] for n in G.nodes()],
    "betweenness": [betweenness[n] for n in G.nodes()],
    "closeness": [closeness[n] for n in G.nodes()]
})

nodes_df = nodes_df.sort_values("weighted_degree", ascending=False)

nodes_df.to_csv("node_metrics.csv", index=False, encoding="utf-8-sig")

# =========================
# 7. En güçlü işbirliği yapan kişi
# =========================

top_artist = nodes_df.iloc[0]

print("\n🎸 En çok işbirliği yapan sanatçı:")
print(f"İsim: {top_artist['artist']}")
print(f"Toplam işbirliği (weighted): {top_artist['weighted_degree']}")

# =========================
# 8. Gephi için çıktı
# =========================

nx.write_gexf(G, "turkish_rock_network.gexf")

print("\n✅ Gephi dosyası oluşturuldu: turkish_rock_network.gexf")
print("✅ Node metrikleri: node_metrics.csv")
