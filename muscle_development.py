import random
import math

#可以改变的参数(按照netlogo中的顺序)
#运动强度
INTENSITY = 90
#睡眠时间
SLEEP = 8
#运动间隔天数
INTERVAL = 2
#慢肌纤维比例
SLOW_FIBER = 50
#是否力量训练
LIFT = True
#总天数
DAYS = 2000
#压力
STRESS = 5

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

    
#补丁类，主要用于控制合成激素和分解激素的变化以及肌肉纤维的生成
class Patch:
    def __init__(self):
        self.anabolic_hormone = 50
        self.catabolic_hormone = 52
        self.fiber = MuscleFiber()

    #执行每日活动
    def perform_daily_activity(self):
        self.anabolic_hormone += 2.0 *math.log10(self.fiber.fiber_size)
        self.catabolic_hormone += 2.5 * math.log10(self.fiber.fiber_size)

    #举重
    def lift_weights(self, intensity):
        if random.random() < (intensity / 100) **2:
            self.anabolic_hormone += 44 * math.log10(self.fiber.fiber_size)
            self.catabolic_hormone += 55 * math.log10(self.fiber.fiber_size)

    #睡眠
    def sleep(self, hours):
        self.anabolic_hormone -= 0.48 * hours * math.log10(self.anabolic_hormone)
        self.catabolic_hormone -= 0.5 * hours * math.log10(self.catabolic_hormone)

    # #压力
    # def stress(self, stress_level):
    #     self.anabolic_hormone -= 0.5 * stress_level * math.log10(self.anabolic_hormone)
    #     self.catabolic_hormone += 0.5 * stress_level * math.log10(self.catabolic_hormone)

    #肌肉纤维的生长，受到合成激素和分解激素的影响
    def grow(self):
        self.fiber_size -= 0.20 * math.log10(self.catabolic_hormone)
        self.fiber_size += 0.20 * min(math.log10(self.anabolic_hormone), 1.05 * math.log10(self.catabolic_hormone))
    
    #生成新的肌肉纤维
    def new_muscle_fiber(self):
        max_size = 4 + sum(1 for _ in range(20) if random.random() > SLOW_FIBER / 100)
        fiber_size = (0.2 + random.random() * 0.4) * max_size
        self.fiber.max_size = max_size
        self.fiber.fiber_size = fiber_size
        self.fiber.regulate_muscle_fiber()
    
    class Muscle:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.patches = []
            for _ in range(height):
                row = []
                for _ in range(width):
                    row.append(Patch())
                self.patches.append(row)
            self.days = 0
    


