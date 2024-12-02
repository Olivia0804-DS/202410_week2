# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# 定义不同角色的系统提示
ROLE_PROMPTS = {
    "Customer Support Specialist": {
        "role": "system",
        "content": """You are a Customer Support Specialist. you need to:
        1.Address customer inquiries about NGS services, pricing, and turnaround time.
        2.Provide FAQs, guide users to appropriate resources or departments, and explain service processes.
        """
    },
    "Technical Assistant": {
        "role": "system",
        "content": """you are a Technical Assistant. you need:
        1. Assist researchers or clients with technical questions related to NGS workflows, protocols, or troubleshooting.
        2. Explain sample preparation steps, sequencing methods, or data analysis details.
        2. 提供实用的产品示例
        3. 解释潜在的性能影响
        4. 分享最佳实践和设计模式
        5. 提到可能遇到的常见陷阱
        6. 推荐相关的技术文档和资源
        7. 讨论不同方案的优劣"""
    },
    "Service Advisor": {
        "role": "system",
        "content": """you are a Service Advisor. you need to：
        1. Guide customers on selecting appropriate NGS services based on their research needs.
        2. Recommend services, explain the benefits of PTA-based whole genome amplification, and clarify differences between WGS and RNA sequencing.
        3. 强调问题解决的思路
        4. 保持学术性的表达方式"""
    }
}

@app.route('/chat/<role>', methods=['POST'])
def chat(role):
    try:
        if role not in ROLE_PROMPTS:
            return jsonify({'error': 'Invalid role'}), 400
        
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # 构建包含角色设定的消息列表
        messages = [
            ROLE_PROMPTS[role],  # 系统角色设定
            {
                "role": "user",
                "content": message
            }
        ]
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        return jsonify({
            'role': role,
            'response': completion.choices[0].message.content
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)