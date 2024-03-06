#!/bin/bash

# 获取当前脚本的文件名，不含扩展名
SCRIPT_NAME=$(basename "$0" .sh)

# 定义日志文件路径，将.sh扩展名替换为.log
LOG_FILE="${SCRIPT_NAME}.log"

# 清空或创建日志文件，准备记录新的内容
> "$LOG_FILE"

# 获取变更的文件列表
files=$(git diff --name-only)

# 遍历所有变更的文件
for file in $files; do
    # 在终端显示变更文件名，使用新格式
    echo "### ${file}"
    # 将变更文件名追加到日志文件，使用新格式
    echo "### ${file}" >> "$LOG_FILE"
    # 在终端显示空行
    echo "\n\n"

    # 显示每个文件的diff，并追加到日志文件
    git diff $file | tee -a "$LOG_FILE"
done
