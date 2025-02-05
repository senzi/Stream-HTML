from flask import Flask, Response
import json
import time
import uuid
import re

app = Flask(__name__)

def generate_sse_data(content):
    # 生成初始角色信息
    initial_data = {
        "id": f"cmpl-{uuid.uuid4().hex}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "mock-llm-v1",
        "choices": [{
            "index": 0,
            "delta": {
                "role": "assistant",
                "content": ""
            },
            "finish_reason": None
        }]
    }
    yield f"data: {json.dumps(initial_data)}\n\n"
    
    # 使用正则表达式分割文本为单词和标点
    # \w+ 匹配单词, [.,!?;:，。！？；：]* 匹配可能跟随的标点符号
    # \s+ 匹配空白字符
    pattern = r'(\w+[.,!?;:，。！？；：]*|\s+)'
    words = re.findall(pattern, content)
    
    for word in words:
        chunk_data = {
            "id": f"cmpl-{uuid.uuid4().hex}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "mock-llm-v1",
            "choices": [{
                "index": 0,
                "delta": {
                    "content": word
                },
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(chunk_data)}\n\n"
        time.sleep(0.01)  # 模拟生成延迟
    
    # 生成结束标记
    final_data = {
        "id": f"cmpl-{uuid.uuid4().hex}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "mock-llm-v1",
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": len(content),
                "total_tokens": len(content) + 10
            }
        }]
    }
    yield f"data: {json.dumps(final_data)}\n\n"
    yield "data: [DONE]\n\n"

@app.route('/v1/chat/completions', methods=['POST'])
def stream_response():
    try:
        with open('example.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Example Page</title>
</head>
<body>
    <h1>Hello World</h1>
    <p>This is a fallback example.</p>
</body>
</html>
"""

    return Response(
        generate_sse_data(html_content),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)