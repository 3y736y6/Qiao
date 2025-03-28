#  #迁移学习 
# model_weight_path = "./vgg16-pre.pth"
# assert os.path.exists(model_weight_path), "file {} does not exist.".format(model_weight_path)
# net.load_state_dict(torch.load(model_weight_path, map_location='cpu'),False)
# for param in net.parameters():
#     param.requires_grad = False
# n_inputs=net.classifier[6].in_features
# last_layer=nn.Linear(n_inputs,4)
# net.classifier[6]=last_layer


# # official pretrain weights
# #预训练的权重下载地址    # 预训练（迁移学习）  # 与权重预设不是一个东西
# model_urls = {
#     'vgg11': 'https://download.pytorch.org/models/vgg11-bbd30ac9.pth',
#     'vgg13': 'https://download.pytorch.org/models/vgg13-c768596a.pth',
#     'vgg16': 'https://download.pytorch.org/models/vgg16-397923af.pth',
#     'vgg19': 'https://download.pytorch.org/models/vgg19-dcbb9e9d.pth'
# }