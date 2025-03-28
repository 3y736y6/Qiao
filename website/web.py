from flask import Flask, render_template,jsonify,request
import ast
import torch.nn.functional as F
import torch
import pymysql
from Prediction_online import *
app = Flask(__name__,template_folder="templates")
import json

# ctrl+/多行注释
# 创建了网址  和 函数index 对应关系
# 在浏览器上访问 /,自动执行 index
# 运行后不会自动退出 需要终端Ctrl+c退出
@app.route("/")
def index_0():
    #return "str1"
    #在flask框架下，会render a file
    return render_template("0_index.html")

#这个是首页的"登录"跳转界面
@app.route("/1_index_register")
def register_index_1():
    return render_template("/home/1_index_register.html")

#这个是首页的"实验室"跳转界面
@app.route("/1_index_laboratory")
def visitor_login():
    return render_template("/home/1_index_laboratory.html")

#这个是首页的第一个项目(农机)中的"首页"跳转界面
@app.route("/2_nongji_index")
def index_nongji_2():
    return render_template("/nongji/2_nongji_index.html")

#这个是首页的第一个项目(农机)中的"关于"跳转界面
@app.route("/2_nongji_about")
def about_nongji_2():
    return render_template("/nongji/2_nongji_about.html")

#这个是首页的第一个项目(农机)中的"数据"跳转界面  
@app.route("/2_nongji_data")
def data_nongji_2():
#   return render_template("data.html")
    return render_template("/nongji/2_nongji_data.html")

#这个是首页的第一个项目(农机)中的"其他"跳转界面  
@app.route("/2_nongji_other")
def other_nongji_2():
    return render_template("/nongji/2_nongji_other.html")

#服务器接收本地数据转存数据库API
@app.route('/postsignal',methods=['POST'])
def post_signal():
    error = None
    if request.method == 'POST':
        ret = {}
        ret["code"] ='OK'

        device_NO = request.json["device_NO"]
        frequency_sample = json.dumps(request.json["frequency_sample"])
        sample_points = request.json["sample_points"]
        temp_machine = request.json["temp_machine"]
        humidity_device = request.json["humidity_device"]
        temp_device = request.json["temp_device"]
        vibration = json.dumps(request.json["vibration"])
        date = request.json["date"]

        # print(SignalName,SamplePoints,SampleDate)

        conn = pymysql.connect(
            host='47.109.23.253',
            user='root',
            password='zijipojie',
            port=8306,
            database='machine1'
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 字典形式传参
        sql = '''insert into chart_data(device_NO,frequency_sample,sample_points,temp_machine,humidity_device,temp_device,vibration,date) 
                    VALUES(%(device_NO)s, %(frequency_sample)s, %(sample_points)s,%(temp_machine)s, %(humidity_device)s,%(temp_device)s, %(vibration)s,%(date)s)'''
        try:
            cursor.execute(sql, {
                "device_NO": device_NO,              
                "frequency_sample": frequency_sample,    
                "sample_points":sample_points,        
                "temp_machine": temp_machine,  
                "humidity_device": humidity_device,  
                "temp_device" : temp_device,
                "vibration": vibration,  
                "date" : date})
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
            ret["code"] ='Fail'
        finally:
            cursor.close()
            conn.close()
     
        return json.dumps(ret)  
#预测API
@app.route("/get_updated_data", methods=['GET'])
def get_updated_data():

    MODEL_PATH = r'model_Resnet18.pth'  # 模型路径
    DEVICE = 'cpu'             # 设备（'cpu' 或 'cuda'）

    try:
        # 连接到数据库
        conn = pymysql.connect(
            host='47.109.23.253',
            user='root',
            password='zijipojie',
            port=8306,
            database='machine1'
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 查询 tb_signal_data 表中的最新一条数据
        sql_signal = "SELECT * FROM chart_data ORDER BY id DESC LIMIT 1 "
        cursor.execute(sql_signal)
        signal_row = cursor.fetchone()

        if signal_row:
            str_vibration = signal_row.get("vibration")   
            lisy_vibration = ast.literal_eval(str_vibration)  # 'str'  --> list


            # 预加载模型（每次请求时加载模型）
            try:
                model = torch.load(MODEL_PATH, map_location=DEVICE)
                model.eval()
            except Exception as e:
                return jsonify({"error": f"模型加载失败: {e}"}), 500


            # 调用预测函数进行预测
            probabilities, result = predict_sample_vibrate(lisy_vibration, MODEL_PATH, DEVICE)
            if probabilities is None or result is None:
                return jsonify({"error": "预测失败"}), 500
            print("probabilities",probabilities)
            print("result", result)
            # 将原始分数转换为概率
            probabilities_tensor = torch.tensor(probabilities)
            probabilities_softmax = F.softmax(probabilities_tensor, dim=0)
            probabilities = probabilities_softmax.tolist()
            print("probabilities1", probabilities)
            # 格式化概率值，保留六位小数
            probabilities = [round(prob, 6) for prob in probabilities]
            print("probabilities2", probabilities)
            classes = ('Z', 'W1', 'W2', 'N1', 'N2', 'G1', 'G2')
            probability_dict = {cls: prob for cls, prob in zip(classes, probabilities)}
            print("probability_dict", probability_dict)
            # 返回数据库数据和预测结果
            return jsonify({
                
                "device_NO": signal_row.get("device_NO"),
                "frequency_sample": signal_row.get("frequency_sample"),
                "sample_points": signal_row.get("sample_points"),
                "temp_machine": signal_row.get("temp_machine"),
                "humidity_device": signal_row.get("humidity_device"),
                "temp_device": signal_row.get("temp_device"),
                "date": signal_row.get("date"),


                "SampleVibrate": lisy_vibration,
                "Prediction": {
                "probability": probability_dict,
                "result": result
                }
            })
        else:
            return jsonify({"error": "No data found"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass



# 三创
# #@app.route("/sanchuang_one")
# def sanchuang1():
#     return render_template("/sanchuang/sanchuang1.html")
# @app.route("/sanchuang_two")
# def sanchuang2():
#     return render_template("/sanchuang/sanchuang2.html")


if __name__ == '__main__':
    app.run(host = "127.0.0.1" ,port=9988 )  
    # nginx+uwsgi作为中间层，会将请求转发至本地9988端口
    # host = "127.0.0.1" ,port=9988 flask监听本地9988端口

    # 云主机地址 "172.22.99.106"