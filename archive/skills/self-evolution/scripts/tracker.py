#!/usr/bin/env python3
"""
Ace 自我进化系统 - 核心追踪器
记录错误、遥测数据、用户反馈
"""

import json
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = "/root/.openclaw/workspace/second-brain"
MEMORY_DIR = f"{BASE_DIR}/memory"

class EvolutionTracker:
    """进化追踪器"""
    
    def __init__(self):
        self.ensure_dirs()
    
    def ensure_dirs(self):
        """确保目录存在"""
        for subdir in ['errors', 'telemetry', 'feedback', 'reviews']:
            os.makedirs(f"{MEMORY_DIR}/{subdir}", exist_ok=True)
    
    def log_error(self, error_data):
        """记录错误"""
        now = datetime.now()
        filepath = f"{MEMORY_DIR}/errors/{now.strftime('%Y-%m')}.jsonl"
        
        record = {
            "timestamp": now.isoformat(),
            "date": now.strftime('%Y-%m-%d'),
            "week": now.strftime('%Y-W%W'),
            **error_data
        }
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        print(f"[Evolution] 错误已记录: {error_data.get('error_category', 'unknown')}")
    
    def log_telemetry(self, task_data):
        """记录任务遥测"""
        now = datetime.now()
        filepath = f"{MEMORY_DIR}/telemetry/{now.strftime('%Y-%m')}.jsonl"
        
        record = {
            "timestamp": now.isoformat(),
            "date": now.strftime('%Y-%m-%d'),
            "week": now.strftime('%Y-W%W'),
            **task_data
        }
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def log_feedback(self, feedback_data):
        """记录用户反馈"""
        now = datetime.now()
        filepath = f"{MEMORY_DIR}/feedback/{now.strftime('%Y-%m')}.jsonl"
        
        record = {
            "timestamp": now.isoformat(),
            "date": now.strftime('%Y-%m-%d'),
            **feedback_data
        }
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        print(f"[Evolution] 反馈已记录: {feedback_data.get('rating', 'unknown')}")
    
    def get_error_stats(self, days=7):
        """获取错误统计"""
        errors = []
        
        # 读取最近文件
        now = datetime.now()
        for i in range(2):  # 最近2个月
            month_str = (now.replace(day=1) - __import__('datetime').timedelta(days=i*30)).strftime('%Y-%m')
            filepath = f"{MEMORY_DIR}/errors/{month_str}.jsonl"
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    for line in f:
                        try:
                            record = json.loads(line.strip())
                            errors.append(record)
                        except:
                            pass
        
        # 统计
        from collections import Counter
        category_counts = Counter([e.get('error_category', 'unknown') for e in errors])
        
        return {
            "total_errors": len(errors),
            "by_category": dict(category_counts),
            "recent": errors[-10:] if errors else []
        }
    
    def get_telemetry_stats(self, days=7):
        """获取遥测统计"""
        tasks = []
        
        now = datetime.now()
        for i in range(2):
            month_str = (now.replace(day=1) - __import__('datetime').timedelta(days=i*30)).strftime('%Y-%m')
            filepath = f"{MEMORY_DIR}/telemetry/{month_str}.jsonl"
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    for line in f:
                        try:
                            record = json.loads(line.strip())
                            tasks.append(record)
                        except:
                            pass
        
        # 统计
        from collections import Counter
        type_counts = Counter([t.get('type', 'unknown') for t in tasks])
        skill_counts = Counter([t.get('skill_used', 'none') for t in tasks])
        
        success_count = sum(1 for t in tasks if t.get('success', True))
        success_rate = success_count / len(tasks) if tasks else 0
        
        return {
            "total_tasks": len(tasks),
            "success_rate": round(success_rate * 100, 1),
            "by_type": dict(type_counts),
            "by_skill": dict(skill_counts)
        }

# 全局实例
tracker = EvolutionTracker()

# 便捷函数
def log_error(**kwargs):
    """记录错误"""
    tracker.log_error(kwargs)

def log_telemetry(**kwargs):
    """记录遥测"""
    tracker.log_telemetry(kwargs)

def log_feedback(**kwargs):
    """记录反馈"""
    tracker.log_feedback(kwargs)

if __name__ == "__main__":
    # 测试
    log_error(
        task_type="daily_brief",
        error_category="api_timeout",
        error_message="Semantic Scholar timeout",
        recovery_action="used_fallback"
    )
    
    log_telemetry(
        task_type="content_generation",
        skill_used="daily-brief",
        duration_sec=154,
        success=True
    )
    
    log_feedback(
        task_type="daily_brief",
        rating=5,
        comment="今天的内容很相关"
    )
    
    print("\n错误统计:", tracker.get_error_stats())
    print("遥测统计:", tracker.get_telemetry_stats())
