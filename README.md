# Task Tracker CLI

シンプルなコマンドラインタスク管理ツール
https://roadmap.sh/projects/task-tracker

## 必要環境

- Python 3.x

## インストール方法

```bash
git clone https://github.com/shiramizu-junya/task-tracker-cli-for-python.git
cd task-tracker-cli-for-python
```

## 使用方法

### ヘルプの表示

```bash
python task_cli.py
```

### タスクの追加

```bash
python task_cli.py add "Buy groceries"
# Task added successfully (ID: 1)
```

### タスクの一覧表示

```bash
# 全タスクを表示
python task_cli.py list

# ステータスでフィルタリング
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

### タスクの更新

```bash
python task_cli.py update 1 "Buy groceries and cook dinner"
# Task 1 updated successfully
```

### タスクのステータス変更

```bash
# 進行中に変更
python task_cli.py mark-in-progress 1
# Task 1 marked as in-progress successfully

# 完了に変更
python task_cli.py mark-done 1
# Task 1 marked as done successfully
```

### タスクの削除

```bash
python task_cli.py delete 1
# Task 1 deleted successfully
```

## タスクデータの構造

タスクは `tasks.json` ファイルに保存されます。

```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "status": "todo",
      "createdAt": "2026-01-17T10:00:00.000000",
      "updatedAt": "2026-01-17T10:00:00.000000"
    }
  ]
}
```

### ステータス

| ステータス | 説明 |
|-----------|------|
| `todo` | 未着手 |
| `in-progress` | 進行中 |
| `done` | 完了 |
