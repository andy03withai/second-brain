#!/usr/bin/env python3
"""
Ace 自我进化系统 - 每周复盘报告生成器
每周日 22:00 自动生成
"""

import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict

BASE_DIR = "/root/.openclaw/workspace/second-brain"
MEMORY_DIR = f"{BASE_DIR}/memory"

def load_recent_data(days=7):
    """加载最近N天的数据"""
    errors = []
    telemetry = []
    feedback = []
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 加载错误
    for filepath in [f"{MEMORY_DIR}/errors/{(end_date.replace(day=1) - timedelta(days=i*30)).strftime('%Y-%m')}.jsonl" for i in range(2)]:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        record_date = datetime.fromisoformat(record['timestamp'])
                        if start_date <= record_date <= end_date:
                            errors.append(record)
                    except:
                        pass
    
    # 加载遥测
    for filepath in [f"{MEMORY_DIR}/telemetry/{(end_date.replace(day=1) - timedelta(days=i*30)).strftime('%Y-%m')}.jsonl" for i in range(2)]:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        record_date = datetime.fromisoformat(record['timestamp'])
                        if start_date <= record_date <= end_date:
                            telemetry.append(record)
                    except:
                        pass
    
    # 加载反馈
    for filepath in [f"{MEMORY_DIR}/feedback/{(end_date.replace(day=1) - timedelta(days=i*30)).strftime('%Y-%m')}.jsonl" for i in range(2)]:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        record_date = datetime.fromisoformat(record['timestamp'])
                        if start_date <= record_date <= end_date:
                            feedback.append(record)
                    except:
                        pass
    
    return errors, telemetry, feedback

def analyze_errors(errors):
    """分析错误"""
    if not errors:
        return {"count": 0, "by_category": {}, "top_issues": []}
    
    by_category = Counter([e.get('error_category', 'unknown') for e in errors])
    by_task = Counter([e.get('task_type', 'unknown') for e in errors])
    
    # 找出需要关注的错误（发生多次）
    top_issues = []
    for category, count in by_category.most_common(3):
        if count >= 2:
            related_errors = [e for e in errors if e.get('error_category') == category]
            lessons = [e.get('lesson', '') for e in related_errors if e.get('lesson')]
            top_issues.append({
                "category": category,
                "count": count,
                "suggestion": lessons[0] if lessons else "需要分析根因"
            })
    
    return {
        "count": len(errors),
        "by_category": dict(by_category),
        "by_task": dict(by_task),
        "top_issues": top_issues
    }

def analyze_telemetry(telemetry):
    """分析遥测数据"""
    if not telemetry:
        return {"count": 0, "success_rate": 0, "by_skill": {}}
    
    total = len(telemetry)
    success = sum(1 for t in telemetry if t.get('success', True))
    
    by_skill = defaultdict(lambda: {"count": 0, "success": 0})
    for t in telemetry:
        skill = t.get('skill_used', 'none')
        by_skill[skill]["count"] += 1
        if t.get('success', True):
            by_skill[skill]["success"] += 1
    
    # 计算每个技能的成功率
    skill_stats = {}
    for skill, stats in by_skill.items():
        skill_stats[skill] = {
            "count": stats["count"],
            "success_rate": round(stats["success"] / stats["count"] * 100, 1)
        }
    
    return {
        "count": total,
        "success_rate": round(success / total * 100, 1),
        "by_skill": skill_stats
    }

def analyze_feedback(feedback):
    """分析用户反馈"""
    if not feedback:
        return {"count": 0, "avg_rating": 0}
    
    ratings = [f.get('rating', 0) for f in feedback if f.get('rating')]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    by_task = defaultdict(list)
    for f in feedback:
        by_task[f.get('task_type', 'unknown')].append(f.get('rating', 0))
    
    task_ratings = {}
    for task, ratings in by_task.items():
        if ratings:
            task_ratings[task] = round(sum(ratings) / len(ratings), 1)
    
    return {
        "count": len(feedback),
        "avg_rating": round(avg_rating, 1),
        "by_task": task_ratings
    }

def generate_optimization_suggestions(error_analysis, telemetry_analysis):
    """生成优化建议"""
    suggestions = []
    
    # 基于错误分析
    for issue in error_analysis.get('top_issues', []):
        if issue['count'] >= 3:
            suggestions.append({
                "priority": "高",
                "area": issue['category'],
                "problem": f"本周发生{issue['count']}次",
                "suggestion": issue['suggestion'],
                "expected_impact": "减少同类错误"
            })
    
    # 基于技能成功率
    for skill, stats in telemetry_analysis.get('by_skill', {}).items():
        if stats['success_rate'] < 90 and stats['count'] >= 5:
            suggestions.append({
                "priority": "中",
                "area": skill,
                "problem": f"成功率{stats['success_rate']}%",
                "suggestion": "需要审查失败原因，增加容错机制",
                "expected_impact": "提升稳定性"
            })
    
    return suggestions

def generate_weekly_review():
    """生成每周复盘报告"""
    
    # 加载数据
    errors, telemetry, feedback = load_recent_data(days=7)
    
    # 分析
    error_analysis = analyze_errors(errors)
    telemetry_analysis = analyze_telemetry(telemetry)
    feedback_analysis = analyze_feedback(feedback)
    suggestions = generate_optimization_suggestions(error_analysis, telemetry_analysis)
    
    # 生成报告
    now = datetime.now()
    week_start = now - timedelta(days=7)
    week_str = now.strftime('%Y-W%W')
    
    report = f"""---
title: "Ace 本周复盘报告 - {week_str}"
date: {now.strftime('%Y-%m-%d')}
tags: [ace-review, weekly]
---

# 🤖 Ace 本周复盘报告 ({week_start.strftime('%m/%d')} ~ {now.strftime('%m/%d')})

## 📊 执行统计

| 指标 | 数值 |
|------|------|
| 总任务数 | {telemetry_analysis['count']} |
| 成功率 | {telemetry_analysis['success_rate']}% |
| 错误次数 | {error_analysis['count']} |
| 用户反馈 | {feedback_analysis['count']} |
| 平均满意度 | {feedback_analysis['avg_rating']}/5 |

## 🎯 技能使用分布

| 技能 | 使用次数 | 成功率 |
|------|---------|--------|
"""
    
    for skill, stats in sorted(telemetry_analysis['by_skill'].items(), key=lambda x: x[1]['count'], reverse=True)[:5]:
        report += f"| {skill} | {stats['count']} | {stats['success_rate']}% |\n"
    
    # 错误分析
    if error_analysis['count'] > 0:
        report += f"""
## ❌ 错误分析

本周共 **{error_analysis['count']}** 次错误:

"""
        for category, count in sorted(error_analysis['by_category'].items(), key=lambda x: x[1], reverse=True):
            report += f"- **{category}**: {count}次\n"
        
        if error_analysis['top_issues']:
            report += "\n### 需要关注的问题\n\n"
            for issue in error_analysis['top_issues']:
                report += f"- **{issue['category']}** ({issue['count']}次): {issue['suggestion']}\n"
    else:
        report += "\n## ✅ 错误分析\n\n本周无错误记录！🎉\n"
    
    # 用户反馈
    if feedback_analysis['by_task']:
        report += """
## 💬 用户满意度

| 任务类型 | 平均评分 |
|----------|----------|
"""
        for task, rating in sorted(feedback_analysis['by_task'].items(), key=lambda x: x[1], reverse=True):
            report += f"| {task} | {rating}/5 |\n"
    
    # 优化建议
    if suggestions:
        report += """
## 💡 优化建议

"""
        for i, sug in enumerate(suggestions, 1):
            report += f"""### {i}. [{sug['priority']}优先级] {sug['area']}
- **问题**: {sug['problem']}
- **建议**: {sug['suggestion']}
- **预期收益**: {sug['expected_impact']}

"""
    
    report += f"""
---

*本报告由 Ace 自我进化系统自动生成*
*数据周期: {week_start.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}*
*如需调整复盘内容，请告诉我*
"""
    
    # 保存报告
    report_path = f"{MEMORY_DIR}/reviews/{week_str}.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 同时放入input目录，可被第二大脑收录 (使用 index.md 格式以便 Hugo 生成页面)
    input_dir = f"{BASE_DIR}/content/input/ace-reviews/{week_str}"
    os.makedirs(input_dir, exist_ok=True)
    input_path = f"{input_dir}/index.md"
    
    with open(input_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 复盘报告已生成: {report_path}")
    print(f"✅ 已同步到: {input_path}")
    return report_path, report

if __name__ == "__main__":
    path, content = generate_weekly_review()
    print("\n" + "="*50)
    print(content[:1000] + "...")
