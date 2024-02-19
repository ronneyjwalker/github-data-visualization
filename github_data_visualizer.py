import requests
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Gets the follower list of a user from github using api
def get_followers_list(username, token, page=1, per_page=100):
    api_url = f'https://api.github.com/users/{username}/followers'
    params = {'page': page, 'per_page': per_page}
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# Plot a graph considering each user as node
def plot_graph(username, followers_data):
    graph = nx.DiGraph()
    graph.add_node(username)

    for follower in followers_data:
        follower_username = follower['login']
        graph.add_node(follower_username)
        graph.add_edge(username, follower_username)

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightgreen', font_size=8, font_color='black', font_weight='bold', node_size=300, arrowsize=10)
    plt.title(f"GitHub Follower Network for {username}")
    plt.show()

    return graph

# Plot degree distribution based on the graph
def plot_degree_distribution(graph):
    degrees = [graph.degree(node) for node in graph.nodes]
    plt.hist(degrees, bins=np.arange(min(degrees), max(degrees) + 1, 1), density=True, alpha=0.75)
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Probability")
    plt.show()

def calculate_clustering_coefficient(graph):
    clustering_coefficient = nx.average_clustering(graph)
    print(f"Average Clustering Coefficient: {clustering_coefficient}")

def calculate_closeness_centrality(graph):
    closeness_centrality = nx.closeness_centrality(graph)
    average_closeness = sum(closeness_centrality.values()) / len(closeness_centrality)
    print(f"Average Closeness Centrality: {average_closeness}")


if __name__ == "__main__":
    github_username = 'torvalds'
    github_token = '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'

    followers_data = []

    for page in range(1, 3):
        followers_data_chunk = get_followers_list(github_username, github_token, page=page, per_page=100)
        followers_data.extend(followers_data_chunk)

    github_network = plot_graph(github_username, followers_data)

    plot_degree_distribution(github_network)

    calculate_clustering_coefficient(github_network)

    calculate_closeness_centrality(github_network)
