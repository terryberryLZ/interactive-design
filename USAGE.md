# 使用指南 (Usage Guide)

## 快速开始 (Quick Start)

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
4. 程序窗口将打开，显示一个 320x320 的画布

### 4. 生成头像 (Generate Avatars)

- **点击鼠标**: 在窗口内任意位置点击鼠标，即可生成新的随机头像
- **无限生成**: 可以点击任意多次，每次都会生成不同的组合
- **关闭程序**: 点击窗口的关闭按钮或按 ESC 键

## 程序说明 (Program Description)

### 头像生成规则 (Avatar Generation Rules)

程序会随机选择以下元素组合成独特的头像：

1. **种族特征** (Race Features)
   - 兽人: 宽大的方形头部，带有獠牙
   - 精灵: 优雅的椭圆形头部，尖耳朵
   - 矮人: 结实的圆形头部，带有胡须
   - 地精: 小巧的尖头，大耳朵

2. **皮肤颜色** (Skin Colors)
   - 绿色系 (适合兽人/地精)
   - 浅色系 (适合精灵)
   - 棕褐色系 (适合矮人)
   - 其他奇幻色彩

3. **面部表情** (Facial Expressions)
   - 微笑: 弯曲的笑容
   - 生气: 皱眉和生气的眉毛
   - 滑稽: 吐舌头，一只眼睛眨眼
   - 呆萌: 圆嘴巴和腮红

4. **装饰品** (Accessories)
   - 头饰: 角盔、花冠、巫师帽、触手帽
   - 项链: 骷髅吊坠、宝石项圈、叶子项链
   - 耳环: 圆环、羽毛、骨头

5. **服装** (Clothing)
   - 长袍、盔甲、束腰外衣、斗篷

### 像素艺术风格 (Pixel Art Style)

- 使用 8x8 像素的方块构建图像
- 纯色填充，无渐变效果
- 复古游戏风格的视觉效果

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
