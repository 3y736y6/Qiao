from datetime import datetime  
  
# 获取当前日期和时间  
current_datetime = datetime.now()  
  
# 打印当前日期和时间  
print("当前日期和时间:", current_datetime)

# 格式化日期和时间  
formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") 
