import time
import sys
import get_instance
from graphillion import reconf, setset
from timeout_decorator import timeout, TimeoutError

PICK_UP = [
        0,
        122,
        136,
        138,
        168,
        170,
        172,
        202,
        251,
        253,
        254,
        255,
        256,
        322,
        60,
        ]

def diameter(V,E,S,graph_path, sol_path):
    #解空間のノード構築
    setset.set_universe(V)
    iss = reconf.get_independent_setset(V,E)
    diameter = 0
    for s in iss:
        if not len(s) == len(S):
            continue
        seq_from_s = reconf.get_reconf_seq_ts(S,s,iss,E)
        if seq_from_s == None:
            continue
        for t in iss:
            if s == t or len(s) != len(t):
                continue
            seq = reconf.get_reconf_seq_ts(s,t,iss,E)
            if seq == None:
                continue
            diameter = max(diameter,len(seq))
    return diameter-1


if __name__ == "__main__":
    graph_path = sys.argv[1]
    sol_path = sys.argv[2]
    no = sys.argv[3]
    if int(no) not in PICK_UP:
        exit()
    V, E, S, _ = get_instance.get_instance(graph_path, sol_path)
    print(f"{no},{diameter(V,E,S,graph_path,sol_path)}")
    

    