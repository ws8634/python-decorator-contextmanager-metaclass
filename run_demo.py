#!/usr/bin/env python3
"""
装饰器、上下文管理器、元类实战演示入口。

运行方式:
    python run_demo.py
    或
    python -m run_demo
"""

from src.demos.demo_decorator import run_decorator_demo
from src.demos.demo_context_manager import run_context_manager_demo
from src.demos.demo_metaclass import run_metaclass_demo


def main():
    """主函数：依次运行所有演示"""
    print("=" * 60)
    print("Python 装饰器、上下文管理器、元类 实战演示")
    print("=" * 60)

    # 运行装饰器演示
    run_decorator_demo()

    # 运行上下文管理器演示
    run_context_manager_demo()

    # 运行元类演示
    run_metaclass_demo()

    print("\n" + "=" * 60)
    print("所有演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
