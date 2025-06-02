import os
import csv
import subprocess
import re

class CodeExtractor:
    def __init__(self, TA_resultcsv, root_dir, Code_Basecsv):
        self.csv_file = TA_resultcsv
        self.root_dir = root_dir
        self.output_csv_file = Code_Basecsv
        self.extract_code()

    # def class_name_to_file_path(self, class_name):
    #     """将类名转换为文件路径"""
    #     file_path = class_name.replace('.', os.sep) + '.java'
    #     return os.path.join(self.root_dir, file_path)

    def build_method_pattern(self, return_type, method_name, param_count):
        """构造方法匹配的正则表达式"""
        simplified_return_type = return_type.split('.')[-1]
        if param_count > 0:
            param_pattern = r'\s*\w+\s+\w+(?:\s*,\s*\w+\s+\w+){' + str(param_count - 1) + '}'
        else:
            param_pattern = r'\s*'
        full_pattern = (
            rf'\b(?:public|protected|private|static|final)?\s+'  # 可选修饰符
            rf'{re.escape(simplified_return_type)}\s+'           # 返回值类型
            rf'{re.escape(method_name)}'                         # 方法名
            rf'\s*\('                                           # 匹配左括号
            rf'{param_pattern}'                                 # 参数列表
            rf'\)\s*'                                          # 匹配右括号
            r'.*\s*{'                                          # 方法体开始
        )
        return re.compile(full_pattern)

    def get_function_code(self, lines, return_type, method_name, param_count, line_number):
        """获取方法定义的完整代码块"""
        if method_name is None and return_type is None:
            start_line = max(0, line_number - 11)
            end_line = min(len(lines), line_number + 10)
            function_lines = [lines[i].strip() for i in range(start_line, end_line)]
            return "\n".join(function_lines)

        method_pattern = self.build_method_pattern(return_type, method_name, param_count)

        inside_function = False
        brace_count = 0
        function_lines = []

        for line in lines:
            if not inside_function:
                if method_pattern.search(line):  # 匹配方法定义
                    inside_function = True
                    brace_count += line.count('{') - line.count('}')
                    function_lines.append(line.strip())
            else:
                brace_count += line.count('{') - line.count('}')
                function_lines.append(line.strip())
                if brace_count == 0:  # 大括号匹配结束
                    break

        return "\n".join(function_lines)

    def get_line_code(self, lines, line_number):
        """获取指定行号的代码"""
        if 1 <= line_number <= len(lines):
            return lines[line_number - 1].strip()
        return "Error: Line number out of range."

    def parse_method_signature(self, method_signature):
        """解析方法签名，提取返回值类型、方法名和参数数量"""
        pattern = re.compile(r'^\s*(\w+)\s+(\w+)\((.*?)\)\s*$')
        match = pattern.match(method_signature.strip())
        if not match:
            return None, None, None

        return_type = match.group(1)
        method_name = match.group(2)
        parameters = match.group(3)
        param_count = 0 if not parameters.strip() else len(parameters.split(','))
        return return_type, method_name, param_count


    def extract_code(self):
        with open(self.csv_file, mode='r', encoding='utf-8') as file, \
             open(self.output_csv_file, mode='w', newline='', encoding='utf-8') as out_file:
            reader = csv.reader(file, delimiter=',')
            writer = csv.writer(out_file)
            rows = list(reader)

            # 写入表头
            writer.writerow(["QID", "Parameter1", "Parameter2" , "Line Code", "Method Code"])

            i = 0
            # 从第二行开始处理 CSV 中的数据
            for row in rows[1:]:
                try:
                    if len(row) < 7:
                        writer.writerow([f"Warning: Row with insufficient columns: {row}", "", ""])
                        continue
                    id = i+ 1
                    i += 1
                    para1 = row[1]
                    para2 = row[2]
                    class_name = row[4]       # 完整包名+类名，例如：org.apache.hadoop.net.SocketIOWithTimeout
                    method_signature = row[5]
                    line_number = int(row[7])

                    return_type, method_name, param_count = self.parse_method_signature(method_signature)

                    package_relative_path = class_name.replace('.', '/') + ".java"
                    pattern = f"*/{package_relative_path}"
                    try:
                        result = subprocess.run(
                            ["find", ".", "-type", "f", "-path", pattern],
                            cwd=self.root_dir,
                            stdout=subprocess.PIPE,
                            text=True,
                            check=True
                        )
                        candidates = result.stdout.strip().splitlines()
                        if candidates:
                            candidate = candidates[0]
                            if candidate.startswith("./"):
                                candidate = candidate[2:]
                            file_path = os.path.join(self.root_dir, candidate)
                    except Exception as e:
                        print(f"Find command failed: {e}")

                    if os.path.isfile(file_path):
                        with open(file_path, 'r', encoding='utf-8') as java_file:
                            lines = java_file.readlines()

                        method_code = self.get_function_code(lines, return_type, method_name, param_count, line_number)
                        line_code = self.get_line_code(lines, line_number)

                    writer.writerow([id, para1, para2, line_code, method_code])

                except Exception as e:
                    writer.writerow([id, para1, para2, "ERROR OCCURRED", "ERROR OCCURRED"])
                    print(f"Error processing row {row}: {str(e)}")

if __name__ == '__main__':
    TA_resultcsv = '/dataset-hadoop-3.3.5/cdepdataset/cdep2.0result/cdep-hdfs.csv'
    root_dir = '/home/lhy/cDep/cdep2/cdep-fse-ae/app/hadoop-2.9.2-src/'
    Code_Basecsv = '/CodeDepBase.csv'

    extractor = CodeExtractor(TA_resultcsv, root_dir, Code_Basecsv)

    extractor.extract_code()