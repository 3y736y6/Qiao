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
##引用 & = const*
+ int & ref = a; 
在编译器中转换为
+ int * const ref = &a;
  
|   int a,b;   |     指针     | 指针常量 = 引用 |      备注      |
| :----------: | :----------: | :-------------: | :------------: |
|    初始化    | int *p = &a; | int & ref = a;  | 引用必须赋初值 |
|  自身值改变  |   p = &b;    |  常量不可改变   |
| 指向内容改变 |   *p = b;    |    ref = b;     |


+ 不要返回局部变量的引用
  + 局部变量存放在四区中的 栈区，会被销毁，无法正常返回
+ static
  + 若变量在局部变量中定义，+static后，变量存放在全局区，不会被销毁，可以正常返回
+ 引用可以做函数返回值
  + 函数返回值为引用，则 函数调用 可以作为左值 swap3()=100; 相当于对return返回的 引用(别名)赋值
  
##const修饰
+ ==const== int &ref = ==a==; 
const修饰后，(ref = 20;)错误,该内存空间不可修改
+ const 实际修饰这块内存空间;
  + 防止在传引用时，在函数内部修改了 原变量的内容--void fck(const int &a)
+ 特别的：         
    + const int &a = 10; 合法 
      int &a = 10; 不合法      
  
##C++ 默认参数
+ 声明：int fck(int a,int b = 20,int c =30){}
  + 如果某个位置已经有了缺省参数，之后(右边)的也要有    
  + 函数声明和函数定义中不能有重复的默认参数，能在一个地方放置默认参数
+ 调用：
  + fck(5,6,7);
  + fck(5);
  + 有传入参数则用传入参数，没有则用缺省参数

##C++占位参数
+ 定义 
  + int fck(int a,==int==)  {}
  + int fck(int a,==int== =10 ) {}
+ 调用 fck(1,1);
  + 占位参数没有默认值,必须传入参数补齐位子
  
##函数重载
+ 同一个作用域下，函数名称相同
+ 函数==参数==**类型**不同，或**个数**不同，或**顺序**不同
+ 返回值不可作为重载条件
#####函数重载传引用
```c++
int &b = a;  int a =10;
void fck(int &x) {}; 
//传入b调用这个     
void fck(const int &x) {};
//传入整数调佣这个    
int &a = 10; 不合法   
const int &a = 10; 合法 
```
#####函数重载默认参数
```c++
void fck(int a,int b=10) {}
void fck(int a) {}
//允许存在，但调用时要避免冲突
fck(10);//可同时调用以上两条，冲突。error
fck(10,11);//只可调用第二条。OK
```
##类于对象
class Circle { 权限: 属性  行为 };
+ 成员(属性和行为):
  +   属性 -- 成员属性 -- 成员变量
  +   行为 -- 成员函数 -- 成员方法
  
|   权限    | 外部  | 内部  | 子类  |
| :-------: | :---: | :---: | :---: |
|  public   |   √   |   √   |   √   |
| protected |   ×   |   √   |   √   |
|  private  |   ×   |   √   |   ×   |

####struct 和 class 区别
class缺省权限是public
struct缺省权限是private

###构造函数与析构函数
+ 构造函数--用户初始化，有参，可重载
+ 析构函数--恢复出厂设置，无参，不可重载
  + 都会自动调用且只调用一次
  + 若个人不定义，编译器会自动生成一个空构造和析构和调用

####构造函数
+ 构造方式:
  + 默认构造:不定义，编译器默认构造一个空函数
  + 无参构造:自定义，不设置传入参数
  + 有参构造:自定义，设置传入参数
  + 拷贝构造:自定义，传入参数为 -- 同类的其他对象
    + Circle( const Circle &a) 
      {
        length = a.length ; 
      }
+ 调用方式:
  1. 定义对象时，自动调用
     + 默认调用/无参调用(不加括号)，系统自动调用构造与构析
       + Circle a; 
     + 传参调用，类似函数重载，匹配参数，自动调用对应构造与构析
       + Circle a(各种参(空void，参，对象参));
  2. 定义对象时，手动调用
     + Circle a;
       + 命名一个对象 + 调用默认构造 
     + Circle a = ==Circle ( different parameters )==;
       + 命名一个对象 + 根据重载调用特定构造 
     + 匿名对象 ==Circle ( different parameters )==;
       + 只构造不赋对象，上行中的 '=' 相当于取名，匿名对象构造完立刻构析
       + 匿名对象不可拷贝调用
  3. Circle a = ==different parameters== ;
     + 等于  Circle a = ==Circle ( different parameters )==; 

1. Circle a;
2. **Circle a ( ==different parameters== );**
3. Circle a = ==Circle ( different parameters )==;
4. Circle a = ==different parameters==;


