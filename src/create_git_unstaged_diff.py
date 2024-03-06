import os
import subprocess
import click


@click.command()
@click.option('--log-path', default=None,
              help='Custom log file path. If not provided, will use the script name with .log extension.')
def log_git_changes(log_path):
    """
    This CLI tool logs the git changed files and their diffs to a log file.
    """
    script_name = os.path.splitext(os.path.basename(__file__))[0]

    # 如果用户没有指定日志文件路径，则使用默认的路径
    if not log_path:
        log_path = f"{script_name}.log"

    # 清空或创建日志文件，准备记录新的内容
    with open(log_path, 'w') as log_file:
        pass  # 打开文件后立即关闭，等同于清空或创建文件

    # 获取变更的文件列表
    proc = subprocess.Popen(['git', 'diff', '--name-only'], stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    files = stdout.decode().strip().split('\n')

    # 遍历所有变更的文件
    for file in files:
        if file:  # 确保文件名非空
            # 使用click.echo在终端显示变更文件名，使用新格式
            click.echo(f"### {file}")

            # 将变更文件名追加到日志文件，使用新格式
            with open(log_path, 'a') as log_file:
                log_file.write(f"### {file}\n")

            # 显示每个文件的diff，并追加到日志文件
            proc = subprocess.Popen(['git', 'diff', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            diff_output = stdout.decode()

            click.echo(diff_output)  # 使用click.echo显示diff结果

            with open(log_path, 'a') as log_file:
                log_file.write(diff_output)


if __name__ == '__main__':
    log_git_changes()
