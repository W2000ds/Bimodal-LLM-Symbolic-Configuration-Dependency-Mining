import ast
import os
import csv
from typing import List, Dict, Optional, Tuple

class ControlFlowAnalyzer:

    
    # 支持的控制流节点类型
    CONTROL_FLOW_NODES = (
        ast.If,
        ast.For,
        ast.While,
        ast.Try,
        ast.With,
        ast.AsyncFor,
        ast.AsyncWith,
        ast.IfExp,  # 三元表达式
    )
    
    # 尝试动态获取Match节点（Python 3.10+）
    try:
        CONTROL_FLOW_NODES += (getattr(ast, "Match", None),)
    except AttributeError:
        pass
    
    def __init__(self, project_dir: str, output_csv: str = "controlflow_result.csv"):

        self.project_dir = project_dir
        self.output_csv = output_csv
    
    def _is_control_flow_node(self, node) -> bool:

        return any(isinstance(node, cf_type) for cf_type in self.CONTROL_FLOW_NODES)
    
    def _get_node_lines(self, node) -> Tuple[int, int]:

        start_lineno = getattr(node, "lineno", -1)
        # end_lineno 仅 Python 3.8+ 支持
        end_lineno = getattr(node, "end_lineno", start_lineno)
        return start_lineno, end_lineno
    
    def analyze_file(self, filepath: str) -> List[Dict]:

        results = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source, filename=filepath)
            
            for node in ast.walk(tree):
                if self._is_control_flow_node(node):
                    node_type = type(node).__name__
                    start_lineno, end_lineno = self._get_node_lines(node)
                    results.append({
                        "type": node_type,
                        "start_lineno": start_lineno,
                        "end_lineno": end_lineno,
                        "filepath": filepath
                    })
        except Exception as e:
            print(f"[WARNING] Failed to parse {filepath}: {str(e)}")
        
        return results
    
    def analyze_project(self) -> None:

        rows = []
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    rows.extend(self.analyze_file(filepath))
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(self.output_csv) or ".", exist_ok=True)
        
        with open(self.output_csv, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["type", "start_lineno", "end_lineno", "filepath"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"[INFO] Control flow statements written to {self.output_csv}")
    
    @classmethod
    def analyze_single_file(cls, filepath: str, output_csv: str = None) -> None:

        if output_csv is None:
            output_csv = os.path.splitext(filepath)[0] + "_controlflow.csv"
        
        results = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source, filename=filepath)
            
            for node in ast.walk(tree):
                if any(isinstance(node, cf_type) for cf_type in cls.CONTROL_FLOW_NODES):
                    node_type = type(node).__name__
                    start_lineno, end_lineno = cls._get_node_lines_static(node)
                    results.append({
                        "type": node_type,
                        "start_lineno": start_lineno,
                        "end_lineno": end_lineno,
                        "filepath": filepath
                    })
        except Exception as e:
            print(f"[WARNING] Failed to parse {filepath}: {str(e)}")
        

        os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
        
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["type", "start_lineno", "end_lineno", "filepath"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"[INFO] Control flow statements written to {output_csv}")
    
    @staticmethod
    def _get_node_lines_static(node) -> Tuple[int, int]:

        start_lineno = getattr(node, "lineno", -1)
        # end_lineno 仅 Python 3.8+ 支持
        end_lineno = getattr(node, "end_lineno", start_lineno)
        return start_lineno, end_lineno



if __name__ == "__main__":

    analyzer = ControlFlowAnalyzer("your_project_directory")
    analyzer.analyze_project()

    # ControlFlowAnalyzer.analyze_single_file("path/to/your/file.py")