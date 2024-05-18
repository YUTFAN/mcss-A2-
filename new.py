import random
import math

# Parameters
INTENSITY = 88
SLEEP = 8
INTERVAL = 3
SLOW_FIBER = 40
LIFT = True
DAYS = 3000
STRESS = 5

class MuscleFiber:
    def __init__(self):
        self.fiber_size = 0
        self.max_size = 0

    def regulate_muscle_fiber(self):
        if self.fiber_size > self.max_size:
            self.fiber_size = self.max_size
        if self.fiber_size < 1:
            self.fiber_size = 1

    def grow(self, anabolic_hormone, catabolic_hormone):
        self.fiber_size -= 0.20 * math.log10(catabolic_hormone)
        self.fiber_size += 0.20 * min(math.log10(anabolic_hormone), 1.05 * math.log10(catabolic_hormone))

    def develop_muscle(self, anabolic_hormone, catabolic_hormone):
        self.grow(anabolic_hormone, catabolic_hormone)
        self.regulate_muscle_fiber()

class Patch:
    def __init__(self, muscle, x, y):
        self.anabolic_hormone = 50
        self.catabolic_hormone = 52
        self.fiber = MuscleFiber()
        self.muscle = muscle
        self.x = x
        self.y = y

    def perform_daily_activity(self):
        self.anabolic_hormone += 2.5 * math.log10(self.fiber.fiber_size)
        self.catabolic_hormone += 2.0 * math.log10(self.fiber.fiber_size)

    def lift_weights(self, intensity):
        if random.random() < (intensity / 100) ** 2:
            self.anabolic_hormone += 55 * math.log10(self.fiber.fiber_size)
            self.catabolic_hormone += 44 * math.log10(self.fiber.fiber_size)

    def sleep(self, hours):
        self.anabolic_hormone -= 0.48 * hours * math.log10(self.anabolic_hormone)
        self.catabolic_hormone -= 0.5 * hours * math.log10(self.catabolic_hormone)

    def stress(self, stress_level):
        self.anabolic_hormone -= 0.0 * stress_level * math.log10(self.anabolic_hormone)
        self.catabolic_hormone += 0.0 * stress_level * math.log10(self.catabolic_hormone)

    def new_muscle_fiber(self):
        max_size = 4 + sum(1 for _ in range(20) if random.random() > SLOW_FIBER / 100)
        fiber_size = (0.2 + random.random() * 0.4) * max_size
        self.fiber.max_size = max_size
        self.fiber.fiber_size = fiber_size
        self.fiber.regulate_muscle_fiber()

    def regulate_hormones(self):
        def clamp(value, minimum, maximum):
            return max(minimum, min(value, maximum))
        
        self.anabolic_hormone = clamp(self.anabolic_hormone, 50, 200)
        self.catabolic_hormone = clamp(self.catabolic_hormone, 52, 250)

    def diffuse_hormones(self, hormone, rate):
        neighbors = self.get_neighbors()
        total_neighbors = 8
        num_neighbors = len(neighbors)
        current_value = getattr(self, hormone)

        distributed_value = current_value * rate / total_neighbors
        remaining_value = current_value * (1 - rate) + distributed_value * (total_neighbors - num_neighbors)

        for neighbor in neighbors:
            neighbor_hormone_value = getattr(neighbor, hormone)
            setattr(neighbor, hormone, neighbor_hormone_value + distributed_value)
        
        setattr(self, hormone, remaining_value)

    def get_neighbors(self):
        offsets = [-1, 0, 1]
        neighbors = []
        for dx in offsets:
            for dy in offsets:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < self.muscle.width and 0 <= ny < self.muscle.height:
                    neighbors.append(self.muscle.patches[ny][nx])
        return neighbors

class Muscle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.patches = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Patch(self, x, y))
            self.patches.append(row)
        self.days = 0

    def muscle_mass(self):
        mass = 0
        for row in self.patches:
            for patch in row:
                mass += patch.fiber.fiber_size
        return mass

    def anabolic_hormone_mean(self):
        mean = 0
        for row in self.patches:
            for patch in row:
                mean += patch.anabolic_hormone
        return mean / (self.width * self.height)

    def catabolic_hormone_mean(self):
        mean = 0
        for row in self.patches:
            for patch in row:
                mean += patch.catabolic_hormone
        return mean / (self.width * self.height)

    def set_up(self):
        for row in self.patches:
            for patch in row:
                patch.regulate_hormones()
                patch.new_muscle_fiber()

    def go(self):
        for row in self.patches:
            for patch in row:
                patch.perform_daily_activity()
                if LIFT and self.days % INTERVAL == 0:
                    patch.lift_weights(INTENSITY)
                patch.sleep(SLEEP)
                patch.stress(STRESS)

        for row in self.patches:
            for patch in row:
                patch.diffuse_hormones('anabolic_hormone', 0.75)
                patch.diffuse_hormones('catabolic_hormone', 0.75)

        for row in self.patches:
            for patch in row:
                patch.regulate_hormones()
                
        for row in self.patches:
            for patch in row:
                patch.fiber.develop_muscle(patch.anabolic_hormone, patch.catabolic_hormone)
        self.days += 1

    def csv(self, filename):
        muscle = [self.days, self.muscle_mass(), self.anabolic_hormone_mean(), self.catabolic_hormone_mean()]
        with open(filename, 'a') as csvfile:
            csvfile.write(','.join(map(str, muscle)) + '\n')

if __name__ == '__main__':
    world = Muscle(17, 17)
    world.set_up()
    for i in range(DAYS):
        print(f"\r{world.days}/{DAYS}", end="")
        world.go()
        world.csv('muscle.csv')
