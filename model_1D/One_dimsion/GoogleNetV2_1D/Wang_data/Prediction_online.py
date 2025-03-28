import torch
import numpy as np

def prediction(data_path = './Data/xc_src01_test2.dat',
               model_path = '1Googlenet\model\model_googlenetv2_xc_src_01_1.pkl',
               data_idx = 333,
               device = "cpu"):
    # 加载数据
    data = np.loadtxt(data_path,dtype=np.float32) # 获得一个列表
    input = data[data_idx] # 取第X个sample 
    input = torch.from_numpy(input) # 转化为tensor
    input = input.unsqueeze(0)  # 增加维度
    # 改变数据形状
    size_tmp = input.shape
    input.resize_(size_tmp[0], 1, size_tmp[1])
    input = input.to(device)

    # 加载模型  
    model = torch.load(model_path,map_location=device)  
    model = model.to(device)  
    model.eval()  # 将模型设置为评估模式

    # 进行预测  
    with torch.no_grad():  # 不需要计算梯度，也不会进行反向传播，这可以减少内存消耗并加速预测过程  
        predictions_tensor_2V = model(input)  # 得到模型的输出--2维tensor
    predicted_class = predictions_tensor_2V.argmax(dim=1).item()  # 概率最高的类别   
    predictions_list_1V = predictions_tensor_2V.view(-1).tolist() #扁平化为列表
    classes = ('Z','W1','W2','N1','N2','G1','G2')
    return predictions_list_1V,classes[predicted_class] # 返回每种情况预测值-list ， 最大可能性的结果-str


# 调用
probability,result = prediction(data_path = './Data/xc_src01_test2.dat',
            model_path = '1Googlenet\model\model_googlenetv2_xc_src_01_1.pkl',
            data_idx = 333,
            device = "cpu")
# 打印结果 
print(f"""
classification:
'Z'=  {probability[0]}
'W1'= {probability[1]}
'W2'= {probability[2]}
'N1'= {probability[3]}
'N2'= {probability[4]}
'G1'= {probability[5]}
'G2'= {probability[6]}
'result'= {result}
""")
# Ctrl+/ 多行注释
