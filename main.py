"""Python 基础综合项目：仅使用标准库，Python 3.12+。"""
import json
from pathlib import Path


def validate_tasks(value):
    if not isinstance(value, list):
        raise ValueError("任务数据必须是列表")
    ids = set()
    for task in value:
        if not isinstance(task, dict):
            raise ValueError("每条任务必须是对象")
        task_id = task.get("id")
        title = task.get("title")
        if type(task_id) is not int or task_id <= 0 or task_id in ids:
            raise ValueError("任务编号必须为不重复的正整数")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("任务名称不能为空")
        if type(task.get("done")) is not bool:
            raise ValueError("完成状态必须为布尔值")
        ids.add(task_id)
    return value


def load_tasks(path):
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError("任务文件不是有效 JSON，请检查原文件") from error
    return validate_tasks(value)


def save_tasks(path, tasks):
    validate_tasks(tasks)
    # 先完整写入临时文件，再替换；写入失败时保留上一份正式文件。
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def add_task(tasks, title):
    title = title.strip()
    if not title:
        raise ValueError("任务名称不能为空")
    task_id = max((task["id"] for task in tasks), default=0) + 1
    tasks.append({"id": task_id, "title": title, "done": False})
    return task_id


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise ValueError("任务不存在")


def complete_task(tasks, task_id):
    find_task(tasks, task_id)["done"] = True


def delete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    tasks.remove(task)


def show_tasks(tasks):
    if not tasks:
        print("暂无任务")
    for task in tasks:
        status = "已完成" if task["done"] else "待完成"
        print(f"{task['id']}. {task['title']} [{status}]")


def read_id():
    text = input("任务编号：")
    try:
        value = int(text)
    except ValueError as error:
        raise ValueError("任务编号必须为正整数") from error
    if value <= 0:
        raise ValueError("任务编号必须为正整数")
    return value


def main():
    path = Path(__file__).resolve().parent / "tasks.json"
    try:
        tasks = load_tasks(path)
    except (ValueError, OSError, UnicodeError) as error:
        print(f"无法加载：{error}")
        return 1
    print("命令：add / list / done / delete / quit")
    while True:
        try:
            command = input("命令：").strip().lower()
            if command == "quit":
                print("再见")
                return 0
            if command == "list":
                show_tasks(tasks)
                continue
            # 修改副本，保存成功后才更新当前内存状态。
            changed = [task.copy() for task in tasks]
            if command == "add":
                task_id = add_task(changed, input("任务名称："))
                message = f"已添加：{task_id}"
            elif command == "done":
                complete_task(changed, read_id())
                message = "已完成"
            elif command == "delete":
                delete_task(changed, read_id())
                message = "已删除"
            else:
                print("未知命令")
                continue
            save_tasks(path, changed)
            tasks = changed
            print(message)
        except (OSError, UnicodeError) as error:
            print(f"保存失败：{error}")
        except ValueError as error:
            print(error)
        except (EOFError, KeyboardInterrupt):
            print("\n再见")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())