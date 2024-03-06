# GPT Git Assistant CLI
Your SW Git Repository CLI Tool for GPT Assistant

## Installation or Upgrade

```sh
pip install --upgrade https://github.com:FLHCore/pygptgitassist/releases/download/0.0.1/pygptgitassist-0.0.1-py3-none-any.whl
```

# create-git-diff CLI

`create-git-diff` 是一個 CLI 工具，用於創建 git 差異。它是使用 Python 和 click 庫構建的。

## 使用

```bash
create-git-diff [OPTIONS] COMMIT_ID_START COMMIT_ID_END
```

Usage: create-git-diff [OPTIONS] COMMIT_ID_START COMMIT_ID_END

  Generates and accumulates git diff outputs between two commits into
  individual and total diff files.

Options:
  --repo_path TEXT  Path to the Git repository.
  --help            Show this message and exit.

## 範例

以下是一個使用 `create-git-diff` 的範例：

```bash
create-git-diff abc123 def456 
```

這將會生成從 `abc123` 提交到 `def456` 提交的 git 差異，並將結果存儲在 `/path/to/repo/.gitdiff` 目錄中。