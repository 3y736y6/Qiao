import torch
from MyDataset import MyDataset

def test(test_loader):

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model = torch.load('model\model_Resnet1D.pth')  
    model.eval()# evaluation mode

    correct = 0.0
    total = 0
    class_numbers = 6
    classes = ('normal','eccentric','broken_tooth','half_broken_tooth','surface_wearing','crack')
    class_correct = list(0. for i in range(class_numbers))
    class_total = list(0. for i in range(class_numbers))

    with torch.no_grad():  # 测试的时候不需要对梯度进行调整，所以梯度设置不调整
        for (inputs, labels) in test_loader:        
            inputs, labels = inputs.to(device), labels.to(device) # 将输入和目标在每一步都送入GPU

            size_tmp = inputs.shape
            inputs.resize_(size_tmp[0], 1, size_tmp[1])
            labels = labels.long()-1
            
            outputs = model(inputs)
            pred = outputs.argmax(dim=1)  # 返回每一行中最大值元素索引
            total += inputs.size(0)
            correct += torch.eq(pred,labels).sum().item()
        
            c = (pred == labels.to(device)).squeeze()
            for i in range(len(c)):

                label = labels[i]
                class_correct[label] += float(c[i])
                class_total[label] += 1
    print('Accuracy of the network on the %d/%d tests: %.2f %%' % ( correct,total,100.0 * correct / total))
    print (class_total)
    print()

    for i in range(class_numbers):
        print('Accuracy of %5s : %.2f %%' % (classes[i],100 * class_correct[i] / class_total[i]))
