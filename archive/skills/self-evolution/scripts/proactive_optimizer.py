#!/usr/bin/env python3
"""
Ace 自我进化系统 - 主动优化建议
识别问题模式，主动提出改进
"""

import json
import os
from datetime import datetime, timedelta
from collections import Counter

BASE_DIR = "/root/.openclaw/workspace/second-brain"
MEMORY_DIR = f"{BASE_DIR}/memory"

class ProactiveOptimizer:
    """主动优化器"""
    
    def __init__(self):
        self.suggestions_file = f"{MEMORY_DIR}/proactive_suggestions.jsonl"
    
    def check_error_patterns(self, threshold=3):
        """检查错误模式"""
        errors = []
        
        # 加载最近7天的错误
        now = datetime.now()
        for i in range(2):
            month_str = (now.replace(day=1) - __import__('datetime').timedelta(days=i*30)).strftime('%Y-%m')
            filepath = f"{MEMORY_DIR}/errors/{month_str}.jsonl"
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    for line in f:
                        try:
                            record = json.loads(line.strip())
                            record_date = datetime.fromisoformat(record['timestamp'])
                            if now - record_date <= timedelta(days=7):
                                errors.append(record)
                        except:
                            pass
        
        # 分析模式
        by_category = Counter([e.get('error_category') for e in errors])
        by_task = Counter([e.get('task_type') for e in errors])
        
        suggestions = []
        
        # 同类错误多次发生
        for category, count in by_category.items():
            if count >= threshold:
                suggestions.append({
                    "type": "error_pattern",
                    "priority": "高",
                    "trigger": f"{category} 错误本周发生{count}次",
                    "suggestion": self._get_error_solution(category),
                    "auto_fix_possible": self._can_auto_fix(category)
                })
        
        # 特定任务频繁出错
        for task, count in by_task.items():
            task_errors = [e for e in errors if e.get('task_type') == task]
            if len(task_errors) >= threshold:
                error_rate = len(task_errors) / max(self._get_task_count(task), 1)
                if error_rate > 0.3:  # 错误率>30%
                    suggestions.append({
                        "type": "task_stability",
                        "priority": "高",
                        "trigger": f"{task} 错误率{error_rate*100:.0f}%",
                        "suggestion": f"需要审查 {task} 的容错机制和异常处理",
                        "auto_fix_possible": False
                    })
        
        return suggestions
    
    def check_skill_usage(self, min_usage=10):
        """检查技能使用情况"""
        # 加载遥测
        telemetry = []
        now = datetime.now()
        
        for i in range(2):
            month_str = (now.replace(day=1) - __import__('datetime').timedelta(days=i*30)).strftime('%Y-%m')
            filepath = f"{MEMORY_DIR}/telemetry/{month_str}.jsonl"
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    for line in f:
                        try:
                            record = json.loads(line.strip())
                            record_date = datetime.fromisoformat(record['timestamp'])
                            if now - record_date <= timedelta(days=30):
                                telemetry.append(record)
                        except:
                            pass
        
        # 统计技能使用
        from collections import defaultdict
        skill_stats = defaultdict(lambda: {"count": 0, "success": 0, "ratings": []})
        
        for t in telemetry:
            skill = t.get('skill_used')
            if skill and skill != 'none':
                skill_stats[skill]["count"] += 1
                if t.get('success', True):
                    skill_stats[skill]["success"] += 1
        
        # 加载反馈
        for i in range(2):
            month_str = (now.replace(day=1) - __import__('datetime').timedelta(days=i*30)).strftime('%Y-%m')
            filepath = f"{MEMORY_DIR}/feedback/{month_str}.jsonl"
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    for line in f:
                        try:
                            record = json.loads(line.strip())
                            skill = record.get('task_type')
                            if skill and record.get('rating'):
                                skill_stats[skill]["ratings"].append(record['rating'])
                        except:
                            pass
        
        suggestions = []
        
        for skill, stats in skill_stats.items():
            if stats["count"] >= min_usage:
                success_rate = stats["success"] / stats["count"]
                avg_rating = sum(stats["ratings"]) / len(stats["ratings"]) if stats["ratings"] else 0
                
                # 成功率低
                if success_rate < 0.9:
                    suggestions.append({
                        "type": "skill_reliability",
                        "priority": "高",
                        "trigger": f"{skill} 使用{stats['count']}次，成功率{success_rate*100:.0f}%",
                        "suggestion": f"{skill} 需要增加错误处理和重试机制",
                        "auto_fix_possible": False
                    })
                
                # 满意度低
                if avg_rating > 0 and avg_rating < 3.5:
                    suggestions.append({
                        "type": "skill_quality",
                        "priority": "中",
                        "trigger": f"{skill} 平均评分{avg_rating:.1f}/5",
                        "suggestion": f"{skill} 的输出质量需要优化，建议收集具体改进点",
                        "auto_fix_possible": False
                    })
                
                # 使用频繁但无负面反馈，考虑扩展功能
                if stats["count"] >= 20 and success_rate > 0.95 and (avg_rating >= 4 or avg_rating == 0):
                    suggestions.append({
                        "type": "skill_extension",
                        "priority": "低",
                        "trigger": f"{skill} 高频使用且稳定，{stats['count']}次，成功率{success_rate*100:.0f}%",
                        "suggestion": f"{skill} 表现良好，可考虑增加更多功能或参数定制",
                        "auto_fix_possible": False
                    })
        
        return suggestions
    
    def _get_error_solution(self, category):
        """获取错误类别的解决方案"""
        solutions = {
            "api_timeout": "增加API超时重试机制，设置合理的超时时间，超时后使用降级策略（缓存/估算值）",
            "api_error": "增加API错误处理，区分临时错误和永久错误，临时错误可重试",
            "network_error": "增加网络错误重试，使用指数退避策略",
            "parse_error": "增强数据解析容错，增加字段存在性检查，使用try-except捕获",
            "logic_error": "审查业务逻辑，增加单元测试覆盖边界情况",
            "misunderstanding": "增加需求确认环节，复杂任务先输出理解摘要",
            "resource_error": "增加资源监控，内存/磁盘不足时提前预警"
        }
        return solutions.get(category, "需要具体分析根因")
    
    def _can_auto_fix(self, category):
        """判断是否可自动修复"""
        auto_fixable = ["api_timeout", "network_error", "parse_error"]
        return category in auto_fixable
    
    def _get_task_count(self, task_type):
        """获取任务总次数"""
        # 简化实现，实际应该查询遥测
        return 10
    
    def generate_suggestions(self):
        """生成所有优化建议"""
        all_suggestions = []
        
        # 检查错误模式
        all_suggestions.extend(self.check_error_patterns())
        
        # 检查技能使用
        all_suggestions.extend(self.check_skill_usage())
        
        # 保存建议
        if all_suggestions:
            with open(self.suggestions_file, 'a') as f:
                for sug in all_suggestions:
                    record = {
                        "timestamp": datetime.now().isoformat(),
                        "status": "pending",
                        **sug
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        return all_suggestions
    
    def format_suggestion_message(self, suggestions):
        """格式化建议消息"""
        if not suggestions:
            return None
        
        message = "🔍 Ace 发现以下可优化的地方:\n\n"
        
        high_priority = [s for s in suggestions if s['priority'] == '高']
        medium_priority = [s for s in suggestions if s['priority'] == '中']
        
        if high_priority:
            message += "【高优先级】\n"
            for i, sug in enumerate(high_priority, 1):
                message += f"{i}. **{sug['trigger']}**\n"
                message += f"   建议: {sug['suggestion']}\n"
                if sug['auto_fix_possible']:
                    message += f"   ✅ 我可以自动修复这个问题\n"
                message += "\n"
        
        if medium_priority:
            message += "【中优先级】\n"
            for i, sug in enumerate(medium_priority, 1):
                message += f"{i}. **{sug['trigger']}**\n"
                message += f"   建议: {sug['suggestion']}\n\n"
        
        message += "要我实施这些优化吗？或者你有其他想法？"
        
        return message

if __name__ == "__main__":
    optimizer = ProactiveOptimizer()
    suggestions = optimizer.generate_suggestions()
    
    if suggestions:
        print(optimizer.format_suggestion_message(suggestions))
    else:
        print("暂无优化建议，系统运行良好 ✨")
