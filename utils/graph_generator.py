import csv
import pickle
import powerlaw
import numpy as np
import networkx as nx

#import matplotlib.pyplot as plt

def get_graph(type, args):
    """
    Returns the type of graph with the given size
    :param type: The graph's type you wish (simple, erdos-renyi ...)
    :param size: Node size of th graph
    """
    if type == "simple":
        return get_simple()
    elif type == "read_from":
        return read_gml(args)
    elif type == "erdos-renyi":
        return get_erdos_renyi(args)
    elif type =="nx-pickle":
        return get_pickle(args)
    elif type =="random-regular":
        return get_random_regular(args)
    elif type =="random-geometric":
        return get_random_geometric(args)
    elif type =="pref_attachment":
        return get_pref_attachment(args)
    elif type =="config_model":
        return get_config_model(args)
    elif type =="single-node":
        return get_single_node(args)
    elif type =="path":
        return get_path(args)
    elif type =="grid":
        return get_grid(args)
    elif type =="2grids":
        return get_2grids(args)
    elif type =="torus":
        return get_torus(args)
    else:
        print("Type : {} not recognized".format(type))

def read_gml(args):
    graph = nx.Graph()
    return nx.read_graphml(args["path"])

def get_path(args):
    graph = nx.Graph()
    pop = args["population"]
    travel = args["population"]//2

    graph.add_node(0,index = 0, population = pop, pos = (0,0))
    for i in range(1,args["n"]):
        graph.add_node(i,index = i, population = pop, pos = (i,0))
        graph.add_edge(i, i-1, weight = travel, dist = 1.0)

    #nx.draw(graph)
    #plt.show()
    return graph

def get_erdos_renyi(args, plot=False):
    n = args["n"]
    p = args["d"]/n

    G = nx.erdos_renyi_graph(n, p)

    # === Init node population ===
    #print("  ==> Erdos-Renyi Graph")
    for i,v in enumerate(nx.nodes(G)):
        G.nodes[v]["population"]=max(1, nx.degree(G,v)*150)
        G.nodes[v]["index"]=i
        #print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

    # === Init edge weights ===
    for u,v in nx.edges(G):
        G[u][v]["weight"]=np.min([30, nx.degree(G,u),nx.degree(G,v) ])
        G[u][v]["dist"] = 1.0

    pos = nx.spring_layout(G)
    nx.set_node_attributes(G, {k:[v[0]*15,v[1]*15] for k,v in  pos.items() }, 'pos')

    #if(plot):
    #    nx.draw(G)
    #    plt.show()
    return G

def get_pref_attachment(args, plot=False):
    n = args["n"]
    
    G = nx.barabasi_albert_graph(n, 3)

    # === Init node population ===
    #print("  ==> Erdos-Renyi Graph")
    for i,v in enumerate(nx.nodes(G)):
        G.nodes[v]["population"]=max(1, nx.degree(G,v)*150)
        G.nodes[v]["index"]=i
        #print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

    # === Init edge weights ===
    for u,v in nx.edges(G):
        G[u][v]["weight"]=30.0
        G[u][v]["dist"] = 1.0

    pos = nx.spring_layout(G)
    nx.set_node_attributes(G, {k:[v[0]*15,v[1]*15] for k,v in  pos.items() }, 'pos')

    #if(plot):
    #    nx.draw(G)
    #    plt.show()
    return G


def get_config_model(args, plot=False):
    n = args["n"]
    if "deg_exp" in args:
        deg_exp = args["deg_exp"]
    else:
        deg_exp = 3.5
        
    d=powerlaw.Power_Law(xmin=3,parameters=[deg_exp]).generate_random(n).astype(int)
    if (sum(d) %2)>0:
        d[-1]+=1
    
    G = nx.configuration_model(d)
    G=nx.Graph(G)

    # === Init node population ===
    #print("  ==> Erdos-Renyi Graph")
    for i,v in enumerate(nx.nodes(G)):
        G.nodes[v]["population"]=max(1, nx.degree(G,v)*150)
        G.nodes[v]["index"]=i
        #print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

    # === Init edge weights ===
    for u,v in nx.edges(G):
        G[u][v]["weight"]=30.0
        G[u][v]["dist"] = 1.0

    pos = nx.spring_layout(G)
    nx.set_node_attributes(G, {k:[v[0]*15,v[1]*15] for k,v in  pos.items() }, 'pos')

    #if(plot):
    #    nx.draw(G)
    #    plt.show()
    return G


def get_random_regular(args):
    n = args["n"]
    d = args["d"]
    N = args["N"]

    #m = args["m"]
    #G = nx.gnm_random_graph(n, m)
    G = nx.random_regular_graph(d,n)

    # some properties
    for i,v in enumerate(nx.nodes(G)):
        G.nodes[v]["population"]=int(N/n)
        G.nodes[v]["index"]=i
        #print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

    for u,v in nx.edges(G):
        G[u][v]["weight"]=int(N/(n*d))
        G[u][v]["dist"] = 1.0
    
    pos = nx.spring_layout(G)
    nx.set_node_attributes(G, {k:[v[0]*15,v[1]*15] for k,v in  pos.items() }, 'pos')
    nx.set_node_attributes(G, {n:n for n in G.nodes() }, 'label')

    return G

def get_random_geometric(args):
    n = args["n"]
    d = args["d"]
    N = args["N"]

    #m = args["m"]
    #G = nx.gnm_random_graph(n, m)
    G = nx.random_geometric_graph(n,np.sqrt(d/(np.pi*n)))

    # some properties
    for i,v in enumerate(nx.nodes(G)):
        G.nodes[v]["population"]=int(N/n)
        G.nodes[v]["index"]=i
        #print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

    for u,v in nx.edges(G):
        G[u][v]["weight"]=int(N/(n*d))
        G[u][v]["dist"] = 1.0
    
    pos = nx.get_node_attributes(G,"pos")
    nx.set_node_attributes(G, {k:[v[0]*15,v[1]*15] for k,v in  pos.items() }, 'pos')
    nx.set_node_attributes(G, {n:n for n in G.nodes() }, 'label')
    return G



def get_grid(args):
    n = args["n"]
    d = args["d"]
    N = args["N"]
    #print(n)

    #m = args["m"]
    #G = nx.gnm_random_graph(n, m)
    G = nx.grid_2d_graph(int(np.sqrt(n)),int(np.sqrt(n)))

    # some properties
    for i,v in enumerate(nx.nodes(G)):
        G.nodes[v]["population"]=int(N/G.number_of_nodes())
        G.nodes[v]["index"]=i
        #print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

    for u,v in nx.edges(G):
        G[u][v]["weight"]=int(N/(G.number_of_nodes()*d))
        G[u][v]["dist"]=1.0
        
    nx.set_node_attributes(G, {n:n for n in G.nodes() }, 'pos')
    nx.set_node_attributes(G, {n:n for n in G.nodes() }, 'label')

    return G


def get_2grids(args):
    n = args["n"]
    d = args["d"]
    N = args["N"]
    #print(n)
    n=int(np.sqrt(n))

    #m = args["m"]
    #G = nx.gnm_random_graph(n, m)
    G = nx.grid_2d_graph(n,n)

    rows=range(n)
    columns=range(n)
    G.add_nodes_from( (i+n+1,j) for i in rows for j in columns )
    G.add_edges_from( ((i+n+1,j),(i-1+n+1,j)) for i in rows for j in columns if i>0 )
    G.add_edges_from( ((i+n+1,j),(i+n+1,j-1)) for i in rows for j in columns if j>0 )


    # some properties
    for i,v in enumerate(nx.nodes(G)):
        G.nodes[v]["population"]=int(N/G.number_of_nodes())
        G.nodes[v]["index"]=i
        #print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

    for u,v in nx.edges(G):
        G[u][v]["weight"]=int(N/(G.number_of_nodes()*d))
        G[u][v]["dist"]=1.0
        
    nx.set_node_attributes(G, {n:n for n in G.nodes() }, 'pos')
    nx.set_node_attributes(G, {n:n for n in G.nodes() }, 'label')

    return G


def get_torus(args):
    n = args["n"]
    d = args["d"]
    N = args["N"]
    #print(n)

    #m = args["m"]
    #G = nx.gnm_random_graph(n, m)
    G = nx.grid_2d_graph(int(np.sqrt(n)),int(np.sqrt(n)), periodic=True)

    # some properties
    for i,v in enumerate(nx.nodes(G)):
        G.nodes[v]["population"]=int(N/G.number_of_nodes())
        G.nodes[v]["index"]=i
        #print('%s %d %f' % (v, nx.degree(G, v), nx.clustering(G, v)))

    for u,v in nx.edges(G):
        G[u][v]["weight"]=int(N/(G.number_of_nodes()*d))
        G[u][v]["dist"]=1.0
        
    nx.set_node_attributes(G, {n:n for n in G.nodes() }, 'pos')
    nx.set_node_attributes(G, {n:n for n in G.nodes() }, 'label')

    return G


def get_single_node(args):
    G = nx.Graph()
    G.add_node(0)
    G.nodes[0]["population"]=args["N"]
    G.nodes[0]["index"]=0
    return G
    
    
def get_pickle(args):
    with open(args["path"], 'rb') as handle:
        return pickle.load(handle)
