import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

def create_graph(net):

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        net.show('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')

    # Read the HTML file
    source_code = HtmlFile.read()

    return components.html(source_code, height=400)


def inventory_graph():
    G = Network(
                    height='400px',
                    width='100%',
                    bgcolor='white',
                    font_color='black',
                    directed=True,
                    neighborhood_highlight=True,
                )
    
    manuf_df = pd.read_csv("./data/Manufacturing_Facilities.csv")

    st.subheader('Manufacturing Facilities')
    st.table(manuf_df)

    for index, row in manuf_df.iterrows():
        G.add_node(row["Facility_Id"], label=row["Facility_Id"], title=row["Facility_name"],Facility_name=row["Facility_name"], Capacity=row["Capacity"], Utilization=row["Utilization_rate"], Maintenance=row["Maintenance_status"], group=1, size=10)

    log_df = pd.read_csv("./data/Logistics_Hubs.csv")

    st.subheader('Logistics Hubs')
    st.table(log_df)

    for index, rows in log_df.iterrows():
        G.add_node(rows["Hub_Id"], label=rows["Hub_Id"] , title=rows["Hub_name"] ,Hub_name=rows["Hub_name"], Location=rows["Location"], Capacity=rows["Capacity"], Throughput=rows["Throughput"], Inventory_levels=rows["Inventory_Levels"], group=2, size=15)


    relation_df = pd.read_csv("./data/Distribution_Relationship.csv")

    st.subheader('Distribution Relationship')
    st.table(relation_df)

    new_df = pd.merge(manuf_df, relation_df, on="Facility_Id")
    new_df = pd.merge(new_df, log_df, on="Hub_Id")

    for index, r in new_df.iterrows():
        G.add_edge(r["Facility_Id"], r["Hub_Id"], Transportation_mode=r["Transportation_Mode"], Shipment_frequency=r["Shipment_Frequency"], Cost=r["Cost"])

    st.subheader('Graph Visualization')
    # Create a graph using PyVis
    create_graph(G)

def assembly_graph():
    G = Network(
                    height='400px',
                    width='100%',
                    bgcolor='white',
                    font_color='black',
                    directed=True,
                    neighborhood_highlight=True,
                )
    
    df = pd.read_csv('./data/Final_component.csv')

    st.subheader('Assembly Components')
    st.table(df)

    for i,r in df.iterrows():
        G.add_node(
                    r['Node_ID'], 
                    label=r['Node_ID'],
                    title=r['Node_Name'],
                    size=20, 
                    group=1
                )

    cf = pd.read_csv('./data/Subassembly.csv')

    st.subheader('Subassembly')
    st.table(cf)

    for i,r in cf.iterrows():
        G.add_node(
                    r['Node_ID'],
                    label=r['Node_ID'],
                    title=r['Node_Name'],
                    size=15,
                    group=2
                )
        
    bf = pd.read_csv('./data/Raw_materials.csv')

    st.subheader('Raw Materials')
    st.table(bf)

    for i,r in bf.iterrows():
        G.add_node(
                    r['Node_ID'],
                    title=r['Node_Name'],
                    label=r['Node_ID'],
                    size=10,
                    group=3
                )

    af = pd.read_csv('./data/The_connections.csv')

    st.subheader('Connections')
    st.table(af)

    new_df = pd.merge(df,af,on= 'Node_ID')
    for i,r in new_df.iterrows():
        G.add_edge(
                    r['From_Node_ID'],
                    r['Node_ID']
                )
    
    new_df_2 = pd.merge(cf,af,on = 'Node_ID')
    for i,r in new_df_2.iterrows():
        G.add_edge(
                    r['From_Node_ID'],
                    r['Node_ID'],
                )

    st.subheader('Graph Visualization')
    create_graph(G)

def main():
    # streamlit title and dropdown to choose the dataset for visualization
    st.title('LAM Graph Visualization Demo')

    # Show dropdown for dataset selection
    dataset = st.selectbox('Select dataset', ['Assembly', 'Inventory'])

    if dataset == 'Inventory':
        inventory_graph()
    elif dataset == 'Assembly':
        assembly_graph()

if __name__ == '__main__':
    main()