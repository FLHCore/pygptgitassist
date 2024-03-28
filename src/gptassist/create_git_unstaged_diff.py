import os
import subprocess
import click
import dotenv
from openai import OpenAI
from gptassist.create_git_pr_diff_for_gpt import calculate_line_count

dotenv.load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY", '')


def _chat_with_gpt(total_diff: str) -> str:
    client = OpenAI(
        api_key=openai_api_key
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "请根据以下git diff输出，生成一个符合Conventional Commits规范的commit message。"
            },
            {
                "role": "user",
                "content": f"git diff输出内容：\n\n{total_diff}"
            },
            {
                "role": "system",
                "content": "分析diff输出，理解代码变更的主要内容和目的。根据Conventional Commits规范，确定合适的type、[optional scope]和description。生成建议的commit message。"
            }
        ]
        ,
        model="gpt-4",
    )
    # print(chat_completion)
    return chat_completion.choices[0].message.content


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
            line_count = calculate_line_count(file, '.')
            proc = subprocess.Popen(['git', 'diff', f'-U{line_count}', '--', file],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            diff_output = stdout.decode()

            click.echo(diff_output)  # 使用click.echo显示diff结果

            with open(log_path, 'a') as log_file:
                log_file.write(diff_output)

    if openai_api_key:
        with open(log_path, 'r') as f:
            total_diff = f.read()
        commit_message = _chat_with_gpt(total_diff)
        click.echo(commit_message)


if __name__ == '__main__':
    log_git_changes()
