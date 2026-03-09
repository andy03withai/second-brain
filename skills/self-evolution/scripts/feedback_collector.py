#!/usr/bin/env python3
"""
Ace 自我进化系统 - 满意度收集
在合适时机主动询问用户反馈
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/second-brain/skills/self-evolution/scripts')
from tracker import log_feedback

def ask_for_feedback(task_type, task_description=""):
    """
    请求用户反馈
    这个函数在需要收集反馈时调用，返回要展示给用户的消息
    """
    message = f"""
💭 快速反馈

刚才的 {task_type} 任务完成啦！

花2秒打个分？
👍 满意  /  👎 不满意

或者简单说两句哪里好/哪里需要改进
"""
    return message

def process_feedback(task_type, rating, comment="", user_id="default"):
    """处理用户反馈"""
    log_feedback(
        task_type=task_type,
        rating=rating,  # 1-5或👍=5, 👎=1
        comment=comment,
        user_id=user_id
    )
    return "感谢反馈！这会帮助我变得更好 ✨"

# 使用场景示例
if __name__ == "__main__":
    # 模拟：任务完成后请求反馈
    print(ask_for_feedback("daily-brief", "生成了5个主题的简报"))
    
    # 模拟：用户给了反馈
    print(process_feedback("daily-brief", 5, "今天的内容很相关"))
