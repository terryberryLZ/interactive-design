# 奇幻像素头像生成器 (Fantasy Pixel Avatar Generator)

一个交互式奇幻风格像素头像生成器，可生成随机组合的幽默、可爱、搞怪的大头照式头像。支持 Processing Python Mode 和 Pygame 两种版本。

An interactive fantasy-style pixel avatar generator that creates randomly combined humorous, cute, and quirky portrait-style avatars. Available in both Processing Python Mode and Pygame versions.

## ✨ NEW: High Quality Version Available!

**现在提供高质量奇幻风格渲染版本！** 使用 SVG 矢量图形技术，生成更精致、更具细节的奇幻头像。

- 📁 文件: `fantasy_avatar_hq.py` + `fantasy_render.py`
- 🎨 特点: 平滑曲线、丰富细节、光影效果、渐变背景
- 📖 详细说明: 查看 [HQ_VERSION_GUIDE.md](HQ_VERSION_GUIDE.md)
- 🚀 快速开始:
  ```powershell
  pip install -r requirements.txt
  python fantasy_avatar_hq.py
  ```

## 🎮 Three Versions Available

### Version 1: Processing Python Mode (Original)
- File: `fantasy_avatar_generator.pyde`
- Requires: Processing with Python Mode installed
- Best for: Learning and creative coding

### Version 2: Standalone Pygame (Pixel Style)
- File: `fantasy_avatar_generator.py`
- Requires: Python 3.8+ and Pygame
- Features: Command-line arguments, seed support, save function
- Can be packaged as Windows .exe

### Version 3: High Quality (NEW) ⭐
- Files: `fantasy_avatar_hq.py` + `fantasy_render.py`
- Requires: Python 3.8+, Pygame, cairosvg, Pillow
- Features: SVG-based rendering, smooth graphics, rich details
- Best for: Modern fantasy avatars with professional quality

## 功能特点 (Features)

### 用户交互 (User Interaction)
- **Mouse Click / 鼠标点击**: Generate new avatar / 生成新头像
- **Press R**: Generate new avatar / 生成新头像
- **Press S** (Pygame only): Save avatar as PNG / 保存头像为PNG
- **Press ESC** (Pygame only): Exit program / 退出程序
- **--seed parameter** (Pygame only): Reproducible generation / 可复现生成

### 头像元素 (Avatar Elements)

#### 基础属性 (Basic Attributes)
- **性别 (Gender)**: 男 / 女 (Male / Female)
- **种族 (Race)**: 人类、兽人、精灵、矮人、地精 (Human, Orc, Elf, Dwarf, Goblin)
- **皮肤颜色 (Skin Color)**: 8种奇幻肤色 (8 fantasy skin tones)
  - 绿色 (兽人/地精)
  - 浅色 (精灵/人类)
  - 棕褐色、桃色、淡黄色等 (人类)
  - 淡绿色、淡蓝色等

#### 表情 (Expressions)
- 英俊 (Handsome) - 自信的笑容配挑眉
- 严肃 (Serious) - 直线嘴巴配皱眉
- 可爱 (Cute) - 圆圆的嘴和腮红
- 搞怪 (Goofy) - 吐舌头配眨眼和挑眉

#### 头饰 (Headwear)
- 角盔 (Horn Helmet) - 带角的金属头盔
- 花冠 (Flower Crown) - 彩色花朵和绿叶
- 巫师帽 (Wizard Hat) - 高高的尖顶帽配星星装饰
- 触手帽 (Tentacle Hat) - 章鱼风格的帽子
- 头巾 (Headband) - 简单头巾配装饰
- 无 (None)

#### 首饰 (Jewelry)
**项链 (Necklaces)**:
- 骷髅吊坠 (Skull Pendant)
- 宝石项圈 (Gem Collar)
- 叶子项链 (Leaf Necklace)
- 符文吊坠 (Rune Pendant) - 发光魔法符文
- 无 (None)

**耳饰 (Earrings)**:
- 圆环 (Hoop)
- 羽毛 (Feather)
- 骨头 (Bone)
- 耳钉 (Stud) - 金色小耳钉
- 无 (None)

#### 衣服 (Clothing)
- 长袍 (Robe) - 流动的法师长袍配腰带
- 盔甲 (Armor) - 板甲装备
- 束腰外衣 (Tunic) - 简单的束腰外衣
- 斗篷 (Cloak) - 神秘的斗篷配金色扣环
- 连帽衫 (Hoodie) - 现代风格连帽衫

#### 背景 (Backgrounds)
- 纯色 (Solid Colors) - 紫色、蓝色、粉色
- 渐变 (Gradients) - 日落渐变、海洋渐变
- 图案 (Patterns) - 星星图案、圆点图案

### 绘图风格 (Drawing Style)
- 像素风格 (使用 `rect()` 模拟像素块)
- 画面尺寸: 512x512 像素 (从 128x128 逻辑画布 4倍放大)
- 使用简洁色块，部分背景支持渐变
- 每个元素用函数模块化绘制，便于组合和扩展

## 如何运行 (How to Run)

### Option 1: Processing Python Mode (Original Version)

#### 前置要求 (Prerequisites)
1. 下载并安装 [Processing](https://processing.org/download)
2. 在 Processing 中切换到 Python Mode:
   - 点击右上角的 "Java" 按钮
   - 选择 "Add Mode..."
   - 安装 "Python Mode for Processing 3"

#### 运行步骤 (Running the Program)
1. 启动 Processing
2. 确保已切换到 Python Mode
3. 打开 `fantasy_avatar_generator.pyde` 文件
4. 点击运行按钮 (或按 Ctrl+R / Cmd+R)
5. 在弹出的窗口中点击鼠标任意位置或按R键生成新头像

### Option 2: Pygame Standalone (New Version)

#### 安装依赖 (Install Dependencies)
```bash
pip install -r requirements.txt
```

或直接安装:
```bash
pip install pygame
```

#### 运行程序 (Run Program)

基本运行:
```bash
python fantasy_avatar_generator.py
```

使用特定种子 (可复现生成):
```bash
python fantasy_avatar_generator.py --seed 12345
```

#### 按键说明 (Controls)
- **鼠标点击 / Mouse Click**: 生成新头像 / Generate new avatar
- **R键 / R Key**: 生成新头像 / Generate new avatar
- **S键 / S Key**: 保存当前头像为PNG / Save current avatar as PNG
- **ESC键 / ESC Key**: 退出程序 / Exit program

### Option 3: Windows .exe (No Python Required)

See [BUILD_EXE.md](BUILD_EXE.md) for instructions on building a standalone Windows executable.

Once built, simply double-click `FantasyAvatarGenerator.exe` to run!

## 代码结构 (Code Structure)

### 主要函数 (Main Functions)

- `setup()` - 初始化程序，设置画布大小
- `draw()` - 主绘制循环 (静态图像)
- `mousePressed()` - 鼠标点击事件处理
- `generateAvatar()` - 生成随机头像并绘制

### 绘制模块 (Drawing Modules)

#### 头部相关 (Head-related)
- `drawHead(race, skin_col)` - 绘制头部/脸部
- `drawExpression(expression)` - 绘制面部表情

#### 配饰相关 (Accessory-related)
- `drawHeadwear(headwear_type, race)` - 绘制头饰
- `drawNecklace(necklace_type)` - 绘制项链
- `drawEarrings(earring_type)` - 绘制耳环

#### 服装相关 (Clothing-related)
- `drawClothes(clothes_type, skin_col)` - 绘制服装/盔甲

### 全局变量 (Global Variables)

- `PIXEL` - 像素块大小 (8x8)
- `GENDERS` - 性别选项列表
- `RACES` - 种族选项列表
- `SKIN_COLORS` - 皮肤颜色选项列表
- `EXPRESSIONS` - 表情选项列表
- `HEADWEAR` - 头饰选项列表
- `NECKLACES` - 项链选项列表
- `EARRINGS` - 耳环选项列表
- `CLOTHES` - 服装选项列表

## 扩展建议 (Extension Ideas)

1. 添加更多种族 (如龙人、鱼人等)
2. 增加更多配饰选项 (如眼镜、面具、胡须等)
3. 添加保存功能 (按键保存当前头像为图片)
4. 实现头像动画效果
5. 添加背景元素和装饰
6. 实现颜色主题系统
7. 添加头像名称生成器

## 技术细节 (Technical Details)

- **语言**: Processing Python Mode
- **画布尺寸**: 320x320 像素
- **像素块大小**: 8x8 像素
- **绘图方法**: 使用 `rect()` 函数绘制像素块
- **无描边**: 使用 `noStroke()` 实现纯色块效果

## 许可证 (License)

本项目采用开源许可，可自由使用和修改。

## 作者 (Author)

Created for interactive design learning and fun!

## 截图 (Screenshots)

运行程序后，每次点击鼠标都会生成一个独特的奇幻角色头像。尝试点击多次，发现各种有趣的组合！

Try clicking multiple times to discover various interesting combinations of fantasy characters!