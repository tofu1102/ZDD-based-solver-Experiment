import time
import sys
import get_instance
from graphillion import reconf, setset
from timeout_decorator import timeout, TimeoutError
PICK_UP = [259]
def solve_ISR(vertices, edges, S, T, graph_path, sol_path):
    with open("ZDD_based_solver_log.txt", mode="a") as f:

        #ISRを解く
        setset.set_universe(vertices)
        start = time.time()
        iss = reconf.get_independent_setset(vertices, edges)
        end = time.time()
        IS_time = end - start
        print(f"IS,{len(iss)},{graph_path},{sol_path}")
    
    with open("ZDD_based_solver_log.txt", mode="a") as f:
        seq = reconf.get_reconf_seq_ts(S,T,iss,edges)
        print(file=f)
    return seq
    
if __name__ == "__main__":
    graph_path = sys.argv[1]
    sol_path = sys.argv[2]
    no = int(sys.argv[4])
    V, E, S, T = get_instance.get_instance(graph_path, sol_path)
    @timeout(int(sys.argv[3]))
    def _solve_ISR(V, E, S, T, graph_path, sol_path):
        return solve_ISR(V, E, S, T, graph_path, sol_path)
    try:
        dummy = _solve_ISR(V, E, S, T, graph_path, sol_path)
        print("o,solved")
    except TimeoutError:
        print("o,timeover")
