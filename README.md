 Turkish Rock Social Network Analysis

This project performs a graph-based social network analysis of Turkish Rock artist collaborations. 
Using data collected from Spotify and MusicBrainz APIs, a collaboration network was constructed to analyze artist relationships and identify influential figures within the genre.

The network was modeled using NetworkX, and advanced graph metrics were computed to evaluate structural properties of the collaboration network. The final network was exported and visualized using Gephi for deeper structural analysis.

 Objectives

- Construct a collaboration network of Turkish Rock artists
- Analyze influence using centrality metrics
- Identify key artists in the network structure
- Visualize network topology using Gephi
- Perform data cleaning and normalization on API data


Technologies & Tools

- Python
- NetworkX
- Spotipy (Spotify API Wrapper)
- MusicBrainz API
- Gephi (for network visualization)

 Methodology
 Data Collection
- Artist and collaboration data were collected using:
  - Spotify API (via Spotipy)
  - MusicBrainz API
- Collaboration relationships were extracted based on shared tracks and metadata.

Data Cleaning & Preprocessing
- Removed duplicate collaborations
- Normalized artist names
- Filtered incomplete or inconsistent records
- Constructed an edge list representing artist collaborations

Graph Construction
- Built an undirected graph using NetworkX
- Nodes represent artists
- Edges represent collaboration relationships
- Edge weights represent collaboration frequency

 Network Metrics Computed
- Degree Centrality
- Betweenness Centrality
- Closeness Centrality
- Graph density
- Connected components analysis

 Network Visualization
- Exported graph data as .gexf format
- Imported network into Gephi
- Applied layout algorithms (e.g., ForceAtlas2)
- Adjusted node size based on centrality scores
- Applied community-based coloring

Key Insights

- Identified highly central artists based on degree and betweenness metrics
- Observed clustering behavior within sub-genres
- Detected structural hubs connecting different artist communities
