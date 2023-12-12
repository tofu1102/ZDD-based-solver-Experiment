import csv

LIST_PATH = "2022benchmark-main/list/list-all-benchmark.csv"
HEAD = "2022benchmark-main/"

def path_list():
    with open(LIST_PATH) as f:
        csvreader = csv.reader(f)

        return [(HEAD + path, HEAD + ans) for path,ans in csvreader]

if __name__ == "__main__":
    print(path_list())