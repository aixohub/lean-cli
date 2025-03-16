
from lean.commands import lean

import logging



logging.basicConfig(level=logging.DEBUG)


def run_lean_live(project_path: str):
    args = ["live", project_path]

    # 调用 lean 命令
    try:
        lean.main(args=args)
    except SystemExit as e:
        # 捕获 SystemExit 异常（click 命令执行完毕后会抛出）
        if e.code != 0:
            print(f"Command failed with exit code: {e.code}")
        else:
            print("Command executed successfully.")

# 调用函数

def run_lean_project_create(project_path: str):
    args = ["project-create", project_path]

    # 调用 lean 命令
    try:
        lean.main(args=args)
    except SystemExit as e:
        # 捕获 SystemExit 异常（click 命令执行完毕后会抛出）
        if e.code != 0:
            print(f"Command failed with exit code: {e.code}")
        else:
            print("Command executed successfully.")


if __name__ == "__main__":
   # run_lean_live("/Users/jupyter/work/code/github/lean-cli/trade")
   run_lean_project_create("stock-nvda")
