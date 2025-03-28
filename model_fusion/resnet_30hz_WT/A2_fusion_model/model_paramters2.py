import torch  
from torchinfo import summary 
# 加载模型  
model = torch.load('A2_fusion_model\model\model_Resnet18.pth')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# 打印模型摘要
input_tensor1 = torch.randn(32, 1, 17, 97)
input_tensor2 = torch.randn(32, 1, 128, 1536)
input1 = input_tensor1.to(device)
input2 = input_tensor2.to(device)

summary(model, input_data=[input_tensor1, input_tensor2], device=device,col_names=[ "input_size", "output_size", "num_params",  "kernel_size", "trainable"],
    verbose=1)


# import torch  
# #详细参数################
# # 加载模型  
# model = torch.load('A2_fusion_model\model\model_Resnet18.pth')  

# # 查看模型参数  
# for name, param in model.named_parameters():  
#     print(f'Name: {name}, Shape: {param.shape}')
#     # print(f'Name: {name}, Shape: {param.shape}, Data: {param.data},Dtype:{param.dtype}')

