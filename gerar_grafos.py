import networkx as nx
import matplotlib.pyplot as plt

def gerar_grafo(arquivo_topo, imagem_saida):
    G = nx.Graph()
    
    with open(arquivo_topo, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) == 2:
                u, v = parts[0], parts[1]
                G.add_edge(u, v)
                
                h_u = f"h{u.replace('s', '')}"
                h_v = f"h{v.replace('s', '')}"
                G.add_edge(u, h_u)
                G.add_edge(v, h_v)

    plt.figure(figsize=(8, 6))
    
    switches = [node for node in G.nodes if node.startswith('s')]
    hosts = [node for node in G.nodes if node.startswith('h')]
    
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_nodes(G, pos, nodelist=switches, node_color='skyblue', node_size=1200, label='Switches')
    nx.draw_networkx_nodes(G, pos, nodelist=hosts, node_color='lightgreen', node_size=800, label='Hosts')
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    plt.title(f"Grafo da Topologia: {arquivo_topo}", fontsize=14)
    plt.legend()
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(imagem_saida, dpi=300)
    plt.close()
    print(f"Imagem gerada com sucesso: {imagem_saida}")

if __name__ == '__main__':
    gerar_grafo('topo_triangle.txt', 'grafo_triangle.png')
    gerar_grafo('topo_someloops.txt', 'grafo_someloops.png')
