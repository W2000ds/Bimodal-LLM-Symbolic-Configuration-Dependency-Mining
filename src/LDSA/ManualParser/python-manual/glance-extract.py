from bs4 import BeautifulSoup
import csv

# 假设 html_content 是你加载的 HTML 字符串
with open("ManualParser/Basic Configuration — glance 30.1.0.dev43 documentation.html", "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

results = []

# 遍历所有section
for section in soup.find_all("section"):
    section_id = section.get("id", "")
    dl = section.find("dl")
    if not dl:
        continue
    dt_tags = dl.find_all("dt")
    dd_tags = dl.find_all("dd")

    for dt, dd in zip(dt_tags, dd_tags):
        # 提取配置名，去除等号后的部分
        code_tag = dt.find("code")
        if not code_tag:
            continue
        config_full = code_tag.text.strip()
        config_name = config_full.split("=")[0].strip()

        # 提取描述
        description_parts = [p.get_text(" ", strip=True) for p in dd.find_all("p")]
        description = " ".join(description_parts)

        results.append({
            "section_id": section_id,
            "config_name": config_name,
            "description": description
        })


# 输出到 CSV
csv_file = "ManualParser/glance_config_options.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["section_id", "config_name", "description"])
    writer.writeheader()
    writer.writerows(results)

print(f"Saved {len(results)} config options to {csv_file}")
