from bs4 import BeautifulSoup
import csv

# 读取 HTML 文件内容
with open("ManualParser/python-manual/cinder.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# 查找所有表格
tables = soup.find_all("table", class_="config-ref-table")

# 存储提取的数据
data = []

# 遍历每个表格
for table in tables:
    # 获取表格标题作为 section 名
    caption = table.find("caption")
    section_name = caption.get_text(strip=True) if caption else "Unknown Section"

    # 跳过表头，遍历每一行配置项
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) >= 2:
            config_td, desc_td = cols
            config_code = config_td.find("code")
            if config_code:
                full_config = config_code.get_text(strip=True)
                config_name = full_config.split("=")[0].strip()
                description = desc_td.get_text(strip=True)
                data.append((config_name, description, section_name))

# 写入 CSV 文件
with open("ManualParser/python-manual/cinder_config_options.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["config_name", "description", "section"])
    writer.writerows(data)

print("配置项已成功提取到 ManualParser/python-manual/cinder_config_options.csv 文件中。")
