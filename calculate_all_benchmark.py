import get_all_benchmark_path
import solve_ISR
import get_instance
import make_csv_from_log
from timeout_decorator import timeout, TimeoutError
import glob

def main():
    return
    already_calculated = set(glob.glob("results/*"))

    instances = get_all_benchmark_path.path_list()
    for graph_path, ans_path in instances:
        try:
            name = (graph_path+ "_" +ans_path).replace("/","_").replace(".","_")
            if "results/" + name + ".csv" in already_calculated:
                continue
            V, E, S, T = get_instance.get_instance(graph_path, ans_path)
            solve_ISR.solve_ISR(V,E,S,T,name)
            make_csv_from_log.make_csv_from_log()
        except TimeoutError:
            with open("ZDD_based_solver_log.txt",mode="a") as f:
                f.write("unsolved")
            make_csv_from_log.make_csv_from_log()
            continue

if __name__ == "__main__":
    ...
    #main()