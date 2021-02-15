# metapop
Effective implementation of infection spreading on metapopulational graphs.

## Intro

You can launch the application with launch.py. There you can define your graph, the infection parameters, and other simulation settings (such as: number of simulations, number of processing cores etc.).

The given graph should in networkx format, it should contain for each node:
* population (int)
* index (int)

And each edge should contain :
* weight(float): the number of travelling agents in the edge.

For each node, the sum of the outgoing edges cannot exceed the population.
The id-order of the nodes have to be 0,1,...,n and should match with the index attribute (That may couse some inconvenient... and please use python >=3.6).

The C_Country.run_async will simulate the infection seeded from the given infected cities, and with the given infected agents. It returns for each measure the [(S_i,E_i,I_i,R_i) i = 1...max_iter] array.
