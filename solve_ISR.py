import time
import sys
import get_instance
from graphillion import reconf, setset
from timeout_decorator import timeout, TimeoutError
PICK_UP = [('2022benchmark-main/benchmark/color04/1-FullIns_3.col', '2022benchmark-main/benchmark/color04/1-FullIns_3_01.dat'),
('2022benchmark-main/benchmark/color04/1-FullIns_5.col', '2022benchmark-main/benchmark/color04/1-FullIns_5_01.dat'),
('2022benchmark-main/benchmark/color04/1-Insertions_5.col', '2022benchmark-main/benchmark/color04/1-Insertions_5_01.dat'),
('2022benchmark-main/benchmark/color04/2-FullIns_3.col', '2022benchmark-main/benchmark/color04/2-FullIns_3_01.dat'),
('2022benchmark-main/benchmark/color04/2-Insertions_3.col', '2022benchmark-main/benchmark/color04/2-Insertions_3_01.dat'),
('2022benchmark-main/benchmark/color04/3-Insertions_3.col', '2022benchmark-main/benchmark/color04/3-Insertions_3_01.dat'),
('2022benchmark-main/benchmark/color04/3-Insertions_4.col', '2022benchmark-main/benchmark/color04/3-Insertions_4_01.dat'),
('2022benchmark-main/benchmark/color04/4-FullIns_3.col', '2022benchmark-main/benchmark/color04/4-FullIns_3_01.dat'),
('2022benchmark-main/benchmark/color04/4-Insertions_3.col', '2022benchmark-main/benchmark/color04/4-Insertions_3_01.dat'),
('2022benchmark-main/benchmark/color04/5-FullIns_3.col', '2022benchmark-main/benchmark/color04/5-FullIns_3_01.dat'),
('2022benchmark-main/benchmark/color04/DSJC125.1.col', '2022benchmark-main/benchmark/color04/DSJC125.1_01.dat'),
('2022benchmark-main/benchmark/color04/DSJC125.5.col', '2022benchmark-main/benchmark/color04/DSJC125.5_01.dat'),
('2022benchmark-main/benchmark/color04/DSJC125.9.col', '2022benchmark-main/benchmark/color04/DSJC125.9_01.dat'),
('2022benchmark-main/benchmark/color04/anna.col', '2022benchmark-main/benchmark/color04/anna_01.dat'),
('2022benchmark-main/benchmark/color04/david.col', '2022benchmark-main/benchmark/color04/david_01.dat'),
('2022benchmark-main/benchmark/color04/games120.col', '2022benchmark-main/benchmark/color04/games120_01.dat'),
('2022benchmark-main/benchmark/color04/huck.col', '2022benchmark-main/benchmark/color04/huck_01.dat'),
('2022benchmark-main/benchmark/color04/miles1000.col', '2022benchmark-main/benchmark/color04/miles1000_01.dat'),
('2022benchmark-main/benchmark/color04/miles1500.col', '2022benchmark-main/benchmark/color04/miles1500_01.dat'),
('2022benchmark-main/benchmark/color04/miles500.col', '2022benchmark-main/benchmark/color04/miles500_01.dat'),
('2022benchmark-main/benchmark/color04/miles750.col', '2022benchmark-main/benchmark/color04/miles750_01.dat'),
('2022benchmark-main/benchmark/color04/mug100_1.col', '2022benchmark-main/benchmark/color04/mug100_1_01.dat'),
('2022benchmark-main/benchmark/color04/mug88_1.col', '2022benchmark-main/benchmark/color04/mug88_1_01.dat'),
('2022benchmark-main/benchmark/color04/myciel3.col', '2022benchmark-main/benchmark/color04/myciel3_01.dat'),
('2022benchmark-main/benchmark/color04/myciel4.col', '2022benchmark-main/benchmark/color04/myciel4_01.dat'),
('2022benchmark-main/benchmark/color04/myciel5.col', '2022benchmark-main/benchmark/color04/myciel5_01.dat'),
('2022benchmark-main/benchmark/color04/myciel6.col', '2022benchmark-main/benchmark/color04/myciel6_02.dat'),
('2022benchmark-main/benchmark/color04/queen10_10.col', '2022benchmark-main/benchmark/color04/queen10_10_01.dat'),
('2022benchmark-main/benchmark/color04/queen11_11.col', '2022benchmark-main/benchmark/color04/queen11_11_01.dat'),
('2022benchmark-main/benchmark/color04/queen12_12.col', '2022benchmark-main/benchmark/color04/queen12_12_01.dat'),
('2022benchmark-main/benchmark/color04/queen14_14.col', '2022benchmark-main/benchmark/color04/queen14_14_01.dat'),
('2022benchmark-main/benchmark/color04/queen5_5.col', '2022benchmark-main/benchmark/color04/queen5_5_01.dat'),
('2022benchmark-main/benchmark/color04/queen6_6.col', '2022benchmark-main/benchmark/color04/queen6_6_01.dat'),
('2022benchmark-main/benchmark/color04/queen7_7.col', '2022benchmark-main/benchmark/color04/queen7_7_01.dat'),
('2022benchmark-main/benchmark/color04/queen8_12.col', '2022benchmark-main/benchmark/color04/queen8_12_01.dat'),
('2022benchmark-main/benchmark/color04/queen8_8.col', '2022benchmark-main/benchmark/color04/queen8_8_01.dat'),
('2022benchmark-main/benchmark/color04/queen9_9.col', '2022benchmark-main/benchmark/color04/queen9_9_01.dat'),
('2022benchmark-main/benchmark/grid/grid004x004.col', '2022benchmark-main/benchmark/grid/grid004x004_01.dat'),
('2022benchmark-main/benchmark/grid/grid010x010.col', '2022benchmark-main/benchmark/grid/grid010x010_01_6141.dat'),
('2022benchmark-main/benchmark/handcrafted/hc-power-11.col', '2022benchmark-main/benchmark/handcrafted/hc-power-11_01.dat'),
('2022benchmark-main/benchmark/handcrafted/hc-power-12.col', '2022benchmark-main/benchmark/handcrafted/hc-power-12_01.dat'),
('2022benchmark-main/benchmark/handcrafted/hc-square-01.col', '2022benchmark-main/benchmark/handcrafted/hc-square-01_01.dat'),
('2022benchmark-main/benchmark/handcrafted/hc-square-02.col', '2022benchmark-main/benchmark/handcrafted/hc-square-02_01.dat'),
('2022benchmark-main/benchmark/handcrafted/hc-toyno-01.col', '2022benchmark-main/benchmark/handcrafted/hc-toyno-01_01.dat'),
('2022benchmark-main/benchmark/handcrafted/hc-toyyes-01.col', '2022benchmark-main/benchmark/handcrafted/hc-toyyes-01_01.dat'),
('2022benchmark-main/benchmark/power/hc-power-004-002.col', '2022benchmark-main/benchmark/power/hc-power-004-002_01.dat'),
('2022benchmark-main/benchmark/power/hc-power-005-002.col', '2022benchmark-main/benchmark/power/hc-power-005-002_01.dat'),
('2022benchmark-main/benchmark/power/hc-power-006-002.col', '2022benchmark-main/benchmark/power/hc-power-006-002_01.dat'),
('2022benchmark-main/benchmark/power/hc-power-010-002.col', '2022benchmark-main/benchmark/power/hc-power-010-002_01.dat'),
('2022benchmark-main/benchmark/power/hc-power-011-002.col', '2022benchmark-main/benchmark/power/hc-power-011-002_01.dat'),
('2022benchmark-main/benchmark/power/hc-power-013-002.col', '2022benchmark-main/benchmark/power/hc-power-013-002_01.dat'),
('2022benchmark-main/benchmark/queen/queen008x008.col', '2022benchmark-main/benchmark/queen/queen008x008_01_4136.dat'),
('2022benchmark-main/benchmark/queen/queen010x010.col', '2022benchmark-main/benchmark/queen/queen010x010_01_0612.dat'),
('2022benchmark-main/benchmark/sp/sp001.col', '2022benchmark-main/benchmark/sp/sp001_01.dat'),
('2022benchmark-main/benchmark/sp/sp004.col', '2022benchmark-main/benchmark/sp/sp004_01.dat'),
('2022benchmark-main/benchmark/sp/sp005.col', '2022benchmark-main/benchmark/sp/sp005_01.dat'),
('2022benchmark-main/benchmark/sp/sp007.col', '2022benchmark-main/benchmark/sp/sp007_01.dat'),
('2022benchmark-main/benchmark/sp/sp009.col', '2022benchmark-main/benchmark/sp/sp009_01.dat'),
('2022benchmark-main/benchmark/sp/sp012.col', '2022benchmark-main/benchmark/sp/sp012_01.dat'),
('2022benchmark-main/benchmark/sp/sp013.col', '2022benchmark-main/benchmark/sp/sp013_01.dat'),
('2022benchmark-main/benchmark/sp/sp022.col', '2022benchmark-main/benchmark/sp/sp022_01.dat'),
('2022benchmark-main/benchmark/square/hc-square-004-002.col', '2022benchmark-main/benchmark/square/hc-square-004-002_01.dat'),
('2022benchmark-main/benchmark/square/hc-square-005-002.col', '2022benchmark-main/benchmark/square/hc-square-005-002_01.dat'),
('2022benchmark-main/benchmark/square/hc-square-006-002.col', '2022benchmark-main/benchmark/square/hc-square-006-002_01.dat'),
('2022benchmark-main/benchmark/square/hc-square-007-002.col', '2022benchmark-main/benchmark/square/hc-square-007-002_01.dat'),
('2022benchmark-main/benchmark/square/hc-square-014-002.col', '2022benchmark-main/benchmark/square/hc-square-014-002_01.dat'),
('2022benchmark-main/benchmark/square/hc-square-020-002.col', '2022benchmark-main/benchmark/square/hc-square-020-002_01.dat')]

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
    V, E, S, T = get_instance.get_instance(graph_path, sol_path)
    @timeout(int(sys.argv[3]))
    def _solve_ISR(V, E, S, T, graph_path, sol_path):
        return solve_ISR(V, E, S, T, graph_path, sol_path)
    try:
        _solve_ISR(V, E, S, T, graph_path, sol_path)
        print("o,solved")
    except TimeoutError:
        print("o,timeover")
