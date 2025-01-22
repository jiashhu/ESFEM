import os
import imageio
from PIL import Image

# 定义图像文件夹和输出 GIF 文件名
image_folder = '/Users/liubocheng/Documents/craft/JilinUniveristy/surfaceEvolution/'
output_gif = os.path.join(image_folder, 'output.gif')

# 获取所有 PNG 文件的文件名，并按顺序排序
filenames = sorted((fn for fn in os.listdir(image_folder) if fn.endswith('.png')))

# 定义是否使用白色背景
use_white_background = True  # 如果希望使用透明背景，将其设置为 False

# 读取图像并生成 GIF
images = []
for filename in filenames:
    filepath = os.path.join(image_folder, filename)
    image = Image.open(filepath).convert('RGBA')  # 将图像转换为 RGBA 模式
    # 先缩小尺寸然后再粘贴到白色背景上
    image = image.resize((image.width // 7, image.height // 5))
    
    if use_white_background:
        # 创建一个白色背景的图像
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
        # 将原图像粘贴到白色背景上，使用 alpha 通道作为掩码
        background.paste(image, (0, 0), image)
        image = background
    
    # 将颜色数量减少到 64
    image = image.convert('P', palette=Image.ADAPTIVE, colors=64)
    images.append(image)

# 保存为 GIF 动画
images[0].save(output_gif, save_all=True, append_images=images[1:], duration=200, loop=0)

# 使用 gifsicle 优化 GIF 文件
os.system(f'gifsicle -O3 --colors 64 {output_gif} -o {output_gif}')

print(f"GIF 动画已保存到: {output_gif}")