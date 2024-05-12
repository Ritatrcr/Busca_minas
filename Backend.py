import matplotlib.pyplot as plt
import networkx as nx



# Create a graph
G = nx.Graph()

# Add nodes to the graph
num_nodes = 32
for i in range(num_nodes):
    G.add_node(i)

# Create positions for the nodes within a square layout
positions = {}
side_length = 6  # Adjust the side length as needed
for i in range(num_nodes):
    row = i // 4  # Assuming you want 4 nodes per row
    col = i % 4   # Assuming you want 4 nodes per row
    x = col * side_length
    y = row * side_length
    positions[i] = (x, y)

# Draw the graph
nx.draw(G, pos=positions, with_labels=True, node_size=500, node_color='skyblue')

# Show the plot
plt.title("Graph with 32 nodes in a square layout")
plt.show()
