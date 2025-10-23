#!/usr/bin/env python3
"""
Quick GPU/CUDA Test Script
Tests if PyTorch can detect and use your GPU
"""

print("🔍 Testing GPU/CUDA Setup...")
print("=" * 50)

try:
    import torch
    print(f"✅ PyTorch version: {torch.__version__}")
    print(f"✅ CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"✅ CUDA version: {torch.version.cuda}")
        print(f"✅ GPU device count: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            print(f"\n🎮 GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"   VRAM: {props.total_memory / 1024**3:.2f} GB")
            print(f"   Compute Capability: {props.major}.{props.minor}")
            print(f"   Multiprocessors: {props.multi_processor_count}")
        
        # Test if we can actually use the GPU
        print("\n🧪 Testing GPU computation...")
        try:
            x = torch.rand(1000, 1000).cuda()
            y = torch.rand(1000, 1000).cuda()
            z = x @ y
            print("✅ GPU computation works!")
            
            # Clean up
            del x, y, z
            torch.cuda.empty_cache()
            
        except Exception as e:
            print(f"❌ GPU computation failed: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 GPU is ready for fast AI generation!")
        print("   Generation time: 10-30 seconds (vs 2-5 minutes on CPU)")
        
    else:
        print("\n⚠️  CUDA not available!")
        print("   Possible reasons:")
        print("   1. No NVIDIA GPU in your system")
        print("   2. GPU drivers not installed")
        print("   3. CUDA toolkit not compatible")
        print("\n   Will use CPU (slow but works)")
        
except ImportError:
    print("❌ PyTorch not installed!")
    print("   Run: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128")

print("=" * 50)
