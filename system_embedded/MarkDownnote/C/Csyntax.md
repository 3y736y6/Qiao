---
export_on_save:
  html: true
html:
  embed_local_images: false
  embed_svg: true
  offline: false
  toc: true

print_background: false
---


###返回一个二维数组
```c
//c++中函数不能直接返回一个二维数组
//当需要函数的返回值为一个二维数组，可采用typedef
//第二层为[3]，因为arr第一层中的每一个房间中放了3个房间
typedef int(*R)[3];//定义一个二层指针，第一层是变量(可以指向第一层中的任意房间)，每个房间中放的(嵌套的)房间数为3
R transpose(int arr[][3])       //不能写成int ** transpose(int **a ,int...)
{
	static int arr[3][3] = { { 1, 2, 3 },{ 4, 5, 6 },{ 7, 8, 9 } };
	return arr;
}
//注意static，arr局部变量，当此函数执行完后，返回的是数组首地址，但数组内容被释放。需要添加static保证返回的地址有效
//或者把arr定义在外部
```