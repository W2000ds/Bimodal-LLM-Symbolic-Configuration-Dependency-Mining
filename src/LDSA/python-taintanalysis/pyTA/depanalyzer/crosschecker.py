import csv
from collections import defaultdict

class VarControlFlowCrossChecker:
    def __init__(self, var_file, cf_file, output_file):
        self.var_file = var_file
        self.cf_file = cf_file
        self.output_file = output_file

    def load_vars(self):
        vars_by_file = defaultdict(list)
        with open(self.var_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0].startswith("#"):
                    continue
                varname, localname, lineno, filepath = row
                vars_by_file[filepath].append({
                    "varname": varname,
                    "localname": localname,
                    "lineno": int(lineno)
                })
        return vars_by_file

    def load_controlflows(self):
        cf_by_file = defaultdict(list)
        with open(self.cf_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header_skipped = False
            for row in reader:
                if not header_skipped:
                    header_skipped = True
                    continue
                if not row or row[0].startswith("#"):
                    continue
                cf_type, start, end, filepath = row
                cf_by_file[filepath].append({
                    "type": cf_type,
                    "start": int(start),
                    "end": int(end)
                })
        return cf_by_file

    def check(self):
        vars_by_file = self.load_vars()
        cf_by_file = self.load_controlflows()
        results = []
        # 用于same_controlflow去重：key为 (filepath, cf_type, cf_start, cf_end, var1, var2)
        controlflow_seen = set()

        for filepath, varlist in vars_by_file.items():
            cfs = cf_by_file.get(filepath, [])
            for i in range(len(varlist)):
                for j in range(i+1, len(varlist)):
                    v1, v2 = varlist[i], varlist[j]
                    # 跳过同名变量
                    if v1["varname"] == v2["varname"]:
                        continue
                    # 保留变量名和local变量名
                    pair = tuple(sorted([
                        (v1["varname"], v1["localname"]),
                        (v2["varname"], v2["localname"])
                    ]))
                    # 检查同一控制流
                    for cf in cfs:
                        if (cf["start"] <= v1["lineno"] <= cf["end"] and
                            cf["start"] <= v2["lineno"] <= cf["end"]):
                            cf_key = (
                                filepath, cf["type"], cf["start"], cf["end"], pair[0], pair[1]
                            )
                            if cf_key not in controlflow_seen:
                                controlflow_seen.add(cf_key)
                                results.append((
                                    filepath,
                                    cf["type"],
                                    cf["start"],
                                    cf["end"],
                                    v1["lineno"],
                                    v2["lineno"],
                                    pair[0][0], pair[0][1],  # var1, localvar1
                                    pair[1][0], pair[1][1],  # var2, localvar2
                                    "same_controlflow"
                                ))
                    # 检查同一行
                    if v1["lineno"] == v2["lineno"]:
                        results.append((
                            filepath,
                            "",
                            "",
                            "",
                            v1["lineno"],
                            v2["lineno"],
                            pair[0][0], pair[0][1],
                            pair[1][0], pair[1][1],
                            "same_line"
                        ))

        with open(self.output_file, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "filepath", "controlflow_type", "cf_start_lineno", "cf_end_lineno",
                "var1_lineno", "var2_lineno",
                "var1", "localvar1", "var2", "localvar2", "relation"
            ])
            for idx, row in enumerate(sorted(results), 1):
                writer.writerow([idx] + list(row))
        print(f"[INFO] Done. Results written to {self.output_file}")