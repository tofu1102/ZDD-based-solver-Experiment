import time
import sys
import get_instance
from graphillion import reconf, setset
from timeout_decorator import timeout, TimeoutError
PICK_UP = [255, 256, 136, 322, 253, 202, 251, 138, 254, 168, 0, 170, 252, 18, 352, 140, 172, 12, 325, 353, 30, 176, 257, 274, 354, 326, 92, 355, 42, 258, 178, 88, 132, 328, 259, 143, 174, 128, 154, 207, 278, 281, 329, 36, 330, 90, 156, 56, 58, 120, 122, 124, 126, 80, 158, 362, 46, 263, 333, 264, 334, 265, 366, 145, 162, 266, 8, 368, 14, 267, 164, 268, 339, 340, 62, 64, 66, 167, 342, 32, 4, 343, 272, 344]
def solve_ISR(vertices, edges, S, T, graph_path, sol_path):
    if not (graph_path,sol_path) in PICK_UP:
        return
    
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
    no = sys.argv[4]
    if no not in PICK_UP:
        exit()
    V, E, S, T = get_instance.get_instance(graph_path, sol_path)
    @timeout(int(sys.argv[3]))
    def _solve_ISR(V, E, S, T, graph_path, sol_path):
        return solve_ISR(V, E, S, T, graph_path, sol_path)
    try:
        _solve_ISR(V, E, S, T, graph_path, sol_path)
        print("o,solved")
    except TimeoutError:
        print("o,timeover")
