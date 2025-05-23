#!/usr/bin/env python3
"""Run development server for SayZhong."""

import subprocess
import sys
from pathlib import Path


def main():
    """Run the development server."""
    print("🚀 Starting SayZhong development environment...")
    
    # Add src to Python path
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))
    
    try:
        # For now, just run a simple Python REPL with the package loaded
        # You can modify this to run your actual application
        print("📦 Loading SayZhong package...")
        import sayzhong
        print(f"✅ SayZhong {sayzhong.__version__} loaded successfully")
        
        print("\n💡 Development server placeholder")
        print("   Modify this script to run your actual application")
        print("   For example:")
        print("   - Web server (FastAPI, Flask, etc.)")
        print("   - CLI application")
        print("   - Jupyter notebook server")
        
        # Start Python interactive session
        print("\n🐍 Starting Python interactive session...")
        subprocess.run([sys.executable, "-i", "-c", "import sayzhong; print('SayZhong loaded. Type help(sayzhong) for info.')"])
        
    except ImportError as e:
        print(f"❌ Failed to import SayZhong: {e}")
        print("💡 Try running: pip install -e .")
        sys.exit(1)


if __name__ == "__main__":
    main()
