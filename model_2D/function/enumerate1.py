
# enumerate(iterable, start=0)
# iterable：必需参数，表示一个可迭代对象，如列表、元组、字符串等。
# start：可选参数，表示起始的索引值，默认为0。

fruits = ['apple', 'banana', 'orange']  
for index, fruit in enumerate(fruits,start=0):  
    print(f"Index: {index}, Value: {fruit}")
# output:
# Index: 0, Value: apple  
# Index: 1, Value: banana  
# Index: 2, Value: orange

fruits = ['apple', 'banana', 'orange']  
for index, fruit in enumerate(fruits, start=1):  
    print(f"Index: {index}, Value: {fruit}")
# output:
# Index: 1, Value: apple  
# Index: 2, Value: banana  
# Index: 3, Value: orange