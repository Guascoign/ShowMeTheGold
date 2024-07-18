# 定义文件路径
names_file_path = 'Names.txt'
item_strings_file_path = 'ItemStrings.txt'
database_file_path = 'DataBase.txt'

# 读取 Names.txt 文件内容
with open(names_file_path, 'r', encoding='utf-8') as names_file:
    names_content = names_file.read().strip()

# 读取 ItemStrings.txt 文件内容
with open(item_strings_file_path, 'r', encoding='utf-8') as item_strings_file:
    item_strings_content = item_strings_file.read().strip()

# 将每个文件内容按行分割
names_lines = names_content.split('\n')
item_strings_lines = item_strings_content.split('\n')

# 准备合并后的内容列表
merged_content = []

# 遍历每行并合并
for names_line, item_strings_line in zip(names_lines[9:], item_strings_lines[7:]):  # 跳过头部信息行
    # 从 Names.txt 中提取索引和名称
    names_parts = names_line.split(':')
    indices = names_parts[0].strip()
    names = ':'.join(names_parts[1:]).strip()

    # 从 ItemStrings.txt 中提取索引和物品字符串
    item_strings_parts = item_strings_line.split(':')
    item_indices = item_strings_parts[0].strip()
    item_strings = ':'.join(item_strings_parts[1:]).strip()

    # 组合成合并后的格式
    merged_line = f"{indices}: {names}\t\t{item_strings}"
    merged_content.append(merged_line)

# 将合并后的内容写入到 DataBase.txt 文件中
with open(database_file_path, 'w', encoding='utf-8') as database_file:
    database_file.write('\n'.join(merged_content) + '\n')

print(f"合并数据已写入到 {database_file_path}")
