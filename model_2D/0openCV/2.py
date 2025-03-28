import gpiod
import time

#控制小车移动代码
# enable GPIO controller
chip1 = gpiod.Chip('1',gpiod.Chip.OPEN_BY_NUMBER)  
chip6 = gpiod.Chip("6", gpiod.Chip.OPEN_BY_NUMBER)
chip7 = gpiod.Chip("7", gpiod.Chip.OPEN_BY_NUMBER)

# Get GPIO line and make it ouput mode
# left forward
left_F1 = chip1.get_line(2*8+0)  
left_F1.request(consumer="left_F1", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
left_F2 = chip1.get_line(2*8+1)  
left_F2.request(consumer="left_F2", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
# left behind
left_B1 = chip6.get_line(0*8+2)  
left_B1.request(consumer="left_B1", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
left_B2 = chip6.get_line(0*8+3)  
left_B2.request(consumer="left_B2", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
# right forward
right_F1 = chip6.get_line(0*8+5)  
right_F1.request(consumer="right_F1", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
right_F2 = chip6.get_line(0*8+6)  
right_F2.request(consumer="right_F2", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
# right behind
right_B1 = chip6.get_line(0*8+7)  
right_B1.request(consumer="right_B1", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
right_B2 = chip7.get_line(0*8+2)  
right_B2.request(consumer="right_B2", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])


def left_FF():
    left_F1.set_value(1)
    left_F2.set_value(0)
def left_FB():
    left_F1.set_value(0)
    left_F2.set_value(1)
def left_Fstop():
    left_F1.set_value(1)
    left_F2.set_value(1)


def left_BF():
    left_B1.set_value(1)
    left_B2.set_value(0)
def left_BB():
    left_B1.set_value(0)
    left_B2.set_value(1)
def left_Bstop():
    left_B1.set_value(1)
    left_B2.set_value(1)


def right_FF():
    right_F1.set_value(1)
    right_F2.set_value(0)
def right_FB():
    right_F1.set_value(0)
    right_F2.set_value(1)
def right_Fstop():
    right_F1.set_value(1)
    right_F2.set_value(1)


def right_BF():
    right_B1.set_value(1)
    right_B2.set_value(0)

def right_BB():
    right_B1.set_value(0)
    right_B2.set_value(1)
def right_Bstop():
    right_B1.set_value(1)
    right_B2.set_value(1)
# def button():
#     # str = left1.consumer()

#     # button = chip4.get_line(23)
#     # button.request(consumer="BUTTON", type=gpiod.LINE_REQ_DIR_IN)
#     # state = button.get_value()
#     return "over"


# for i in range(0,10):
#     # 设置 GPIO 为高电平
#     left_F1.set_value(1)
#     time.sleep(2)

#     # 设置 GPIO 为低电平
#     left_F1.set_value(0)
#     time.sleep(2)


def Forward(seconds1):
    left_FF()
    left_BF()
    right_FF()
    right_BF()
    time.sleep(seconds1)
    left_Fstop()
    left_Bstop()
    right_Bstop()
    right_Fstop()
        

def Back(seconds1):
    left_FB()
    left_BB()
    right_FB()
    right_BB()
    time.sleep(seconds1)
    left_Fstop()
    left_Bstop()
    right_Bstop()
    right_Fstop()

def Left(seconds1):
    left_FB()
    left_BB()
    right_FF()
    right_BF()
    time.sleep(seconds1)
    left_Fstop()
    left_Bstop()
    right_Bstop()
    right_Fstop()

def Right(seconds1):
    left_FF()
    left_BF()
    right_FB()
    right_BB()
    time.sleep(seconds1)
    left_Fstop()
    left_Bstop()
    right_Bstop()
    right_Fstop()
        

for i in range(0,20):
    Forward(5)
    Back(5)
    Left(5)
    Right(5)


left_F1.release()
left_F2.release()
left_B1.release()
left_B2.release()
right_F1.release()
right_F1.release()
right_B1.release()
right_B2.release()

