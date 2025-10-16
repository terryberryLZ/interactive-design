# 开发与扩展指南 (Development & Extension Guide)

## 代码架构 (Code Architecture)

### 文件结构 (File Structure)

```
interactive-design/
├── fantasy_avatar_generator.pyde  # 主程序文件
├── README.md                      # 项目说明
├── USAGE.md                       # 使用指南
├── EXAMPLES.md                    # 示例说明
├── DEMO_GUIDE.md                  # 演示指南
├── DEVELOPMENT.md                 # 本文件
└── test_structure.py              # 结构测试脚本
```

### 代码组织 (Code Organization)

```python
# 1. 全局变量和配置
current_avatar = {}      # 当前头像配置
PIXEL = 8               # 像素块大小
[各种选项列表]

# 2. Processing 核心函数
setup()                 # 初始化
draw()                  # 绘制循环
mousePressed()          # 鼠标事件

# 3. 头像生成逻辑
generateAvatar()        # 主生成函数
random_choice()         # 随机选择辅助函数

# 4. 绘制模块 (按类别分组)
# 头部相关
drawHead()              # 绘制头部和种族特征
drawExpression()        # 绘制表情

# 配饰相关
drawHeadwear()          # 绘制头饰
drawNecklace()          # 绘制项链
drawEarrings()          # 绘制耳环

# 服装相关
drawClothes()           # 绘制服装
```

## 添加新元素 (Adding New Elements)

### 步骤 1: 添加新选项到列表

例如添加新种族 "龙人" (Dragonborn):

```python
# 在文件顶部的列表中添加
RACES = ["orc", "elf", "dwarf", "goblin", "dragonborn"]
```

### 步骤 2: 在绘制函数中添加逻辑

在 `drawHead()` 函数中添加新的绘制逻辑:

```python
def drawHead(race, skin_col):
    """Draw the head/face based on race"""
    fill(skin_col)
    
    x_center = 160
    y_center = 140
    
    # ... 现有代码 ...
    
    elif race == "dragonborn":
        # 龙人头部 - 更宽更方
        for i in range(6, 14):
            for j in range(4, 13):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        
        # 龙角
        fill(200, 200, 220)
        rect(x_center - 56, y_center - 24, PIXEL * 2, PIXEL * 4)
        rect(x_center + 48, y_center - 24, PIXEL * 2, PIXEL * 4)
        
        # 龙鳞纹理 (可选)
        fill(skin_col)
        # 添加鳞片细节...
```

### 步骤 3: 添加配套颜色 (可选)

如果新种族需要特定颜色:

```python
SKIN_COLORS = [
    # ... 现有颜色 ...
    color(255, 100, 100),  # 红龙人
    color(100, 100, 255),  # 蓝龙人
]
```

## 添加新头饰示例 (Adding New Headwear Example)

### 完整示例: 添加"皇冠" (Crown)

```python
# 1. 添加到选项列表
HEADWEAR = ["horn_helmet", "flower_crown", "wizard_hat", "tentacle_hat", "crown", "none"]

# 2. 在 drawHeadwear() 中添加绘制逻辑
def drawHeadwear(headwear_type, race):
    """Draw headwear"""
    x_center = 160
    y_center = 140
    
    # ... 现有代码 ...
    
    elif headwear_type == "crown":
        # 金色皇冠
        fill(255, 215, 0)
        
        # 皇冠底座
        for i in range(7, 13):
            rect(x_center - 80 + i * PIXEL, y_center - 24, PIXEL, PIXEL)
        
        # 皇冠尖顶 (5个尖)
        for i in [7, 9, 10, 11, 12]:
            rect(x_center - 80 + i * PIXEL, y_center - 32, PIXEL, PIXEL)
            if i in [8, 10, 12]:
                # 更高的尖顶
                rect(x_center - 80 + i * PIXEL, y_center - 40, PIXEL, PIXEL)
        
        # 宝石装饰
        fill(255, 50, 50)
        rect(x_center - 8, y_center - 32, PIXEL, PIXEL)
```

## 添加新表情示例 (Adding New Expression Example)

### 完整示例: 添加"惊讶" (Surprised)

```python
# 1. 添加到选项列表
EXPRESSIONS = ["smile", "angry", "silly", "cute", "surprised"]

# 2. 在 drawExpression() 中添加绘制逻辑
def drawExpression(expression):
    """Draw facial expression"""
    x_center = 160
    y_center = 140
    
    # ... 现有代码 ...
    
    elif expression == "surprised":
        # 大大的圆眼睛
        fill(255)
        rect(x_center - 40, y_center + 4, PIXEL * 4, PIXEL * 4)
        rect(x_center + 16, y_center + 4, PIXEL * 4, PIXEL * 4)
        fill(0)
        rect(x_center - 28, y_center + 12, PIXEL * 2, PIXEL * 2)
        rect(x_center + 24, y_center + 12, PIXEL * 2, PIXEL * 2)
        
        # 圆形的"O"型嘴
        fill(255, 150, 150)
        rect(x_center - 12, y_center + 28, PIXEL * 3, PIXEL * 3)
```

## 高级技巧 (Advanced Techniques)

### 1. 根据种族调整元素

有些元素可能需要根据种族调整位置或样式:

```python
def drawHeadwear(headwear_type, race):
    """Draw headwear"""
    x_center = 160
    y_center = 140
    
    # 根据种族调整Y位置
    if race == "dwarf":
        y_offset = 8  # 矮人头顶位置较低
    elif race == "elf":
        y_offset = -4  # 精灵头顶位置较高
    else:
        y_offset = 0
    
    if headwear_type == "crown":
        # 使用 y_offset 调整位置
        for i in range(7, 13):
            rect(x_center - 80 + i * PIXEL, y_center - 24 + y_offset, PIXEL, PIXEL)
```

### 2. 添加颜色变化

让某些元素有颜色变化:

```python
# 在全局变量中添加颜色选项
ROBE_COLORS = [
    color(80, 60, 140),   # 紫色
    color(140, 60, 60),   # 红色
    color(60, 80, 140),   # 蓝色
    color(60, 140, 80),   # 绿色
]

# 在 generateAvatar() 中选择
current_avatar = {
    # ... 其他属性 ...
    "robe_color": random_choice(ROBE_COLORS) if current_avatar["clothes"] == "robe" else None
}

# 在 drawClothes() 中使用
def drawClothes(clothes_type, skin_col):
    if clothes_type == "robe":
        # 使用自定义颜色或默认颜色
        robe_col = current_avatar.get("robe_color", color(80, 60, 140))
        fill(robe_col)
        # ... 绘制代码 ...
```

### 3. 添加动画效果

虽然当前是静态图像，但可以添加简单动画:

```python
# 全局变量
animation_frame = 0

def draw():
    global animation_frame
    animation_frame += 1
    
    # 每30帧更新一次某个元素
    if animation_frame % 30 == 0:
        # 可以添加眨眼、摆动等效果
        pass

def drawHead(race, skin_col):
    # 根据 animation_frame 调整眼睛
    if animation_frame % 60 < 5:  # 每60帧眨眼一次
        # 绘制闭眼
        fill(skin_col)
        rect(x_center - 32, y_center + 8, PIXEL * 3, PIXEL)
        rect(x_center + 16, y_center + 8, PIXEL * 3, PIXEL)
    else:
        # 正常眼睛
        # ... 原有代码 ...
```

## 优化建议 (Optimization Tips)

### 1. 减少重复代码

使用辅助函数:

```python
def drawPixelRect(x, y, w, h, col):
    """绘制像素矩形区域"""
    fill(col)
    for i in range(w):
        for j in range(h):
            rect(x + i * PIXEL, y + j * PIXEL, PIXEL, PIXEL)

# 使用
drawPixelRect(x_center - 80, y_center - 40, 8, 10, skin_col)
```

### 2. 参数化常量

将硬编码的位置提取为常量:

```python
# 全局常量
HEAD_X = 160
HEAD_Y = 140
HEAD_WIDTH = 8
HEAD_HEIGHT = 10

def drawHead(race, skin_col):
    drawPixelRect(HEAD_X - 80, HEAD_Y - 40, HEAD_WIDTH, HEAD_HEIGHT, skin_col)
```

### 3. 模块化颜色方案

创建颜色主题:

```python
COLOR_THEMES = {
    "classic": {
        "background": color(240, 240, 250),
        "gold": color(255, 215, 0),
        "silver": color(150, 150, 150),
    },
    "dark": {
        "background": color(40, 40, 50),
        "gold": color(200, 180, 0),
        "silver": color(120, 120, 140),
    }
}

current_theme = "classic"

def setup():
    size(320, 320)
    noStroke()
    generateAvatar()
    
def generateAvatar():
    background(COLOR_THEMES[current_theme]["background"])
    # ...
```

## 测试你的更改 (Testing Your Changes)

### 1. 语法检查

```bash
python3 -m py_compile fantasy_avatar_generator.pyde
```

### 2. 结构验证

```bash
python3 test_structure.py
```

### 3. 手动测试

在 Processing 中运行程序并:
- 点击多次确保随机生成正常
- 检查所有新元素是否正确显示
- 确认没有视觉重叠或遮挡问题
- 测试不同种族与新元素的组合

## 调试技巧 (Debugging Tips)

### 1. 添加调试输出

```python
def generateAvatar():
    global current_avatar
    
    # ... 生成代码 ...
    
    # 打印当前配置
    print("Generated avatar:")
    for key, value in current_avatar.items():
        print(f"  {key}: {value}")
```

### 2. 可视化网格

在开发时显示像素网格:

```python
def drawGrid():
    """绘制辅助网格"""
    stroke(200)
    strokeWeight(1)
    for i in range(0, width, PIXEL):
        line(i, 0, i, height)
    for j in range(0, height, PIXEL):
        line(0, j, width, j)
    noStroke()

def setup():
    size(320, 320)
    noStroke()
    generateAvatar()
    drawGrid()  # 调试时使用
```

### 3. 单独测试元素

注释掉其他绘制调用，只测试新元素:

```python
def generateAvatar():
    # ... 生成代码 ...
    
    background(240, 240, 250)
    
    # 只绘制要测试的元素
    # drawClothes(current_avatar["clothes"], current_avatar["skin_color"])
    # drawHead(current_avatar["race"], current_avatar["skin_color"])
    drawHeadwear("crown", "elf")  # 测试新皇冠
```

## 性能考虑 (Performance Considerations)

### 当前实现

- 静态图像: 只在点击时重绘
- 简单几何: 只使用矩形
- 无渐变: 纯色填充

### 如果添加复杂功能

如果要添加动画或更复杂的图形:

1. 考虑使用 PImage 缓存
2. 只重绘改变的部分
3. 使用 frameRate() 控制更新频率

## 贡献指南 (Contribution Guidelines)

### 代码风格

1. **函数命名**: 使用 camelCase (与 Processing 一致)
2. **注释**: 中英文双语注释
3. **像素块**: 始终使用 PIXEL 常量，不要硬编码 8
4. **颜色**: 使用 color() 函数，包含注释说明颜色用途

### 提交前检查

- [ ] 代码通过语法检查
- [ ] 添加了必要的注释
- [ ] 测试了所有新功能
- [ ] 更新了相关文档
- [ ] 新元素与现有风格一致

## 未来扩展想法 (Future Extension Ideas)

### 短期改进
1. 添加更多种族 (如: 龙人、鱼人、树人)
2. 添加更多配饰 (如: 眼镜、面具、胡须)
3. 添加背景元素
4. 实现保存功能 (按 's' 键保存图片)

### 中期改进
1. 添加颜色主题切换
2. 实现头像动画 (眨眼、摆动)
3. 添加名称生成器
4. 创建头像画廊模式

### 长期改进
1. 多人物同时显示
2. 导出为精灵表 (sprite sheet)
3. Web 版本移植
4. 自定义模式 (用户选择元素)

## 资源链接 (Resource Links)

- [Processing 官方文档](https://processing.org/reference/)
- [Processing Python Mode](https://py.processing.org/)
- [像素艺术教程](https://opengameart.org/)
- [颜色选择工具](https://coolors.co/)

## 获取帮助 (Getting Help)

如果遇到问题:
1. 检查 Processing 控制台的错误信息
2. 使用 print() 调试变量值
3. 参考现有代码的实现方式
4. 在项目 Issues 中提问

祝你开发愉快! Happy coding! 🚀
