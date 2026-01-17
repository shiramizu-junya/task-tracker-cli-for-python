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
    例外が発生した場合はエラーメッセージを標準エラー出力に表示し、例外を再送出する。
    引数:
        data: { "tasks": [...] }
    例外:
        IOError: ファイルの書き込みに失敗した場合
    """
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving tasks: {e}", file=sys.stderr)
        raise

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
    try:
        save_tasks(data)
        print(f"Task added successfully (ID: {new_id})")
    except IOError:
        sys.exit(1)

def list_tasks(status_filter=None):
    """
    タスクを一覧表示する関数。
    引数:
        status_filter: フィルタリングするステータス (文字列、オプション)
    """
    data = load_tasks()
    tasks = data['tasks']

    if status_filter:
        tasks = [task for task in tasks if task['status'] == status_filter]

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, CreatedAt: {task['createdAt']}, UpdatedAt: {task['updatedAt']}")

def update_task(task_id, description):
    """
    既存のタスクを更新する関数。
    引数:
        task_id: 更新するタスクのID (整数)
        description: 新しいタスクの説明 (文字列)
    """
    data = load_tasks()
    tasks = data['tasks']

    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updatedAt'] = get_timestamp()
            try:
                save_tasks(data)
                print(f'Task {task_id} updated successfully')
            except IOError:
                sys.exit(1)
            return

    print(f"Error: Task with ID {task_id} not found", file=sys.stderr)
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: task_cli.py <command> [<args>]")
        print("Commands:")
        print("  add <description>    Add a new task")
        print("  list [<status>]      List tasks, optionally filtered by status")
        print("  update <task_id> <description>  Update an existing task")
        return

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 3:
            print("Usage: task_cli.py add <description>")
            return
        description = " ".join(sys.argv[2:])
        add_task(description)
    elif command == 'list':
        status_filter = sys.argv[2] if len(sys.argv) >= 3 else None
        list_tasks(status_filter)
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Usage: task_cli.py update <task_id> <description>")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: ID must be a number")
            return

        description = " ".join(sys.argv[3:])
        update_task(task_id, description)
    else:
        print(f"Unknown command: {command}")

if __name__ == '__main__':
    main()
