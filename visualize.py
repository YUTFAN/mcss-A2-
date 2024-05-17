import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件
filename = 'muscle.csv'
data = pd.read_csv(filename, header=None, names=['Day', 'Muscle Mass', 'Average Anabolic Hormone', 'Average Catabolic Hormone'])

# 将肌肉质量除以 100
data['Muscle Mass'] = data['Muscle Mass'] / 100

# 绘制肌肉质量图表
plt.figure(figsize=(12, 6))
plt.plot(data['Day'], data['Muscle Mass'], label='Muscle Mass (divided by 100)')
plt.xlabel('Day')
plt.ylabel('Muscle Mass')
plt.title('Muscle Mass Over Time')
plt.legend()
plt.grid(True)
plt.savefig('muscle_mass.png')  # 保存图表为 PNG 文件
plt.show()

# 绘制平均激素值图表
plt.figure(figsize=(12, 6))
plt.plot(data['Day'], data['Average Anabolic Hormone'], label='Average Anabolic Hormone')
plt.plot(data['Day'], data['Average Catabolic Hormone'], label='Average Catabolic Hormone')
plt.xlabel('Day')
plt.ylabel('Hormone Level')
plt.title('Average Hormone Levels Over Time')
plt.legend()
plt.grid(True)
plt.savefig('hormone_levels.png')  # 保存图表为 PNG 文件
plt.show()
