import sys
import torch
import numpy as np
import os
import pymysql
from contextlib import closing

# 添加模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, 'model', '3ResNet')
sys.path.append(module_dir)

def get_last_sample_vibrate(host='127.0.0.1', user='root', password='123456', database='web1'):
    """
    从数据库中获取 tb_signal_data 表的最后一行的 SampleVibrate 数据。

    参数:
        host (str): 数据库主机地址。
        user (str): 数据库用户名。
        password (str): 数据库密码。
        database (str): 数据库名称。

    返回:
        list: SampleVibrate 数据列表。
    """
    try:
        with closing(pymysql.connect(host=host,
                                     user=user,
                                     password=password,
                                     database=database,
                                     charset='utf8mb4')) as connection:
            with closing(connection.cursor()) as cursor:
                # 查询最后一行数据（按 ID 降序排列，限制为 1）
                sql = "SELECT SampleVibrate FROM tb_signal_data ORDER BY ID DESC LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    sample_vibrate_str = result[0]
                    # 假设 SampleVibrate 是以空格分隔的字符串
                    sample_vibrate = [float(item) for item in sample_vibrate_str.split()]
                    return sample_vibrate
                else:
                    raise ValueError("tb_signal_data 表中没有数据。")
    except Exception as e:
        print(f"从数据库获取数据时发生错误: {e}")
        return None

def prediction(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='web1',
    model_path=r'C:\Users\董斌\PycharmProjects\web\model\3ResNet\model\model_Resnet18.pth',
    device="cpu"
):
    try:
        # 从数据库获取最后一行的 SampleVibrate 数据
        input_data = get_last_sample_vibrate(host, user, password, database)
        if input_data is None:
            raise ValueError("未能获取有效的 SampleVibrate 数据。")

        input_array = np.array(input_data, dtype=np.float32)
        input_tensor = torch.from_numpy(input_array).unsqueeze(0).unsqueeze(1).to(device)

        # 加载模型
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件未找到: {model_path}")
        model = torch.load(model_path, map_location=device)
        model = model.to(device)
        model.eval()

        # 进行预测
        with torch.no_grad():
            output = model(input_tensor)
            predicted_class = output.argmax(dim=1).item()
            probabilities = output.view(-1).tolist()
            classes = ('Z', 'W1', 'W2', 'N1', 'N2', 'G1', 'G2')
            result = classes[predicted_class]
            print(probabilities)
            print(result)
            return probabilities, result
    except Exception as e:
        print(f"预测过程中发生错误: {e}")
        return None, None
def get_last_sample_vibrate(host='127.0.0.1', user='root', password='123456', database='web1'):
    """
    从数据库中获取 tb_signal_data 表的最后一行的 SampleVibrate 数据。

    参数:
        host (str): 数据库主机地址。
        user (str): 数据库用户名。
        password (str): 数据库密码。
        database (str): 数据库名称。

    返回:
        list: SampleVibrate 数据列表，若获取失败则返回 None。
    """
    try:
        with closing(pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )) as connection:
            with closing(connection.cursor()) as cursor:
                # 查询最后一行数据（按 ID 降序排列，限制为 1）
                sql = "SELECT SampleVibrate FROM tb_signal_data ORDER BY ID DESC LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    sample_vibrate_str = result[0]
                    # 假设 SampleVibrate 是以空格分隔的字符串
                    sample_vibrate = [float(item) for item in sample_vibrate_str.split()]
                    return sample_vibrate
                else:
                    raise ValueError("tb_signal_data 表中没有数据。")
    except Exception as e:
        print(f"从数据库获取数据时发生错误: {e}")
        return None

def predict_sample_vibrate(sample_vibrate, model_path, device="cpu"):
    """
    使用提供的 SampleVibrate 数据进行预测。

    参数:
        sample_vibrate (list): SampleVibrate 数据列表。
        model_path (str): 模型文件的路径。
        device (str): 设备类型，如 "cpu" 或 "cuda"。

    返回:
        tuple: (概率列表, 预测结果) 或 (None, None) 若预测失败。
    """
    try:
        if not sample_vibrate:
            raise ValueError("SampleVibrate 数据为空。")

        # 转换为张量
        input_array = np.array(sample_vibrate, dtype=np.float32)
        input_tensor = torch.from_numpy(input_array).unsqueeze(0).unsqueeze(1).to(device)

        # 加载模型
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件未找到: {model_path}")
        model = torch.load(model_path, map_location=device)
        model = model.to(device)
        model.eval()

        # 进行预测
        with torch.no_grad():
            output = model(input_tensor)
            predicted_class = output.argmax(dim=1).item()
            probabilities = output.view(-1).tolist()
            classes = ('Z', 'W1', 'W2', 'N1', 'N2', 'G1', 'G2')
            result = classes[predicted_class]
            print(probabilities)
            print(result)
            return probabilities, result
    except Exception as e:
        print(f"预测过程中发生错误: {e}")
        return None, None

if __name__ == "__main__":
    prediction()
