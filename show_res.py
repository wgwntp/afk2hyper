import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# 设置图片目录和缩放比例
image_folder = './history/laoshi'  # 替换为你的图片文件夹路径
scale_factor = 1.0 / 20

# 读取图片并调整大小
images = []
for filename in os.listdir(image_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # 根据你的图片格式调整
        img_path = os.path.join(image_folder, filename)
        img = Image.open(img_path)
        img_resized = img.resize((int(img.width * scale_factor), int(img.height * scale_factor)), Image.Resampling.NEAREST)
        images.append(img_resized)

# 计算网格大小（这里假设是10x10的网格，你可以根据需要调整）
grid_size = int(np.sqrt(100))  # 对于100张图片，grid_size将是10

# 创建图形和轴
fig, axes = plt.subplots(grid_size, grid_size , figsize=(grid_size, grid_size*2))  # 调整figsize以适应图片大小
axes = axes.ravel()  # 将二维数组转换为一维数组，方便遍历

# 显示图片
for i, img in enumerate(images):
    ax = axes[i]
    ax.imshow(img)
    ax.axis('off')  # 关闭坐标轴

# 如果图片数量不是网格大小的完美平方，则隐藏多余的轴
for i in range(len(images), grid_size * grid_size):
    axes[i].axis('off')
    axes[i].set_visible(False)

# 调整布局以防止重叠
plt.tight_layout()
plt.show()