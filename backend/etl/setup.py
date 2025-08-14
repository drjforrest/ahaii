#!/usr/bin/env python3
"""
AHAII ETL System Setup Script
Automated setup and configuration for the enhanced ETL system
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path


def run_command(cmd, check=True):
    """Run shell command with error handling"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    else:
        print(f"✅ Success: {result.stdout[:200]}")
        return True


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")

    # Install base requirements
    base_req = Path(__file__).parent.parent / "requirements.txt"
    if base_req.exists():
        if not run_command(f"pip install -r {base_req}"):
            return False

    # Install ETL-specific requirements
    etl_req = Path(__file__).parent / "requirements-etl.txt"
    if etl_req.exists():
        if not run_command(f"pip install -r {etl_req}"):
            return False

    return True


def check_environment():
    """Check environment variables and configuration"""
    print("\n🔧 Checking environment configuration...")

    required_vars = ["SUPABASE_URL", "SUPABASE_KEY"]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file or environment")
        return False

    print("✅ Environment configuration OK")
    return True


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")

    dirs = ["logs", "data", "exports", "backups"]

    for dir_name in dirs:
        dir_path = Path(__file__).parent / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Created: {dir_path}")

    return True


async def test_database_connection():
    """Test database connectivity"""
    print("\n🔗 Testing database connection...")

    try:
        # Import here to ensure dependencies are installed
        from config.database import supabase

        result = supabase.table("countries").select("id").limit(1).execute()
        if result.data is not None:
            print("✅ Database connection successful")
            return True
        else:
            print(f"❌ Database connection failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False


async def run_quick_test():
    """Run quick validation test"""
    print("\n🧪 Running quick validation test...")

    try:
        # Import ETL modules
        from .test_etl import run_quick_test

        success = await run_quick_test()
        if success:
            print("✅ Quick test passed")
            return True
        else:
            print("❌ Quick test failed")
            return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


def show_next_steps():
    """Show next steps after setup"""
    print(
        f"""
{'='*60}
🎉 AHAII ETL Setup Complete!
{'='*60}

Next steps:
1. Set up environment variables in .env file:
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   SERPAPI_KEY=your_serpapi_key (optional)

2. Test the system:
   python -m etl.test_etl quick

3. Run the CLI:
   python -m etl.etl_cli --help

4. Check system health:
   python -m etl.etl_cli health

5. Start the scheduler:
   python -m etl.etl_cli scheduler start

6. Run your first pipeline:
   python -m etl.etl_cli pipeline run --component news

For more information, see the README.md file.
"""
    )


async def main():
    """Main setup function"""
    print("🏥 AHAII ETL System Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)

    # Create directories
    if not create_directories():
        print("❌ Directory creation failed")
        sys.exit(1)

    # Check environment (optional for initial setup)
    env_ok = check_environment()
    if not env_ok:
        print("⚠️  Environment check failed - you may need to configure .env file")

    # Test database (optional)
    if env_ok:
        db_ok = await test_database_connection()
        if db_ok:
            # Run quick test if database is working
            await run_quick_test()

    # Show next steps
    show_next_steps()

    print("✅ Setup completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
