import re
import time

# 定义输入和输出文件路径
lua_file_path = 'TradeSkillMaster.lua'
output_file_path = 'ItemStrings.txt'

# 获取当前时间
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 读取 .lua 文件内容
with open(lua_file_path, 'r', encoding='utf-8') as file:
    lua_content = file.read()

# 定义正则表达式模式用于提取信息
names_pattern = re.compile(r'\["itemStrings"\]\s*=\s*\{([^}]*)\}', re.DOTALL)
locale_pattern = re.compile(r'\["locale"\]\s*=\s*"([^"]*)"')
revision_pattern = re.compile(r'\["revision"\]\s*=\s*"([^"]*)"')
version_pattern = re.compile(r'\["version"\]\s*=\s*(\d+)')
build_pattern = re.compile(r'\["build"\]\s*=\s*"([^"]*)"')

# 提取 names 的内容
names_match = names_pattern.search(lua_content)

if names_match:
    names_content = names_match.group(1)
else:
    print("Error: names content not found")
    exit(1)

# 提取其他元数据
locale_match = locale_pattern.search(lua_content)
revision_match = revision_pattern.search(lua_content)
version_match = version_pattern.search(lua_content)
build_match = build_pattern.search(lua_content)

# 计算总物品数量
total_items = sum(len(line.split('')) for line in names_content.strip().split('\n'))

# 准备输出的头部信息
header = f"""
**********************************************
ItemStrings.txt
locale: {locale_match.group(1)}
revision: {revision_match.group(1)}
version: {version_match.group(1)}
build: {build_match.group(1)}
ExportTime: {current_time}
Total Items: {total_items}
**********************************************
"""

# 写入输出文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(header.strip() + '\n')

    # 处理每行的 names 内容
    lines = names_content.strip().split('\n')
    for i, line in enumerate(lines):
        # 去除开头和末尾的双引号及末尾的元数据，并删除每个元素前的 "i:"
        cleaned_line = re.sub(r'^"\s*|\s*,\s*--\s*\[\d+\]$', '', line).strip()
        cleaned_line = cleaned_line.replace('i:', '')  # 删除 "i:" 前缀
        
        # 按分隔符切割 names，并处理
        names_array = cleaned_line.split('')
        for j, name in enumerate(names_array):
            cleaned_name = name.strip('"').replace('\\', '')
            output_file.write(f"    [{i+1}, {j+1}]: {cleaned_name}\n")
        
        # 每行 names 后添加一个空行
        # output_file.write("\n")
