import json
import urllib.request

url = "http://127.0.0.1:8000/tasks.json"

with urllib.request.urlopen(url, timeout=5) as response:
    print(f"状态码：{response.status}")
    print(f"内容类型：{response.headers['Content-Type']}")
    raw = response.read()
    print(f"读到的类型：{type(raw)}")
    print(f"读到的字节数：{len(raw)}")

text = raw.decode("utf-8")
print(f"解码后的类型：{type(text)}")
tasks = json.loads(text)
print(f"任务条数：{len(tasks)}")
print(f"第一条：{tasks[0]['title']}，完成状态：{tasks[0]['done']}")