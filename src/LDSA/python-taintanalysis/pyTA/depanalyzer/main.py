# 污点分析控制
import csv

from varanalys import DependencyAnalyzer
from controlflow import ControlFlowAnalyzer
from crosschecker import VarControlFlowCrossChecker

softwarelist = ["glance","cinder"]

for software in softwarelist:

    analyzer = DependencyAnalyzer(f"apps/{software}/", f"result/taresult/{software}.csv")

    var_csv = f"configfile/{software}-defaultConfig.csv"

    # with open(var_csv, newline='') as csvfile:
    #         reader = csv.reader(csvfile)
    #         varnames = [row[0] for row in reader if row]  # 跳过空行
    #         for variablename in varnames:
    #             analyzer.run_var_traces(variablename)

    # analyzer = ControlFlowAnalyzer(f"apps/{software}/", f"result/controlflow/{software}controlflow_result.csv")
    # analyzer.analyze_project()

    checker = VarControlFlowCrossChecker(f"result/taresult/{software}.csv", f"result/controlflow/{software}controlflow_result.csv", f"result/depresult/{software}.csv")
    checker.check()