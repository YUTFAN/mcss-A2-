import csv
import random
import math

#固定的参数

#合成激素的最大值和最小值
ANABOLIC_HORMONE_MAX = 200
ANABOLIC_HORMONE_MIN = 50

#分解激素的最大值和最小值
CATABOLIC_HORMONE_MAX = 250
CATABOLIC_HORMONE_MIN = 52

#激素扩散率
HORMONE_DIFFUSE_RATE = 0.75

#可以改变的参数(按照netlogo中的顺序和默认值)
#运动强度
INTENSITY = 95
#睡眠时间
SLEEP = 8
#运动间隔天数
INTERVAL = 5
#慢肌纤维比例
SLOW_FIBER = 50
#是否力量训练
LIFT = True
#总天数
DAYS = 100

#肌肉纤维初始化，控制肌肉的大小和生成
class MuscleFiber:
    def __init__(self):
        self.fiber_size = 0
        self.max_size = 0

    #控制肌肉纤维的大小在一定范围内
    #如果肌肉纤维的大小大于最大值，则将肌肉纤维的大小设置为最大值
    #如果肌肉纤维的大小小于1，则将肌肉纤维的大小设置为1
    def regulate_muscle_fiber(self):
        if self.fiber_size > self.max_size:
            self.fiber_size = self.max_size
        if self.fiber_size < 1:
            self.fiber_size = 1

    #肌肉纤维的生长，受到合成激素和分解激素的影响
    def grow(self, anabolic_hormone, catabolic_hormone):
        self.fiber_size -= 0.20 * math.log10(catabolic_hormone)
        self.fiber_size += 0.20 * min(math.log10(anabolic_hormone), 1.05 * math.log10(catabolic_hormone))
    
    #肌肉纤维的生长和控制
    def develop_muscle(self, anabolic_hormone, catabolic_hormone):
        self.grow(anabolic_hormone, catabolic_hormone)
        self.regulate_muscle_fiber()

    

