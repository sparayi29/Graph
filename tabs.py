import streamlit as st
import json
import uuid
from model import metamodel_dict
import graphviz
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx
from graph_functions import output_nodes_and_edges, count_nodes


def graph_upload():
    upload_graph = st.file_uploader("Upload an Existing Graph", type="json")
    if upload_graph is not None:
        upload_graph_dict = json.load(upload_graph)
        uploaded_nodes = upload_graph_dict["nodes"]
        uploaded_edges = upload_graph_dict["edges"]
        st.write(upload_graph_dict)
    else:
        st.info("Please Upload Graph")

    update_graph_button = st.button(
        "Update Graph via Upload",
        use_container_width=True,
        type="primary"
    )
    if update_graph_button and upload_graph is not None:
        st.session_state["node_list"] = uploaded_nodes
        st.session_state["edge_list"] = uploaded_edges


def create_node():
    name_node = st.text_input("Type the Name")
    age_node = st.number_input("Type the Age", value=0)
    print_hi(name_node, age_node)
    save_node_button = st.button("Store Detail", use_container_width=True, type="primary")
    if save_node_button:
        save_node(name_node, age_node)
    st.write(st.session_state["node_list"])


def print_hi(name, age):
    st.info(f'Hi, my name is {name} and I am {age} years old')  # Press Ctrl+F8 to toggle the breakpoint.


def save_node(name, age):
    node_dict = {
        "name": name,
        "age": age,
        "id": str(uuid.uuid4()),
        "type": "Node"
    }
    st.session_state["node_list"].append(node_dict)


def relation_node():
    node1_col, relation_col, node2_col = st.columns(3)
    node_list = st.session_state["node_list"]
    node_name_list = []
    for node in node_list:
        node_name_list.append(node["name"])
    with node1_col:
        node1_select = st.selectbox(
            "Select the First Node",
            options=node_name_list,
            key="node1_select"
        )
    with node2_col:
        node2_select = st.selectbox(
            "Select the Second Node",
            options=node_name_list,
            key="node2_select"
        )
    with relation_col:
        relation_list = metamodel_dict["edges"]
        relation_name = st.selectbox(
            "Specify the Relation",
            options=relation_list,
            key="relation_select"
        )
    store_edge_button = st.button("Store Relation",
                                  use_container_width=True,
                                  type="primary")

    if store_edge_button:
        save_edge(node1_select, relation_name, node2_select)
    st.write(st.session_state["edge_list"])


def save_edge(node1, relation, node2):
    edge_dict = {
        "source": node1,
        "target": node2,
        "type": relation,
        "id": str(uuid.uuid4())
    }
    st.session_state["edge_list"].append(edge_dict)


def call_graph_dict():
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"]
    }
    st.session_state["graph_dict"] = graph_dict


def graph_store():
    with st.expander("Show individual lists"):
        st.json(st.session_state["node_list"], expanded=False)
        st.json(st.session_state["edge_list"], expanded=False)

    call_graph_dict()

    with st.expander("Show Graph JSON", expanded=False):
        st.json(st.session_state["graph_dict"])


def graph_visualize():
    call_graph_dict()
    # Create a graphlib graph object
    graph = graphviz.Digraph()
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge_list = graph_dict["edges"]
    for node in node_list:
        node_name = node["name"]
        graph.node(node_name)
    for edge in edge_list:
        source = edge["source"]
        target = edge["target"]
        label = edge["type"]
        graph.edge(source, target, label)

    with st.expander("VIZ", expanded=False):
        st.graphviz_chart(graph)

    with st.expander("Agraph visualization", expanded=False):
        nodes = []
        edges = []

        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]

        for node in node_list:
            nodes.append(Node(id=node['name'], label=node["name"]))

        # for edge in edge_list:
        #     for node in node_list:
        #         if edge["source"]==node["name"]:
        #             source=node["id"]
        #         elif edge["target"]==node["name"]:
        #             target=node["id"]
        #     edges.append(Edge(source=source, target=target, label=edge["type"]))

        for edge in edge_list:
            edges.append(Edge(source=edge['source'], target=edge['target'], label=edge["type"]))

        config = Config(width=500,
                        height=500,
                        directed=True,
                        physics=True,
                        heirarchical=False,
                        nodeHighlightBehavior=True,
                        highlightColor="#F7A7A6",  # or "blue"
                        collapsible=False,
                        # coming soon (set for all): node_size=1000, node_color="blue"
                        )

        agraph(nodes=nodes, edges=edges, config=config)


def graph_analyze():
    g = nx.Graph()
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge_list = graph_dict["edges"]
    node_tuple_list = []
    edge_tuple_list = []

    for node in node_list:
        node_tuple = (node["name"], node)
        node_tuple_list.append(node_tuple)

    for edge in edge_list:
        edge_tuple = (edge["source"], edge["target"], edge)
        edge_tuple_list.append(edge_tuple)

    g.add_nodes_from(node_tuple_list)
    g.add_edges_from(edge_tuple_list)
    # st.write(G.nodes)
    # st.write(G.edges)

    select_function = st.selectbox(label="Select Function",
                                   options=["Output Nodes and Edges", "Count Nodes"])
    if select_function == "Output Nodes and Edges":
        output_nodes_and_edges(graph=g)
    else:
        count_nodes(graph=g)


def graph_export():
    graph_string = json.dumps(st.session_state["graph_dict"])

    st.download_button(
        "Export Graph to JSON",
        file_name="graph.json",
        mime="application/json",
        data=graph_string,
        use_container_width=True,
        type="primary"
    )
