# 奇幻头像生成器 (Fantasy Avatar Generator)

一个模块化的奇幻风格头像生成器，支持AI生成的美术素材组合。

A modular fantasy avatar generator with AI-generated art asset support.

---

## 📦 版本说明 (Versions)

### 经典版 (Classic) - `fantasy_avatar_generator.py`
- ✅ 轻量级像素艺术生成器
- ✅ 无需额外素材，开箱即用
- 适合：快速生成、学习、打包成exe

### V2模块版 (Asset-Based) - `fantasy_avatar_generator_v2.py` ⭐ 推荐
- ✅ 支持加载AI生成的美术模块
- ✅ 自动组合素材生成头像
- ✅ 支持保存功能
- 适合：高质量定制化头像生成

---

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install pygame
```

### 2. 运行经典版
```bash
python fantasy_avatar_generator.py
```

### 3. 运行V2模块版
```bash
python fantasy_avatar_generator_v2.py
```

**首次运行**: V2版会使用fallback模式（简单图形），添加AI素材后自动使用高质量资源。

---

## 🎨 添加AI生成的美术素材

### 快速指南：

1. **阅读详细教程**: 查看 `ASSET_GENERATION_GUIDE.md`

2. **推荐工具**: [Leonardo.ai](https://leonardo.ai/) (免费账号每天可生成30-50张)

3. **生成素材**: 使用提供的prompt模板生成以下类别：
   - 帽子 (Hats)
   - 发型 (Hair)
   - 衣服 (Clothes)
   - 配饰 (Accessories)
   - 背景 (Backgrounds)

4. **添加到项目**:
   ```
   assets/
   ├── hats/        ← 放置帽子PNG (512x512, 透明背景)
   ├── hair/        ← 放置发型PNG
   ├── clothes/     ← 放置衣服PNG
   ├── accessories/ ← 放置配饰PNG
   └── backgrounds/ ← 放置背景PNG
   ```

5. **重新运行生成器**: V2版会自动加载所有素材！

### 素材要求：
- ✅ PNG格式，透明背景
- ✅ 推荐尺寸：512x512 或 256x256
- ✅ 奇幻/RPG风格
- ✅ 统一画风（使用相同的AI模型和prompt结构）

---

## ⌨️ 操作说明 (Controls)

| 操作 | 功能 |
|------|------|
| **鼠标点击** / **R键** | 生成新头像 |
| **S键** (仅V2) | 保存当前头像到 `output/` 文件夹 |
| **ESC** | 退出程序 |

---

## 📁 项目结构

```
interactive-design/
├── fantasy_avatar_generator.py      # 经典像素版
├── fantasy_avatar_generator_v2.py   # V2模块版 ⭐
├── ASSET_GENERATION_GUIDE.md        # AI素材生成详细教程
├── requirements.txt                 # 依赖清单
├── assets/                          # 美术素材目录
│   ├── hats/
│   ├── hair/
│   ├── clothes/
│   ├── accessories/
│   └── backgrounds/
└── output/                          # 保存的头像 (自动创建)
```

---

## 🎯 工作流程建议

### 初次使用：
1. 先运行经典版熟悉功能
2. 阅读 `ASSET_GENERATION_GUIDE.md`
3. 使用Leonardo.ai生成5-10个测试素材
4. 运行V2版测试效果
5. 满意后批量生成更多素材

### 持续优化：
- 保持素材风格一致（使用相同AI模型）
- 按需添加新类别素材
- 调整生成概率（修改代码中的random.random()阈值）

---

## 💡 技术细节

- **语言**: Python 3.8+
- **核心库**: Pygame
- **分辨率**: 512x512 像素
- **素材格式**: PNG (RGBA)
- **组合方式**: 随机分层叠加

---

## 📝 许可证

MIT License

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**提示**: 如果你不想自己生成素材，也可以在网上找现成的RPG sprite素材包（确保使用许可允许）。
