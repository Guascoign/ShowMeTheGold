import os
import time
import configparser
from collections import Counter

def conv2Gold(amount_str):
    """将整数金额字符串转换为金银铜格式"""
    try:
        amount = int(amount_str)
    except ValueError:
        return amount_str  # 如果无法转换为整数，则返回原始字符串

    return f"{amount // 10000}g {amount // 100 % 100}s {amount % 100}c"

def export_to_txt(directory, filename, data, formatted_date):
    """将数据导出到指定目录和文件名的文本文件"""
    # 确保目录存在
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"{filename}\n")
        f.write("物品ID\t最低价格\t平均价格\t拍卖数量\t物品数量\t数据更新时间\n")
        for item in data:
            f.write(f"{item['item_name']}\t{item['min_price']}\t{item['ave_price']}\t{item['auction_num']}\t{item['quantity']}\t{item['scan_time']}\n")
    return filepath

def get_most_common_scan_time(data):
    """获取数据中 数据更新时间重复出现最多的日期"""
    scan_times = [item['scan_time'] for item in data]
    count = Counter(scan_times)
    most_common_scan_time = count.most_common(1)[0][0]
    return most_common_scan_time

def read_lua_and_export():
    # 读取配置文件中的路径
    config = configparser.ConfigParser()
    config_path = '../config.ini'  # 使用相对路径访问上层目录中的配置文件
    if not os.path.exists(config_path):
        print(f"Configuration file '{config_path}' not found.")
        return

    config.read(config_path)
    if 'Paths' not in config:
        print(f"Section 'Paths' not found in the configuration file.")
        return

    lua_file = config['Paths'].get('lua_file')
    output_directory = config['Paths'].get('output_directory')

    if not os.path.exists(lua_file):
        print(f"File '{lua_file}' not found.")
        return

    with open(lua_file, 'r', encoding='utf-8') as f:
        lua_content = f.read()

        # 找到包含拍卖行数据的配置
        lines = lua_content.split('\n')
        for line in lines:
            if 'csvAuctionDBScan' in line:
                idx_name_start = line.find('internalData@csvAuctionDBScan')
                sub_name = line[5:idx_name_start-1]

                idx_start = line.find('lastScan')
                sub_str = line[idx_start + 10:-2]
                items = sub_str.split('\\n')

                data_to_export = []
                for item in items:
                    details = item[2:].strip(',').split(',')
                    if len(details) == 6:
                        data_to_export.append({
                            'item_name': details[0],
                            'min_price': details[1],
                            'ave_price': details[2],
                            'auction_num': details[3],
                            'quantity': details[4],
                            'scan_time': details[5]
                        })

                if data_to_export:
                    most_common_time = get_most_common_scan_time(data_to_export)
                    formatted_date = time.strftime('%Y_%m%d_%H%M', time.localtime(int(most_common_time)))
                    directory = os.path.join(output_directory, f"{sub_name}")
                    filename = f"{sub_name}_{formatted_date}.txt"
                    filepath = export_to_txt(directory, filename, data_to_export, formatted_date)
                    print(f"Data exported to '{filepath}'.")

# 主函数入口
if __name__ == "__main__":
    read_lua_and_export()
