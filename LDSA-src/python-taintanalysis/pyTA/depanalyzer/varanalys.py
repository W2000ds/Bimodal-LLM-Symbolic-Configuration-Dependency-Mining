# 污点分析参数位置
import ast
import os
from collections import defaultdict
import csv

class DependencyAnalyzer:
    def __init__(self, project_path, taresultpath):
        self.project_path = project_path
        self.taresultpath = taresultpath

    class FunctionCallLinker(ast.NodeVisitor):
        def __init__(self, filename, reverse_dependencies):
            self.reverse_dependencies = reverse_dependencies
            self.scope_stack = []
            self.filename = filename

        def current_scope(self):
            return ".".join(self.scope_stack) if self.scope_stack else "<global>"

        def scoped(self, name):
            return f"{self.current_scope()}.{name}"

        def visit_FunctionDef(self, node):
            self.scope_stack.append(node.name)
            self.generic_visit(node)
            self.scope_stack.pop()

        def visit_Assign(self, node):
            right_vars = set()

            def try_extract(node_):
                if isinstance(node_, ast.Attribute):
                    full_name = DependencyAnalyzer.extract_full_attribute_name(node_)
                    if full_name:
                        right_vars.add(self.scoped(full_name))
                elif isinstance(node_, ast.Name):
                    right_vars.add(self.scoped(node_.id))

            try_extract(node.value)
            for n in ast.walk(node.value):
                try_extract(n)
            for target in node.targets:
                if isinstance(target, ast.Name):
                    for var in right_vars:
                        self.reverse_dependencies[var].add((self.scoped(target.id), self.filename, node.lineno))

    class ScopedVarDependencyAnalyzer(ast.NodeVisitor):
        def __init__(self, filename):
            self.reverse_dependencies = defaultdict(set)
            self.scope_stack = []
            self.filename = filename

        def current_scope(self):
            return ".".join(self.scope_stack) if self.scope_stack else "<global>"

        def scoped(self, name):
            return f"{self.current_scope()}.{name}"

        def visit_FunctionDef(self, node):
            self.scope_stack.append(node.name)
            self.generic_visit(node)
            self.scope_stack.pop()

        def visit_Attribute(self, node):
            full_name = DependencyAnalyzer.extract_full_attribute_name(node)
            if full_name:
                self.reverse_dependencies[full_name].add(
                    (f"<read>", self.filename, node.lineno)
                )
            self.generic_visit(node)

        def visit_Assign(self, node):
            right_vars = set()
            for n in ast.walk(node.value):
                if isinstance(n, ast.Name):
                    right_vars.add(self.scoped(n.id))
                elif isinstance(n, ast.Attribute):
                    full_name = DependencyAnalyzer.extract_full_attribute_name(n)
                    if full_name:
                        right_vars.add(self.scoped(full_name))
            for target in node.targets:
                if isinstance(target, ast.Name):
                    for var in right_vars:
                        self.reverse_dependencies[var].add(
                            (self.scoped(target.id), self.filename, node.lineno)
                        )
            self.generic_visit(node)

        def visit_Return(self, node):
            if isinstance(node.value, ast.Name):
                returned_var = self.scoped(node.value.id)
                func_name = self.current_scope()
                self.reverse_dependencies[returned_var].add((f"<return>.{func_name}", self.filename, node.lineno))
            self.generic_visit(node)

    @staticmethod
    def extract_full_attribute_name(node):
        if isinstance(node, ast.Attribute):
            base = DependencyAnalyzer.extract_full_attribute_name(node.value)
            if base:
                return f"{base}.{node.attr}"
            return node.attr
        elif isinstance(node, ast.Name):
            return node.id
        else:
            return None

    def analyze_project_dependencies_scoped(self):
        all_reverse_deps = defaultdict(set)
        for root, _, files in os.walk(self.project_path):
            for fname in files:
                if fname.endswith(".py"):
                    path = os.path.join(root, fname)
                    with open(path, 'r') as f:
                        tree = ast.parse(f.read(), filename=path)
                        analyzer = self.ScopedVarDependencyAnalyzer(path)
                        analyzer.visit(tree)
                        for src, tgts in analyzer.reverse_dependencies.items():
                            all_reverse_deps[src].update(tgts)
        for root, _, files in os.walk(self.project_path):
            for fname in files:
                if fname.endswith(".py"):
                    path = os.path.join(root, fname)
                    with open(path, 'r') as f:
                        tree = ast.parse(f.read(), filename=path)
                        linker = self.FunctionCallLinker(path, all_reverse_deps)
                        linker.visit(tree)
        return all_reverse_deps

    def trace_forward_chain_scoped(self, reverse_deps, scoped_varname, max_depth=10):
        chain = set()
        seen = set()
        def dfs(v, depth):
            if v in seen or depth >= max_depth:
                return
            seen.add(v)
            chain.add(v)
            for u in reverse_deps.get(v, []):
                dfs(u[0], depth + 1)
        dfs(scoped_varname, 0)
        return chain

    def run_var_traces(self, target_var):
        deps = self.analyze_project_dependencies_scoped()
        matched_vars = [var for var in deps if target_var in var]
        if not matched_vars:
            print(f"No variable containing '{target_var}' found.")
            return
        print(f"\nFound {len(matched_vars)} variable(s) containing '{target_var}':")
        rows = []
        for a_var in matched_vars:
            print(f"\n=== Chain for {a_var} ===")
            chain = self.trace_forward_chain_scoped(deps, a_var)
            for var in sorted(chain):
                for dep_var, targets in deps.items():
                    for target, filename, lineno in targets:
                        if dep_var == var:
                            print(f"[INFO] {dep_var} → {target} in {filename}, line {lineno}")
                            rows.append({
                                "target_var_name": target_var,
                                "dep_var": dep_var,
                                "linenumber": lineno,
                                "filename": filename
                            })
        if rows:
            with open(self.taresultpath, "a", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["target_var_name", "dep_var", "linenumber", "filename"])
                # 不写表头
                writer.writerows(rows)
            print(f"\n[INFO] Dependency info written to {self.taresultpath}")
    
    def find_var_locations_from_csv(self, input_csv, output_csv):
        # 1. 读取变量名
        with open(input_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            varnames = [row[0] for row in reader if row]  # 跳过空行

        # 2. 分析依赖
        deps = self.analyze_project_dependencies_scoped()
        rows = []
        for variablename in varnames:
            for dep_var, targets in deps.items():
                if variablename in dep_var:
                    for target, filename, lineno in targets:
                        rows.append({
                            "variablename": variablename,
                            "localvariablename": dep_var,
                            "filepath": filename,
                            "linenumber": lineno
                        })

        # 3. 写入新csv
        with open(output_csv, "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["variablename", "localvariablename", "filepath", "linenumber"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"[INFO] Variable locations written to {output_csv}")

# 用法示例（可删除）：

if __name__ == "__main__":
    analyzer = DependencyAnalyzer("apps/glance/", "taresult/test.csv")

    input_csv = "test.csv"

    with open(input_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            varnames = [row[0] for row in reader if row]  # 跳过空行
            for variablename in varnames:
                analyzer.run_var_traces(variablename)