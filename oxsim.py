import osmnx as ox
import matplotlib.pyplot as plt

# streets_graph = ox.graph_from_place('Los Angeles, California', network_type='drive')#address：Los Angeles城市名，California
streets_graph = ox.graph_from_place('湖北省，武汉市,洪山区', network_type='drive')#address：Los Angeles城市名，California
streets_graph = ox.projection.project_graph(streets_graph)

streets = ox.graph_to_gdfs(ox.get_undirected(streets_graph), nodes=False, edges=True,
                                   node_geometry=False, fill_edge_geometry=True)
ox.save_graph_shapefile(streets_graph,filepath = "WuHan_DriveStreet.shp")

f, ax = plt.subplots(figsize=(10, 10))
streets.plot(ax=ax, linewidth=0.2)
ax.set_axis_off()
plt.show()



