import re
import sys
def main(filepath):
    """
    遷移列の出力前に改行が入っていないバグがあるから、それを解消する
    対応するバグの詳細
    ・最初の遷移に関する出力の前に改行が入っていない
    12345r,12333,1141...
    ↓
    12345
    r,12333,1141...
    rの文字はこれ以外に使われていないので、正規表現を用いて"[0-9]r"を検出する。
    """
    with open(filepath) as f:
        content = f.read()
    content = re.sub("([0-9])r", r"\1\nr", content)
    with open(filepath,mode="w") as f:
        f.write(content)


if __name__ == "__main__":
    main(sys.argv[1])