from subprocess import Popen, STDOUT, PIPE

import os
import copy
import numpy as np
import networkx as nx
import multiprocessing

class C_Country:
    def __init__(self, graph):
        # Parameters:
        #     graph      : network of cities
        self.graph = graph
        self.init_cities()

    def init_cities(self):
        # === Init Agents ===
        population = nx.get_node_attributes(self.graph, "population")
        self.agent_num = np.sum(list(population.values()))
        self.city_num = len(self.graph.nodes)

        indexes = nx.get_node_attributes(self.graph, "index")
        for i,ind in enumerate(indexes):
            if i!= ind: assert(1)

    def get_str_graph(self):
        # === City data ===
        str_graph = "{} {}\n".format(self.agent_num, self.city_num)
        for city in range(len(self.graph.nodes())):
            weights = [str(self.graph[city][neigh]["weight"]) for neigh in self.graph[city].keys()]
            neighs = [str(k) for k in self.graph[city].keys()]
            pop = self.graph.nodes[city]["population"]

            line = "{} {} {} {}\n".format(pop, len(neighs), " ".join(neighs), " ".join(weights))
            str_graph += line
        return str_graph
    
    @staticmethod
    def infect_cities(mode, area, inf_agent_num):
        # TODO: use pandas
        if(mode == "uniform_random"):
            agent_location = np.random.choice(area, size = inf_agent_num)
            uniq, count = np.unique(agent_location, return_counts = True)
            return uniq, count
        else:
            print("Mode not implemented yet")

    @staticmethod
    def run(args, inf_area, str_graph, city_num, job_count, lock):
        # === Infect ===
        inf_cities, inf_agents = C_Country.infect_cities("uniform_random", inf_area, args["inf_agent_num"])

        # === Inf cities ===
        str_inf_agents = "{}\n".format(len(inf_area))
        for inf_city, agent_num in zip(inf_cities, inf_agents):
            str_inf_agents += "{} {}\n".format(inf_city, agent_num)
        
        # === Agent data ===
        # TODO: agents should be initialized in C++ 
        str_args = [str(item) for pair in args.items() for item in pair]
        p = Popen([os.path.dirname(os.path.abspath(__file__))+'/main']+ str_args,
                  stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True)

        out,err = p.communicate(str_graph + str_inf_agents)

        history = []
        for line in out.split('\n')[:-1]:
            history.append([int(a) for a in line[:-1].split(" ")])
        history = np.array(history[:])

        with lock:
            job_count[0]+=1
            print('\r {}/{}'.format(job_count[0], job_count[1]), end='', flush=True)
        return history

    def run_async(self, args, inf_area):
        str_graph = self.get_str_graph()
        city_num = self.city_num
        agent_num = self.agent_num

        # === RUN ASYNCHRON ===
        pool = multiprocessing.Pool(processes=args["procnum"])
        manager = multiprocessing.Manager()
        lock = manager.Lock()

        res = []
        job_count = manager.Array("i", [0,args["simnum"]])
        for i in range(args["simnum"]):
            act_args = copy.copy(args)
            act_args["--seed"]=i
            history = pool.apply_async(C_Country.run, args =
                                        (act_args, inf_area, str_graph, city_num, job_count, lock))
            res.append(history)
        pool.close()
        pool.join()
        print('')

        return [np.array(hist.get()) for hist in res]