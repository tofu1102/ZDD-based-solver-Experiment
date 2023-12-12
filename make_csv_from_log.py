import csv
FILE_PATH = "ZDD_based_solver_log.txt"

def make_csv_from_log():
    header = ["step", "size", "zdd", "time"]
    with open(FILE_PATH, mode="r") as log:
        data = log.readlines()
    
    data = list(map(lambda x: x.rstrip().split(), data))

    with open(FILE_PATH, mode="w") as log:
        #すでに読み取ったログは消去
        pass

    filename = data.pop(0)[0]
    with open(f"results/{filename}.csv", mode="w") as f:
        print(",".join(header), file=f)
        for i, d in enumerate(data):
            print(",".join([str(i)] + d), file=f)
          

if __name__ == "__main__":
    make_csv_from_log()