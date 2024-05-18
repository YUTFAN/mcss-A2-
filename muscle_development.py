import random
import math

#可以改变的参数(按照netlogo中的顺序和默认值)
#运动强度
INTENSITY = 88
#睡眠时间
SLEEP = 8
#运动间隔天数
INTERVAL = 3
#慢肌纤维比例
SLOW_FIBER = 40
#是否力量训练
LIFT = True
#总天数
DAYS = 3000
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
        self.anabolic_hormone += 2.5 *math.log10(self.fiber.fiber_size)
        self.catabolic_hormone += 2.0 * math.log10(self.fiber.fiber_size)

    #举重
    def lift_weights(self, intensity):
        if random.random() < (intensity / 100) **2:
            self.anabolic_hormone += 55 * math.log10(self.fiber.fiber_size)
            self.catabolic_hormone += 44 * math.log10(self.fiber.fiber_size)

    #睡眠
    def sleep(self, hours):
        self.anabolic_hormone -= 0.48 * hours * math.log10(self.anabolic_hormone)
        self.catabolic_hormone -= 0.5 * hours * math.log10(self.catabolic_hormone)

    #压力
    def stress(self, stress_level):
        self.anabolic_hormone -= 0.0 * stress_level * math.log10(self.anabolic_hormone)
        self.catabolic_hormone += 0.0 * stress_level * math.log10(self.catabolic_hormone)
    
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

    #计算肌肉的总质量
    def muscle_mass(self):
        mass = 0
        for i in range(self.width):
            for j in range(self.height):
                mass += self.patches[i][j].fiber.fiber_size
        return mass
    
    #计算合成激素的平均值
    def anabolic_hormone_mean(self):
        mean = 0
        for i in range(self.width):
            for j in range(self.height):
                mean += self.patches[i][j].anabolic_hormone
        return mean / (self.width * self.height)
    
    #计算分解激素的平均值
    def catabolic_hormone_mean(self):
        mean = 0
        for i in range(self.width):
            for j in range(self.height):
                mean += self.patches[i][j].catabolic_hormone
        return mean / (self.width * self.height)
    
    #初始化肌肉
    def set_up(self):
        for row in self.patches:
            for patch in row:
                patch.new_muscle_fiber()
        

    #每天的活动
    def go(self):
        for row in self.patches:
            for patch in row:
                patch.perform_daily_activity()
                if LIFT and self.days % INTERVAL == 0:
                    patch.lift_weights(INTENSITY)
                patch.sleep(SLEEP)
                
                patch.stress(STRESS)

        self.regulate_hormones()
        for row in self.patches:
            for patch in row:
                patch.fiber.develop_muscle(patch.anabolic_hormone, patch.catabolic_hormone)
        self.days += 1
    
    #将数据写入csv文件
    def csv(self, filename):
        muscle = [self.days, self.muscle_mass(), self.anabolic_hormone_mean(), self.catabolic_hormone_mean()]
        with open(filename, 'a') as csvfile:
            csvfile.write(','.join(map(str, muscle)) + '\n')

    #调节激素    
    def regulate_hormones(self):
        def clamp(value, minimum, maximum):
            return max(minimum, min(value, maximum))
        
        self.diffuse_hormones('anabolic_hormone', 0.75)
        self.diffuse_hormones('catabolic_hormone', 0.75)

        for row in self.patches:
            for patch in row:
                patch.anabolic_hormone = clamp(patch.anabolic_hormone, 50, 200)
                patch.catabolic_hormone = clamp(patch.catabolic_hormone, 52, 250)
    
    #扩散激素
    def diffuse_hormones(self, hormone, rate):
        total_neighbors = 8
        new_values = [[0] * self.width for _ in range(self.height)]

        #计算扩散的值
        def calculate_distributed_value(value):
            return value * rate / total_neighbors
        
        #累积扩散的值
        def accumulate_distributed_value(x, y, value):
            neighbors = self.get_neighbors(x, y)
            distributed_value = calculate_distributed_value(value)
            for nx, ny in neighbors:
                new_values[ny][nx] += distributed_value
            return len(neighbors)
        
        #累积剩余的值
        def accumulate_remaining_value(x, y, current_value, num_neighbors):
            remaining_value = current_value * (1 - rate)
            if num_neighbors < total_neighbors:
                remaining_value += calculate_distributed_value(current_value) * (total_neighbors - num_neighbors)
            new_values[y][x] += remaining_value
        
        #遍历所有的补丁,计算新的激素值
        for y in range(self.height):
            for x in range(self.width):
                current_value = getattr(self.patches[y][x], hormone)
                num_neighbors = accumulate_distributed_value(x, y, current_value)
                accumulate_remaining_value(x, y, current_value, num_neighbors)

        #将新的激素值赋值给补丁
        for y in range(self.height):
            for x in range(self.width):
                setattr(self.patches[y][x], hormone, new_values[y][x])
    
    #获取邻居
    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        return neighbors


    
if __name__ == '__main__':
    world = Muscle(17, 17)
    world.set_up()
    for i in range(DAYS):
        world.go()
        world.csv('muscle.csv')

        
    




