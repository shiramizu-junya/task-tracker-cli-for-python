#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    """
    タスクをJSONファイルから読み込む関数。
    ファイルが存在しない場合は空のタスクリストを返す。
    例外が発生した場合はエラーメッセージを標準エラー出力に表示し、空のタスクリストを返す。
    返り値: { "tasks": [...] }
    """
    try:
        # 1. ファイルが存在しない場合は {"tasks": []} を返す
        if not os.path.exists(TASKS_FILE):
            return { "tasks": [] }

        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading tasks: {e}", file=sys.stderr)
        return { "tasks": [] }

def save_tasks(data):
    """
    タスクをJSONファイルに保存する関数。
    例外が発生した場合はエラーメッセージを標準エラー出力に表示する。
    引数:
        data: { "tasks": [...] }
    """
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving tasks: {e}", file=sys.stderr)

def get_next_id(tasks):
    """
    タスクのリストから次に使用するIDを取得する関数。
    タスクが存在しない場合は1を返す。
    引数:
        tasks: タスクのリスト
    返り値: 次に使用するID (整数)
    """
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

def get_timestamp():
    """
    現在の日時をISO 8601形式で取得する関数。
    返り値: 現在の日時 (文字列)
    """
    return datetime.now().isoformat()

def add_task(description):
    """
    新しいタスクを追加する関数。
    引数:
        description: タスクの説明 (文字列)
    """
    data = load_tasks()
    new_id = get_next_id(data['tasks'])
    now = get_timestamp()

    new_task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'createdAt': now,
        'updatedAt': now,
    }

    data['tasks'].append(new_task)
    save_tasks(data)
    print(f"Task added successfully (ID: {new_id})")

def main():
    if len(sys.argv) != 3:
        print("Usage: task_cli.py <command> <task_description>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    task_description = sys.argv[2]

    if command == 'add':
        add_task(task_description)

if __name__ == '__main__':
    main()
