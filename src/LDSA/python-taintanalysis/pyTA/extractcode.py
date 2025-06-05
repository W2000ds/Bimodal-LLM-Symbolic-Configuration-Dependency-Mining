import csv
import os

def extract_lines(filepath, start, end):
    """提取文件中从start到end（包含）的代码行，行号从1开始"""
    if not os.path.isfile(filepath):
        return ""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()
    # 行号从1开始，Python索引从0
    start = max(1, start)
    end = min(len(lines), end)
    snippet = "".join(lines[start-1:end])
    return snippet.strip()

def process(depresult_csv, output_csv):
    with open(depresult_csv, newline='', encoding='utf-8') as fin, \
         open(output_csv, "w", newline='', encoding='utf-8') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        header = next(reader)
        writer.writerow(header + ["code_snippet"])
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            filepath = row[1]
            relation = row[-1]
            if relation == "same_line":
                try:
                    lineno = int(row[5])
                except ValueError:
                    writer.writerow(row + [""])
                    continue
                snippet = extract_lines(filepath, lineno-10, lineno+9)
            elif relation == "same_controlflow":
                try:
                    cf_start = int(row[3])
                    cf_end = int(row[4])
                except ValueError:
                    writer.writerow(row + [""])
                    continue
                snippet = extract_lines(filepath, cf_start, cf_end)
            else:
                snippet = ""
            writer.writerow(row + [snippet])

if __name__ == "__main__":
    # 修改为你的实际路径
    softwarelist = ["glance","cinder"]
    for software in softwarelist:
        depresult_csv = f"result/depresult/{software}.csv"
        output_csv = f"result/depresult/{software}_with_code.csv"
        process(depresult_csv, output_csv)
        print(f"[INFO] Done. Output: {output_csv}")