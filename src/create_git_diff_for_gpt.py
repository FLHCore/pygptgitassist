import os
import subprocess
import click


def calculate_line_count(filename, commit_id_start, commit_id_end, repo_path):
    """计算文件在两个提交之间的最大变更行数"""
    diff_output = subprocess.run(['git', 'diff', f'{commit_id_start}^', commit_id_end, '--', filename],
                                 capture_output=True, text=True, cwd=repo_path).stdout
    # 简化计算：使用diff输出的行数作为上下文行数
    return max(3, len(diff_output.splitlines()))  # 至少使用3行作为上下文


@click.command()
@click.argument('commit_id_start')
@click.argument('commit_id_end')
@click.option('--repo_path', default='.', help='Path to the Git repository.')
def main(commit_id_start, commit_id_end, repo_path):
    """Generates and accumulates git diff outputs between two commits into individual and total diff files."""
    gitdiff_dir = os.path.join(repo_path, '.gitdiff')

    if os.path.exists(gitdiff_dir):
        subprocess.run(['rm', '-rf', gitdiff_dir], check=True)

    os.makedirs(gitdiff_dir)
    total_diff_file = os.path.join(gitdiff_dir, 'total.git_diff')
    open(total_diff_file, 'w').close()  # 创建或清空 total.git_diff 文件

    changed_files = subprocess.run(['git', 'diff', '--name-only', f'{commit_id_start}^', commit_id_end],
                                   capture_output=True, text=True, cwd=repo_path).stdout.splitlines()

    for filename in changed_files:
        safe_filename = filename.replace('/', '.')
        individual_diff_file = os.path.join(gitdiff_dir, f'{safe_filename}.git_diff')
        line_count = calculate_line_count(filename, commit_id_start, commit_id_end, repo_path)

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
