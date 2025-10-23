"""
批量生成奇幻风格美术素材
使用开源的 Stable Diffusion 模型
完全本地运行，免费无限制
"""

import os
from pathlib import Path

# 检查是否安装了必要的库
try:
    from diffusers import StableDiffusionPipeline
    import torch
except ImportError:
    print("❌ 需要安装依赖:")
    print("pip install diffusers transformers accelerate torch torchvision")
    exit(1)

# 创建素材目录
ASSETS_DIR = Path("ai_generated_assets")
CATEGORIES = {
    "hats": [
        "fantasy wizard hat",
        "medieval knight helmet", 
        "golden royal crown",
        "leather adventurer hood",
        "magic rune headband",
        "horned viking helmet",
        "feathered tribal headdress",
        "iron barbarian helmet",
        "elven circlet with gems",
        "dark sorcerer hood"
    ],
    "hair": [
        "long flowing blonde hair",
        "short spiky red hair",
        "braided brown hair",
        "curly black hair",
        "straight silver hair",
        "ponytail purple hair",
        "bald head",
        "messy green hair",
        "wavy blue hair",
        "dreadlocks hair"
    ],
    "clothes": [
        "blue wizard robe",
        "silver knight armor",
        "red leather tunic",
        "green forest cloak",
        "purple mage robes",
        "golden paladin armor",
        "black assassin outfit",
        "white priest robe",
        "brown adventurer vest",
        "grey warrior armor"
    ],
    "accessories": [
        "round wizard glasses",
        "golden amulet necklace",
        "silver hoop earrings",
        "ruby pendant",
        "magic staff",
        "iron sword",
        "wooden bow",
        "leather belt with pouches",
        "magical orb",
        "ancient tome book"
    ]
}

# Prompt模板
BASE_PROMPT = "fantasy RPG game character {item}, pixel art style, transparent background, front view, simple clean design, vibrant colors, isolated on white"
NEGATIVE_PROMPT = "blurry, low quality, realistic, 3D render, photo, complex background, multiple objects, side view"


def setup_model():
    """加载Stable Diffusion模型"""
    print("🔄 正在加载 Stable Diffusion 模型...")
    print("   (首次运行需要下载约4GB，请耐心等待)")
    
    # 使用较小的SD 1.5模型（速度快）
    model_id = "runwayml/stable-diffusion-v1-5"
    
    # 检测是否有GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"   使用设备: {device}")
    
    if device == "cpu":
        print("   ⚠️ 未检测到GPU，使用CPU会很慢（每张图约30-60秒）")
        print("   建议使用GPU或减少生成数量")
    
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        safety_checker=None  # 禁用安全检查加快速度
    )
    pipe = pipe.to(device)
    
    # 优化设置
    if device == "cuda":
        pipe.enable_attention_slicing()  # 节省显存
    
    print("✅ 模型加载完成!\n")
    return pipe


def generate_assets(pipe, category, items, output_dir):
    """生成指定类别的素材"""
    print(f"\n{'='*60}")
    print(f"🎨 开始生成 {category} 素材 ({len(items)}个)")
    print(f"{'='*60}")
    
    output_path = output_dir / category
    output_path.mkdir(parents=True, exist_ok=True)
    
    for idx, item in enumerate(items, 1):
        filename = f"{category}_{idx:02d}.png"
        filepath = output_path / filename
        
        # 跳过已存在的文件
        if filepath.exists():
            print(f"⏭️  [{idx}/{len(items)}] {filename} (已存在，跳过)")
            continue
        
        prompt = BASE_PROMPT.format(item=item)
        print(f"🖼️  [{idx}/{len(items)}] 正在生成: {item}...")
        
        try:
            # 生成图像
            image = pipe(
                prompt=prompt,
                negative_prompt=NEGATIVE_PROMPT,
                num_inference_steps=20,  # 降低步数加快速度（默认50）
                guidance_scale=7.5,
                width=512,
                height=512
            ).images[0]
            
            # 保存
            image.save(filepath)
            print(f"   ✅ 保存到: {filepath}")
            
        except Exception as e:
            print(f"   ❌ 生成失败: {e}")
    
    print(f"\n✅ {category} 类别完成!")


def main():
    """主函数"""
    print("="*60)
    print("🎨 开源AI素材批量生成器")
    print("="*60)
    print("\n本工具使用开源Stable Diffusion模型")
    print("完全免费，本地运行，无限制\n")
    
    # 创建输出目录
    ASSETS_DIR.mkdir(exist_ok=True)
    
    # 显示计划
    total_items = sum(len(items) for items in CATEGORIES.values())
    print(f"📋 将生成 {len(CATEGORIES)} 个类别，共 {total_items} 个素材:")
    for cat, items in CATEGORIES.items():
        print(f"   - {cat}: {len(items)} 个")
    
    # 确认
    print("\n⚠️ 注意:")
    print("   - 首次运行需下载约4GB模型")
    print("   - 如无GPU，生成会很慢（建议减少数量或使用GPU）")
    print("   - 预计时间: GPU约5-10分钟 / CPU约30-60分钟")
    
    response = input("\n是否继续？(y/n): ").strip().lower()
    if response != 'y':
        print("已取消")
        return
    
    # 加载模型
    try:
        pipe = setup_model()
    except Exception as e:
        print(f"\n❌ 模型加载失败: {e}")
        print("\n可能原因:")
        print("1. 网络问题，无法下载模型")
        print("2. 磁盘空间不足（需要约4GB）")
        print("3. 依赖库未正确安装")
        return
    
    # 生成所有类别
    for category, items in CATEGORIES.items():
        generate_assets(pipe, category, items, ASSETS_DIR)
    
    print("\n" + "="*60)
    print("🎉 所有素材生成完成!")
    print(f"📁 保存位置: {ASSETS_DIR.absolute()}")
    print("="*60)
    print("\n下一步:")
    print("1. 检查生成的素材质量")
    print("2. 删除不满意的图片")
    print("3. 使用生成器加载这些素材")


if __name__ == "__main__":
    main()
