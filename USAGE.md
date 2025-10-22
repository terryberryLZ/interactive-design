# 使用指南 (Usage Guide)

## 快速开始 (Quick Start)

本项目提供两个版本，可根据需要选择：

## Version 1: Processing Python Mode

### 1. 安装 Processing (Install Processing)

访问 [Processing 官网](https://processing.org/download) 下载并安装适合您操作系统的版本。

### 2. 安装 Python Mode (Install Python Mode)

1. 启动 Processing
2. 点击右上角的模式选择器 (默认显示 "Java")
3. 在下拉菜单中选择 "Add Mode..."
4. 在列表中找到 "Python Mode for Processing 3"
5. 点击 "Install" 安装
6. 安装完成后，再次点击模式选择器，选择 "Python"

### 3. 运行程序 (Run the Program)

1. 在 Processing 中，选择 File -> Open
2. 浏览到 `fantasy_avatar_generator.pyde` 文件并打开
3. 点击运行按钮 (播放图标) 或按快捷键:
   - Windows/Linux: Ctrl + R
   - macOS: Cmd + R
4. 程序窗口将打开，显示一个 512x512 的画布

### 4. 生成头像 (Generate Avatars)

- **点击鼠标**: 在窗口内任意位置点击鼠标，即可生成新的随机头像
- **按R键**: 按R键也可以生成新头像
- **无限生成**: 可以点击任意多次，每次都会生成不同的组合
- **关闭程序**: 点击窗口的关闭按钮或按 ESC 键

## Version 2: Pygame Standalone

### 1. 安装 Python 和 Pygame

确保已安装 Python 3.8 或更高版本，然后安装 pygame:

```bash
pip install pygame
```

或使用 requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. 运行程序

**基本运行**:
```bash
python fantasy_avatar_generator.py
```

**使用种子值（可复现生成）**:
```bash
python fantasy_avatar_generator.py --seed 12345
```

使用相同的种子值会生成相同的头像序列，适合：
- 展示特定的头像组合
- 调试和测试
- 创建可复现的演示

### 3. 交互控制

- **鼠标点击**: 生成新头像
- **R键**: 生成新头像
- **S键**: 保存当前头像为PNG文件（保存在当前目录）
- **ESC键**: 退出程序

### 4. 查看帮助

```bash
python fantasy_avatar_generator.py --help
```

## Version 3: Windows .exe (无需安装Python)

### 构建可执行文件

参见 [BUILD_EXE.md](BUILD_EXE.md) 获取详细的构建说明。

简要步骤：
1. 安装 PyInstaller: `pip install pyinstaller`
2. 运行构建命令: `pyinstaller fantasy_avatar_generator.spec`
3. 在 `dist/` 文件夹中找到 `FantasyAvatarGenerator.exe`

### 运行可执行文件

双击 `FantasyAvatarGenerator.exe` 即可运行。

或在命令行中使用种子值:
```bash
FantasyAvatarGenerator.exe --seed 12345
```

## 程序说明 (Program Description)

### 头像生成规则 (Avatar Generation Rules)

程序会随机选择以下元素组合成独特的头像：

1. **种族特征** (Race Features)
   - 人类: 平衡圆润的头部，正常耳朵
   - 兽人: 宽大的方形头部，带有獠牙
   - 精灵: 优雅的椭圆形头部，尖耳朵
   - 矮人: 结实的圆形头部，带有胡须
   - 地精: 小巧的尖头，大耳朵

2. **皮肤颜色** (Skin Colors)
   - 绿色系 (适合兽人/地精)
   - 浅色系 (适合精灵/人类)
   - 棕褐色、桃色、淡黄色系 (适合人类)
   - 其他奇幻色彩 (淡蓝、淡绿等)

3. **面部表情** (Facial Expressions)
   - 英俊: 自信的笑容配挑眉
   - 严肃: 直线嘴巴配皱眉
   - 可爱: 圆嘴巴和腮红
   - 搞怪: 吐舌头配眨眼和挑眉

4. **装饰品** (Accessories)
   - 头饰: 角盔、花冠、巫师帽、触手帽、头巾
   - 项链: 骷髅吊坠、宝石项圈、叶子项链、符文吊坠
   - 耳环: 圆环、羽毛、骨头、耳钉

5. **服装** (Clothing)
   - 长袍、盔甲、束腰外衣、斗篷、连帽衫

6. **背景** (Backgrounds)
   - 纯色: 紫色、蓝色、粉色
   - 渐变: 日落渐变、海洋渐变
   - 图案: 星星图案、圆点图案

### 像素艺术风格 (Pixel Art Style)

- 使用 4x4 像素的方块构建图像
- 主要使用纯色填充，背景支持渐变效果
- 复古游戏风格的视觉效果
- 输出分辨率: 512x512 像素 (从 128x128 逻辑画布放大)

## 故障排除 (Troubleshooting)

### 问题: 程序无法运行

**解决方案**:
1. 确认已安装 Processing 3 或更高版本
2. 确认已正确安装 Python Mode
3. 确认当前模式已切换到 "Python" 而非 "Java"

### 问题: 窗口显示不正常

**解决方案**:
1. 检查屏幕分辨率是否支持 320x320 窗口
2. 尝试重启 Processing

### 问题: 点击鼠标没有反应

**解决方案**:
1. 确保点击在程序窗口内
2. 检查程序是否正在运行 (未暂停)
3. 尝试重新运行程序

## 进阶使用 (Advanced Usage)

### 修改像素大小 (Modify Pixel Size)

在代码中找到 `PIXEL = 8` 这一行，可以修改像素块大小:
- 较小的值 (如 4) 会产生更精细的图像
- 较大的值 (如 16) 会产生更粗糙的像素感

### 修改画布大小 (Modify Canvas Size)

在 `setup()` 函数中找到 `size(320, 320)`，可以修改画布尺寸:
```python
def setup():
    size(640, 640)  # 更大的画布
    noStroke()
    generateAvatar()
```

注意: 修改画布大小后，可能需要调整绘图坐标以保持头像居中。

### 添加新元素 (Add New Elements)

1. 在对应的列表中添加新选项 (如 `HEADWEAR`)
2. 在对应的绘制函数中添加新的绘制逻辑 (如 `drawHeadwear()`)
3. 使用像素块 (`rect()`) 绘制新元素

例如添加新头饰:
```python
HEADWEAR = ["horn_helmet", "flower_crown", "wizard_hat", "tentacle_hat", "crown", "none"]

def drawHeadwear(headwear_type, race):
    # ... 现有代码 ...
    
    elif headwear_type == "crown":
        # 绘制皇冠
        fill(255, 215, 0)  # 金色
        for i in range(7, 13):
            rect(x_center - 80 + i * PIXEL, y_center - 32, PIXEL, PIXEL)
```

## 学习资源 (Learning Resources)

- [Processing 官方网站](https://processing.org/)
- [Processing Python Mode 教程](https://py.processing.org/tutorials/)
- [像素艺术教程](https://opengameart.org/content/pixel-art-tutorial)

## 分享作品 (Share Your Work)

如果您创建了有趣的头像或添加了新功能，欢迎分享！
