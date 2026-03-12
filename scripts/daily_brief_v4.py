#!/usr/bin/env python3
"""
每日简报 v4.0 - 完整生成流程
整合: 采集 -> 评分 -> 生成 -> 推送
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def run_script(script_name, description):
    """运行子脚本并输出状态"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print('='*60)
    
    script_path = Path(f"/root/.openclaw/workspace/second-brain/scripts/{script_name}")
    
    try:
        result = subprocess.run(
            ['python3', str(script_path)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # 输出 stdout
        if result.stdout:
            print(result.stdout)
        
        # 如果有错误但返回码为0，可能是警告
        if result.returncode != 0:
            print(f"⚠️ 返回码: {result.returncode}")
            if result.stderr:
                print(f"stderr: {result.stderr[:500]}")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"❌ 超时: {description}")
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
        # git add
        result = subprocess.run(
            ['git', 'add', '.'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        # git commit
        result = subprocess.run(
            ['git', 'commit', '-m', f'Add daily brief v4.0 for {date_str}'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 and 'nothing to commit' not in result.stdout:
            print(f"⚠️ Commit 可能失败或没有变更: {result.stdout}")
        
        # git push
        result = subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ 推送成功")
            return True
        else:
            print(f"⚠️ 推送可能有问题: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 推送错误: {e}")
        return False

def main():
    """主函数"""
    date_str = datetime.now().strftime('%Y%m%d')
    
    print("🤖 Ace 每日简报生成系统 v4.0")
    print("基于 AI 资讯速览方法论升级")
    print(f"日期: {date_str}")
    print("=" * 60)
    
    # 步骤1: 采集信息源
    if not run_script('daily_brief_collector_v4.py', '步骤1/4: 采集信息源 (20+ 英文源)'):
        print("❌ 采集失败，中止")
        return 1
    
    # 步骤2: 评分筛选
    if not run_script('daily_brief_scorer_v4.py', '步骤2/4: 评分筛选 (多源交叉验证)'):
        print("❌ 评分失败，中止")
        return 1
    
    # 步骤3: 生成简报
    if not run_script('daily_brief_generator_v4.py', '步骤3/4: 生成简报 (AI选题 + 深度报道)'):
        print("❌ 生成失败，中止")
        return 1
    
    # 步骤4: 推送
    git_push(date_str)
    
    print("\n" + "=" * 60)
    print("🎉 每日简报 v4.0 生成完成！")
    print(f"📖 查看地址: https://andy03withai.github.io/second-brain/input/{date_str}/")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
