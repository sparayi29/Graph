import streamlit as st
import networkx as nx


def output_nodes_and_edges(graph: nx.Graph):
    st.write(graph.nodes)
    st.write(graph.edges)


def count_nodes(graph: nx.Graph):
    count = graph.number_of_nodes()
    st.write(f"The Number of Nodes are {count}")

