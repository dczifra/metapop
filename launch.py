import numpy as np
import matplotlib.pyplot as plt
from src.c_country import C_Country
from utils.graph_generator import get_path

args = {
    "--p_moving": 0.0005, 
    "--p_worker": 0.0, 
    "--beta": 0.4,
    "--beta_super":0.0,
    "--sigma": 1.0,
    "--gamma": 0.1,
    "--max_sim": 200,
    "inf_agent_num":100,
    "simnum":5,
    "procnum":8,
}

if(__name__ == "__main__"):
    np.random.seed(0)

    graph = get_path(args = {"n":4, "population":50000})
    country = C_Country(graph)
    measurements = country.run_async(args, [1])

    for i,hist in enumerate(measurements):
        plt.plot(hist[:,2], label = "Simulation "+str(i))
    
    plt.title("Infection curves for different random seeds")
    plt.legend()
    plt.show()