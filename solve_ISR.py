import time
import sys
import get_instance
from graphillion import reconf, setset
from timeout_decorator import timeout, TimeoutError


@timeout(120)
def solve_ISR(vertices, edges, S, T, name):
    with open("ZDD_based_solver_log.txt", mode="w") as f:
        print(name, file=f)
    with open("ZDD_based_solver_log.txt", mode="a") as f:

        #ISRを解く
        setset.set_universe(vertices)
        start = time.time()
        iss = reconf.get_independent_setset(vertices, edges)
        end = time.time()
        IS_time = end - start
        print(f"IS,{IS_time}", file=f)
    
    with open("ZDD_based_solver_log.txt", mode="a") as f:
        seq = reconf.get_reconf_seq_ts(S,T,iss,edges)
        print(file=f)
    return seq
    
if __name__ == "__main__":
    V, E, S, T = get_instance.get_instance(sys.argv[1],sys.argv[2])
    try:
        print(len(solve_ISR(V, E, S, T, sys.argv[3])))
    except TimeoutError:
        with open("ZDD_based_solver_log.txt",mode="a") as f:
            f.write("unsolved")
