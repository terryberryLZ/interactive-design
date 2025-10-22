# Fantasy Avatar Generator - High Quality Version

## 新增高质量渲染模式

现在你的头像生成器有了两个版本：

### 1. 原版像素风格（fantasy_avatar_generator.py）
- 传统像素艺术风格
- 无需额外依赖
- 快速轻量

### 2. 高质量奇幻风格（fantasy_avatar_hq.py）⭐ 新增
- 使用 SVG 矢量渲染
- 精致光滑的奇幻风格
- 更丰富的细节和效果

## 快速开始

### 安装依赖

```powershell
# 安装新的依赖（cairosvg 和 Pillow）
pip install -r requirements.txt
```

如果 cairosvg 安装遇到问题（Windows 常见），可以尝试：

```powershell
# 方案1: 使用预编译包
pip install pipwin
pipwin install cairocffi

# 方案2: 使用 conda（如果你有 Anaconda）
conda install -c conda-forge cairosvg

# 方案3: 继续使用（会降级到简单渲染模式，但仍可运行）
# 程序会自动检测并提示
```

### 运行高质量版本

```powershell
# 运行新的高质量生成器
python fantasy_avatar_hq.py

# 使用固定种子（可复现）
python fantasy_avatar_hq.py --seed 12345
```

### 控制方式

- **点击鼠标** 或 **按 R 键**：生成新头像
- **按 S 键**：保存当前头像到 output/ 文件夹
- **按 ESC 键**：退出程序

## 主要改进

### 1. 更精致的绘制

使用 SVG 矢量图形替代像素块：
- 平滑的曲线和渐变
- 更自然的光影效果
- 丰富的细节和装饰

### 2. 更好的部件设计

- **头部**：不同种族有独特的脸型和特征
  - 人类：平衡圆润
  - 兽人：强壮方正，带獠牙
  - 精灵：优雅尖耳
  - 矮人：结实，带大胡子
  - 哥布林：小巧尖耳

- **表情**：更生动的面部表情
  - handsome：自信微笑
  - serious：严肃坚定
  - cute：可爱腮红
  - goofy：搞怪吐舌

- **装备**：更华丽的装饰
  - 头饰：角盔、花冠、法师帽、触手帽等
  - 项链：符文吊坠、骷髅、宝石项圈等
  - 耳环：耳钉、圆环、羽毛、骨饰
  - 衣服：长袍、盔甲、束腰外衣、斗篷、连帽衫

- **背景**：多样化背景
  - 纯色（紫、蓝、粉）
  - 渐变（日落、海洋）
  - 图案（星空、圆点）

### 3. 性能优化

- 自动缓存已渲染的元素
- 只在需要时重新渲染
- 支持实时交互生成

## 技术细节

### 架构

```
fantasy_avatar_hq.py          # 主程序（高质量版本）
├── fantasy_render.py         # SVG 渲染模块
│   ├── 背景生成
│   ├── 头部生成（按种族）
│   ├── 表情生成
│   ├── 装备生成（头饰/项链/耳环/衣服）
│   └── 渲染缓存
└── 依赖
    ├── pygame (显示和交互)
    ├── cairosvg (SVG -> PNG 渲染)
    └── Pillow (图像处理)
```

### 渲染流程

1. 程序化生成 SVG 代码（每个部件）
2. 使用 cairosvg 将 SVG 渲染为高质量 PNG
3. 转换为 pygame Surface
4. 按层次叠加到屏幕上

### 自定义和扩展

你可以轻松添加新元素：

1. 在 `fantasy_render.py` 中添加新的生成函数
2. 在 `fantasy_avatar_hq.py` 的选项列表中添加新类型
3. 在 `generate_avatar()` 中调用渲染

示例 - 添加新头饰：

```python
# 在 fantasy_render.py 的 generate_headwear_svg() 中：
elif headwear_type == "crown":
    # 画一个皇冠
    svg_parts.append(f'<path d="..." fill="gold"/>')
```

## 对比

| 特性 | 原版像素风 | 高质量版 |
|------|-----------|---------|
| 风格 | 复古像素艺术 | 现代奇幻风 |
| 细节 | 简单像素块 | 平滑矢量图 |
| 性能 | 极快 | 快（有缓存）|
| 依赖 | 仅 pygame | +cairosvg +Pillow |
| 文件大小 | 小 | 中等 |
| 适用场景 | 像素游戏、复古风 | 现代游戏、精致头像 |

## 下一步

- 可以调整 `fantasy_render.py` 中的颜色、大小、形状参数
- 添加更多种族、表情、装备类型
- 导出为透明背景 PNG
- 批量生成画廊（参考 `demo_batch_generate.py`）

## 故障排除

### cairosvg 安装失败（Windows）

如果遇到编译错误，尝试：
1. 安装 GTK+ runtime：https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
2. 或使用 conda 环境
3. 或联系我获取预编译版本

### 程序运行但渲染为纯色

这说明 cairosvg 未正确安装，程序降级到了基础模式。重新安装依赖即可。

### 内存占用高

清除缓存可以释放内存（已自动管理），或重启程序。

---

**享受创作精美的奇幻头像！** ✨🧙‍♂️🧝‍♀️⚔️
