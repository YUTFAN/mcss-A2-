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



