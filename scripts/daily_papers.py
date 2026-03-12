#!/usr/bin/env python3
"""
每日论文推荐 v1.0 - 完整流程
整合: 采集 -> 生成 -> 推送
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def run_script(script_name, description, timeout=300):
    """运行子脚本"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print('='*60)
    
    script_path = Path(f"/root/.openclaw/workspace/second-brain/scripts/{script_name}")
    
    try:
        result = subprocess.run(
            ['python3', str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.returncode != 0 and result.stderr:
            print(f"stderr: {result.stderr[:500]}")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"❌ 超时")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def git_push(date_str):
    """推送到 GitHub"""
    print(f"\n{'='*60}")
    print("🚀 推送到 GitHub")
    print('='*60)
    
    repo_path = "/root/.openclaw/workspace/second-brain"
    
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Add daily paper recommendations for {date_str}'], 
                      cwd=repo_path, capture_output=True)
        result = subprocess.run(['git', 'push', 'origin', 'main'], 
                              cwd=repo_path, capture_output=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ 推送成功")
            return True
        else:
            print(f"⚠️ 推送可能有问题")
            return False
            
    except Exception as e:
        print(f"❌ 推送错误: {e}")
        return False

def main():
    """主函数"""
    date_str = datetime.now().strftime('%Y%m%d')
    
    print("📚 每日论文推荐 v1.0")
    print("专注领域: 自动驾驶 | Physical AI | AI Agent")
    print(f"日期: {date_str}")
    print("=" * 60)
    
    # 步骤1: 采集和评分
    if not run_script('daily_papers_collector.py', '步骤1/2: 采集论文 (arXiv + HF Daily)', timeout=120):
        print("❌ 采集失败")
        return 1
    
    # 步骤2: 生成简报
    if not run_script('daily_papers_generator.py', '步骤2/2: 生成推荐简报', timeout=60):
        print("❌ 生成失败")
        return 1
    
    # 推送
    git_push(date_str)
    
    print("\n" + "=" * 60)
    print("🎉 每日论文推荐生成完成！")
    print(f"📖 查看地址: https://andy03withai.github.io/second-brain/daily-papers/{date_str}/")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
