# Stream-HTML

一个模拟LLM流式生成HTML内容的演示项目。

## 项目结构

- `mock_server.py`: 模拟LLM服务器
  - 实现了类似ChatGPT的流式响应接口
  - 按单词级别流式生成`example.html`的内容
  - 支持中英文标点符号的正确处理

- `test.py`: API测试工具
  - 用于验证mock服务器的输出
  - 测试流式响应的正确性

- `server.py`: HTML预览服务器
  - 用于运行和预览`example.html`
  - 提供实时的页面渲染效果

- `example.html`: 演示页面
  - 集成了霞鹜文楷字体
  - 用于展示流式生成的内容

## 运行方式

1. 启动模拟LLM服务器：
```bash
python mock_server.py
```

2. 运行HTML预览服务器：
```bash
python server.py
```

3. 测试API响应（可选）：
```bash
python test.py