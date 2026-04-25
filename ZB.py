import json
import random
import sys
import os

def resource_path(relative_path):
    """ 获取程序运行时的资源路径（兼容打包后的环境） """
    try:
        # PyInstaller 打包后的临时存放路径
        base_path = sys._MEIPASS
    except Exception:
        # 未打包时的当前路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def draw_final_gua(sequence, info):
    """
    最终展示：加入颜色，并使用全角空格优化阴爻对齐
    """
    RED = "\033[31m"
    RESET = "\033[0m"
    
    print("\n" + "═"*34)
    header = f"{info['symbol']} {info['name']}"
    print(f"{header.center(30)}")
    print("═"*34)
    
    for i in range(5, -1, -1):
        bit = sequence[i]
        if bit == "1":
            print(f"    {RED}████████████████{RESET}    ")
        else:
            print(f"    ██████　　　　██████    ")
            
    print("═"*34)
    print(f"二进制序列 (初->上): {sequence}")

def start_divination():
    # 使用 resource_path 动态获取 JSON 文件的位置
    json_path = resource_path('64G.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            i_ching_data = json.load(f)
    except Exception as e:
        print(f"请确保 {json_path} 在相应目录下。错误: {e}")
        return

    print("--- 易经起卦 · 交互版 ---")
    gua_sequence = ""
    
    for i in range(6):
        input(f"\n[ 正在起卦... 按回车掷出第 {i+1} 爻 ]")
        res = str(random.randint(0, 1))
        gua_sequence += res
        
        status = "【 阳 】" if res == "1" else "【 阴 】"
        print(f">>> 第 {i+1} 爻结果为：{status}")

    info = i_ching_data.get(gua_sequence)
    if info:
        draw_final_gua(gua_sequence, info)
    else:
        print(f"\n序列 {gua_sequence} 在数据库中未找到，请检查 64G.json")
    
    input("\n起卦完成，按回车键退出...") # 保持窗口，防止打包后瞬间消失

if __name__ == "__main__":
    start_divination()