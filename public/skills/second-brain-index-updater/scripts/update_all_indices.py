#!/usr/bin/env python3
"""
第二大脑索引更新脚本 - 统一入口
更新所有索引页面
"""

import subprocess
import sys
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    
    print("🔄 开始更新第二大脑索引...\n")
    
    # 更新深度调研索引
    print("📊 更新深度调研索引...")
    result = subprocess.run(
        [sys.executable, str(script_dir / "update_deep_research_index.py")],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    
    # 更新首页文章列表
    print("\n📰 更新首页文章列表...")
    result = subprocess.run(
        [sys.executable, str(script_dir / "update_homepage_articles.py")],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    
    print("\n✅ 所有索引更新完成！")
    print("\n记得执行 git add + commit + push 来部署更新")

if __name__ == "__main__":
    main()
