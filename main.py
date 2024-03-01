import streamlit as st
from streamlit_option_menu import option_menu
from tabs import graph_upload, create_node, relation_node, graph_store, graph_visualize, graph_analyze, graph_export


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []
    if "edge_list" not in st.session_state:
        st.session_state["edge_list"] = []
    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []

    tab_list = [
        "Import Existing Graph",
        "Create Nodes (Nodes)",
        "Create Relations between Nodes",
        "Store Graph",
        "Visualize Graph",
        "Analyze Graph",
        "Export Graph"
        ]

    st.set_page_config(layout="wide", initial_sidebar_state="auto")

    # st.title("PyInPSE Tutorial")
    # (
    #     import_graph_tab,
    #     create_node_tab,
    #     create_relations_tab,
    #     store_graph_tab,
    #     visualize_graph_tab,
    #     analyze_the_graph,
    #     export_graph_tab
    #  ) = st.tabs(tab_list)

    # with st.sidebar:
    selected_tab = option_menu("Main Menu", tab_list,
                               menu_icon="cast",
                               default_index=0,
                               orientation="horizontal")

    st.write(selected_tab)

    # selected_tab = option_menu("Navigation", tab_list)

    if selected_tab == "Import Existing Graph":
        graph_upload()

    if selected_tab == "Create Nodes (Nodes)":
        create_node()

    if selected_tab == "Create Relations between Nodes":
        relation_node()

    if selected_tab == "Store Graph":
        graph_store()

    if selected_tab == "Visualize Graph":
        graph_visualize()

    if selected_tab == "Analyze Graph":
        graph_analyze()

    if selected_tab == "Export Graph":
        graph_export()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
