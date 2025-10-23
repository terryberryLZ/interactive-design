# 美术素材生成指南

## 推荐工具：Leonardo.ai

访问：https://leonardo.ai/
- 注册免费账号（每天150 tokens）
- 选择模型：**RPG 4.0** 或 **DreamShaper v7**（适合奇幻风格）

## 素材规格

### 统一设置：
- **尺寸**: 512x512 或 256x256（小尺寸更快）
- **背景**: 透明背景（PNG格式）
- **风格**: Fantasy RPG pixel art / 16-bit game sprite

### 素材分类和数量建议：

1. **帽子 (hats/)** - 建议10-15个
   - 巫师帽、头盔、王冠、兜帽等

2. **发型 (hair/)** - 建议10-15个
   - 长发、短发、辫子、光头等

3. **衣服 (clothes/)** - 建议10-15个
   - 法师袍、盔甲、斗篷、衬衫等

4. **配饰 (accessories/)** - 建议5-10个
   - 眼镜、项链、徽章、武器等

5. **背景 (backgrounds/)** - 建议3-5个
   - 简单纯色或渐变，不要太复杂

## Prompt 模板

### 帽子类：
```
fantasy RPG game asset, [wizard hat/knight helmet/crown/hood], 
pixel art style, 16-bit, transparent background, 
front view, clean design, vibrant colors, isolated object
```

### 发型类：
```
fantasy RPG character hair, [long flowing hair/short spiky hair/braids/bald], 
pixel art style, 16-bit, transparent background,
front view, clean design, vibrant colors, isolated hairstyle
```

### 衣服类：
```
fantasy RPG character clothing, [wizard robe/knight armor/cloak/tunic],
pixel art style, 16-bit, transparent background,
front view, clean design, vibrant colors, isolated garment
```

### 配饰类：
```
fantasy RPG accessory, [glasses/necklace/badge/sword],
pixel art style, 16-bit, transparent background,
front view, clean design, vibrant colors, isolated item
```

## 负面提示词（Negative Prompt）：
```
blurry, low quality, realistic, 3D render, photo, 
complex background, multiple objects, side view, back view
```

## 生成后处理：

1. **下载PNG格式**
2. **确保透明背景**（用Photoshop或在线工具去除白色背景）
3. **统一尺寸**（推荐256x256像素）
4. **命名规范**：
   - `hat_01.png`, `hat_02.png`, ...
   - `hair_01.png`, `hair_02.png`, ...
   - `clothes_01.png`, `clothes_02.png`, ...
   - `accessory_01.png`, `accessory_02.png`, ...

## 在线工具推荐：

- **去除背景**: https://www.remove.bg/ 或 https://www.photoroom.com/
- **调整尺寸**: https://www.iloveimg.com/resize-image
- **批量处理**: https://www.birme.net/

## 快速开始：

1. 先生成5-10个素材测试效果
2. 放到对应文件夹
3. 运行生成器查看效果
4. 满意后批量生成更多素材

---

**提示**: 保持素材风格一致很重要！在Leonardo.ai中选择同一个模型和相似的prompt结构。
