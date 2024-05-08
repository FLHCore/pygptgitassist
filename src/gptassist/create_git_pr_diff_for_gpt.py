import os
import subprocess
import click
import dotenv

dotenv.load_dotenv()
OUTPUT_PATH = os.getenv("OUTPUT_PATH", 'build')


def calculate_line_count(filename, repo_path):
    """计算文件的行数"""
    result = subprocess.run(['wc', '-l', filename], capture_output=True, text=True, cwd=repo_path)
    line_count = int(result.stdout.split()[0])
    return line_count


@click.command()
@click.argument('commit_id_start')
@click.argument('commit_id_end')
@click.option('--repo_path', default='.', help='Path to the Git repository.')
@click.option('-o', '--output-path', default=OUTPUT_PATH, help='Path to the output directory.')
def main(commit_id_start, commit_id_end, repo_path, output_path):
    """Generates and accumulates git diff outputs between two commits into individual and total diff files."""
    output_path = f'{os.path.join(repo_path, output_path)}'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    total_diff_file = os.path.join(output_path, 'total.git_diff')
    open(total_diff_file, 'w').close()  # 创建或清空 total.git_diff 文件

    changed_files = subprocess.run(['git', 'diff', '--name-only', f'{commit_id_start}^', commit_id_end],
                                   capture_output=True, text=True, cwd=repo_path).stdout.splitlines()

    for filename in changed_files:
        safe_filename = filename.replace('/', '.')
        individual_diff_file = os.path.join(output_path, f'{safe_filename}.git_diff')
        line_count = calculate_line_count(filename, repo_path)

        with open(individual_diff_file, 'w') as f:
            subprocess.run(['git', 'diff', f'-U{line_count}', f'{commit_id_start}^', commit_id_end, '--', filename],
                           stdout=f, cwd=repo_path)

        print(f'Generated diff for {filename} with context lines: {line_count} in {individual_diff_file}')

        with open(total_diff_file, 'a') as f:
            f.write(f"---- {filename} ----\n")
            with open(individual_diff_file, 'r') as individual_f:
                f.writelines(individual_f.readlines())


if __name__ == '__main__':
    main()
