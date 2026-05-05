# -*- coding: utf-8 -*-
"""
Created on Tue May  5 15:38:47 2026

@author: Yusuf Nart Tokgöz
"""
import csv
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# --- File Paths ---
csv_file_path = "data/marmaracargo_edges.csv"
img_output_path = "results/marmaracargo_network_visualization.png"


# --- Graph Initialization & Data Loading ---
G = nx.DiGraph()
NODE_LABELS = {}

with open(csv_file_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        src = row["source_node"]
        tgt = row["target_node"]
        weight = int(row["travel_time_minutes"])
        route = row["route_type"]
        
        # Create dynamic labels with line breaks for visualization
        if src not in NODE_LABELS:
            src_label = row.get("source_label", src).replace(" (", "\n(").replace(" - ", "\n")
            NODE_LABELS[src] = f"{src}\n{src_label}"
            G.add_node(src)
            
        if tgt not in NODE_LABELS:
            tgt_label = row.get("target_label", tgt).replace(" (", "\n(").replace(" - ", "\n")
            NODE_LABELS[tgt] = f"{tgt}\n{tgt_label}"
            G.add_node(tgt)

        G.add_edge(src, tgt, weight=weight, route_type=route)

# --- Dijkstra's Algorithm ---
SOURCE = "N0"
TARGET = "N6"

shortest_path = nx.dijkstra_path(G, source=SOURCE, target=TARGET, weight="weight")
shortest_time = nx.dijkstra_path_length(G, source=SOURCE, target=TARGET, weight="weight")

# =============================================================================
# CONSOLE OUTPUT & SAVING TO TXT
# =============================================================================
output_lines = []
output_lines.append("=" * 65)
output_lines.append("  MarmaraCargo | Shortest Path Analysis Results")
output_lines.append("=" * 65)
output_lines.append(f"Target Delivery : {SOURCE} -> {TARGET}")
output_lines.append(f"Fastest Route   : {' -> '.join(shortest_path)}")
output_lines.append(f"Total Time      : {shortest_time} minutes\n")

output_lines.append("--- Step-by-Step Route Details ---")
output_lines.append(f"{'Step':<6} {'From':<6} {'To':<6} {'Time (min)':<12} {'Route Type'}")
output_lines.append("-" * 65)
for i in range(len(shortest_path) - 1):
    u, v = shortest_path[i], shortest_path[i + 1]
    w = G[u][v]["weight"]
    rt = G[u][v]["route_type"]
    output_lines.append(f"{i+1:<6} {u:<6} {v:<6} {w:<12} {rt}")
output_lines.append("-" * 65)
output_lines.append(f"{'':<6} {'':<6} TOTAL: {shortest_time} min\n")

output_lines.append("--- Alternative Routes Comparison ---")
all_paths = list(nx.all_simple_paths(G, source=SOURCE, target=TARGET))
path_results = []
for p in all_paths:
    total = sum(G[p[j]][p[j+1]]["weight"] for j in range(len(p)-1))
    path_results.append((p, total))
path_results.sort(key=lambda x: x[1])

output_lines.append(f"{'#':<4} {'Route':<35} {'Total Time (min)'}")
output_lines.append("-" * 65)
for idx, (p, t) in enumerate(path_results):
    marker = "  <-- FASTEST" if idx == 0 else ""
    output_lines.append(f"{idx+1:<4} {' -> '.join(p):<35} {t}{marker}")
output_lines.append("=" * 65 + "\n")

#Print the output to the terminal.
final_output = "\n".join(output_lines)
print(final_output)

# Save the output to solution_output.txt 
txt_output_path = "results/solution_output.txt"
with open(txt_output_path, "w", encoding="utf-8") as text_file:
    text_file.write(final_output)
    

# =============================================================================
# VISUALIZATION
# =============================================================================

pos = {
    "N0": (0, 1), "N1": (1.5, 2), "N2": (1.5, 0), "N3": (3, 2),
    "N4": (3, 0), "N5": (4.2, 1), "N6": (6, 1)
}

fig, ax = plt.subplots(figsize=(15, 8))
fig.patch.set_facecolor("#F4F6F9")
ax.set_facecolor("#F4F6F9")

shortest_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
other_edges = [e for e in G.edges() if e not in shortest_edges]

# Draw other edges
nx.draw_networkx_edges(
    G, pos, edgelist=other_edges, ax=ax, edge_color="#AAAAAA", 
    arrows=True, arrowsize=20, width=1.5, connectionstyle="arc3,rad=0.08"
)

# Draw shortest path edges
nx.draw_networkx_edges(
    G, pos, edgelist=shortest_edges, ax=ax, edge_color="#E63946", 
    arrows=True, arrowsize=25, width=4.0, connectionstyle="arc3,rad=0.08"
)

# Color nodes
node_colors = [
    "#2A9D8F" if n == SOURCE else 
    "#E63946" if n == TARGET else 
    "#F4A261" if n in shortest_path else "#ADB5BD" 
    for n in G.nodes()
]

nx.draw_networkx_nodes(
    G, pos, ax=ax, node_color=node_colors, node_size=3500, 
    edgecolors="#333333", linewidths=2
)

nx.draw_networkx_labels(
    G, pos, labels=NODE_LABELS, ax=ax, font_size=7, 
    font_weight="bold", font_color="#1A1A2E"
)

edge_labels = {(u, v): f"{d['weight']} min" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, ax=ax, font_size=8, font_color="#333333",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#CCCCCC", alpha=0.85),
    label_pos=0.38
)

ax.set_title(
    "MarmaraCargo | Anatolian Side Logistics Network Model\n"
    "Fastest Delivery Route with Dijkstra's Algorithm",
    fontsize=14, fontweight="bold", color="#1A1A2E", pad=18
)

legend_handles = [
    mpatches.Patch(color="#2A9D8F", label="Start: N0"),
    mpatches.Patch(color="#E63946", label="Target: N6"),
    mpatches.Patch(color="#F4A261", label="Nodes on Fastest Route"),
    mpatches.Patch(color="#ADB5BD", label="Other Nodes"),
    mpatches.Patch(color="#E63946", label=f"Route: {' > '.join(shortest_path)} | {shortest_time} min"),
]
ax.legend(handles=legend_handles, loc="upper left", fontsize=8, framealpha=0.92, edgecolor="#CCCCCC", facecolor="white")

ax.axis("off")
plt.tight_layout(pad=1.5)

# Save the visualization directly to the specific folder
plt.savefig(img_output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()

print(f"[*] Visualization successfully saved to:\n    {img_output_path}")