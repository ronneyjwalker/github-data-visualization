import networkx as nx
import matplotlib.pyplot as plt
import requests
import numpy as np
import csv
import json

def fetch_user_followers(username, github_token):
    url = f'https://api.github.com/users/{username}/followers'
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        followers = response.json()
        return [follower['login'] for follower in followers]
    else:
        raise ValueError(f"Failed to fetch followers. Status code: {response.status_code}")

def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def save_data_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def create_followers_graph(username, github_token, depth=1):
    graph = nx.Graph()
    nodes_data = []
    edges_data = []
    users_to_explore = [(username, 0)]

    while users_to_explore:
        current_user, current_depth = users_to_explore.pop(0)

        if current_depth <= depth:
            followers = fetch_user_followers(current_user, github_token)
            
            for follower in followers:
                graph.add_edge(current_user, follower)
                users_to_explore.append((follower, current_depth + 1))

                if current_user not in nodes_data:
                    nodes_data.append(current_user)
                if follower not in nodes_data:
                    nodes_data.append(follower)
                edges_data.append((current_user, follower))

    save_data_to_csv(nodes_data, 'nodes_data.csv')
    save_data_to_csv(edges_data, 'edges_data.csv')
    save_data_to_json({'nodes': nodes_data, 'edges': edges_data}, 'graph_data.json')

    return graph

def draw_followers_graph(graph):
    pos = nx.spring_layout(graph)
    
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=200, node_color='skyblue', font_size=4, edge_color='gray')
    plt.show()

def calculate_degree_distribution(graph):
    degree_sequence = [d for n, d in graph.degree()]
    return degree_sequence

def calculate_clustering_coefficient(graph):
    return nx.average_clustering(graph)

def calculate_closeness_centrality(graph):
    closeness_centrality = nx.closeness_centrality(graph)
    average_closeness = sum(closeness_centrality.values()) / len(closeness_centrality)
    return average_closeness


if __name__ == "__main__":
    start_user = 'ozkalai'
    github_token = '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'
    
    followers_graph = create_followers_graph(start_user, github_token, depth=1)
    
    draw_followers_graph(followers_graph)

    degree_sequence = calculate_degree_distribution(followers_graph)
    plt.hist(degree_sequence, bins=np.arange(min(degree_sequence), max(degree_sequence) + 1, 1), density=True, alpha=0.75)
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Probability")
    plt.show()

    clustering_coefficient = calculate_clustering_coefficient(followers_graph)
    print(f"Average Clustering Coefficient: {clustering_coefficient}")

    average_closeness = calculate_closeness_centrality(followers_graph)
    print(f"Average Closeness Centrality: {average_closeness}")
