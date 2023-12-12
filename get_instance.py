
def get_instance(graph_path, ans_path):
    with open(graph_path, mode="r") as f:
        data = f.read().split("\n")
    with open(ans_path, mode="r") as f:
        data += f.read().split("\n")
    #インスタンスの情報取得
    vertices = set()
    edges = []
    S, T = [], []

    for info in data:
        info = info.split()
        if len(info) == 0:continue
        if info[0] == "e":
            edges.append((info[1], info[2]))
            vertices |= set(info[1:])
        elif info[0] == "s":
            S = set(info[1:])
        elif info[0] == "t":
            T = set(info[1:])
    
    vertices = list(vertices)

    return (vertices, edges, S, T)

if __name__ == "__main__":
    print(get_instance("2022benchmark-main/benchmark/color04/1-FullIns_3.col","2022benchmark-main/benchmark/color04/1-FullIns_3_01.dat"))