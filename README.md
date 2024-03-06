# GPT Git Assistant CLI
Your SW Git Repository CLI Tool for GPT Assistant

## Installation or Upgrade

```bash
pip install --upgrade https://github.com/FLHCore/pygptgitassist/releases/download/0.0.1/gptgitassist-0.0.1-py3-none-any.whl
```

# create-git-pr-diff

```bash
Usage: create-git-pr-diff [OPTIONS] COMMIT_ID_START COMMIT_ID_END

  Generates and accumulates git diff outputs between two commits into
  individual and total diff files.

Options:
  --repo_path TEXT  Path to the Git repository.
  --help            Show this message and exit.
```

旨在幫助用戶生成Git倉庫中兩個commit之間的差異，並將差異信息保存到文件中，以便進一步分析和審查。

- 為每個變更的文件生成一個包含差異信息的單獨文件。
- 將所有文件的差異信息匯總到一個總文件中。

執行腳本後，會在 Git 倉庫的當前目錄下生成一個 `.gitdiff` 隱藏目錄（建議將 `.gitdiff` 加入 `.gitignore` 設定中），裡面包含了以下文件：

1. 單個文件差異：每個變更過的文件都會有一個對應的 `{safe_filename}.git_diff` 文件，其中`{safe_filename}`是原始文件名，將 `/` 替換為 `.` 。
2. 總差異文件：名為 `total.git_diff` 的文件，包含了所有變更文件的差異信息。
