import os
from contextlib import contextmanager
from typing import Dict, Optional, Iterator


@contextmanager
def temp_env(env_vars: Dict[str, Optional[str]]) -> Iterator[None]:
    """
    临时修改环境变量的上下文管理器。

    用途：在代码块执行期间临时设置或删除环境变量，
         退出代码块时自动恢复原来的环境变量状态。

    场景：
    - 测试代码中需要特定环境变量的场景
    - 需要隔离不同模块对环境变量的依赖
    - 模拟特定环境下的行为

    工作原理：
    - 进入时（__enter__）：保存当前环境变量值，设置新值
    - 退出时（__exit__）：恢复保存的环境变量值

    异常处理说明：
    1. 如果进入时（__enter__）失败：
       - 通常是指在 yield 之前的代码抛出异常
       - 此时还没有保存原始状态，或者只保存了部分
       - 在本实现中，如果在 __enter__ 阶段失败，不会有清理
       - 实际使用时，如果 __enter__ 失败，通常不会执行 __exit__

    2. 如果代码块内部抛出异常：
       - @contextmanager 会确保 __exit__ 逻辑（yield 之后的代码）被执行
       - 即使代码块抛出异常，我们仍然会恢复环境变量
       - 这是 @contextmanager 的核心特性：无论如何都保证清理

    参数:
        env_vars: 字典，键是环境变量名，值是要设置的新值。
                  如果值为 None，则表示删除该环境变量。

    示例:
        with temp_env({'DEBUG': 'true', 'API_KEY': None}):
            # 在此代码块中，DEBUG='true'，且 API_KEY 被删除
            pass
        # 离开代码块后，环境变量恢复原值
    """
    original_values: Dict[str, Optional[str]] = {}

    # __enter__ 阶段：保存原值并设置新值
    for key, new_value in env_vars.items():
        original_values[key] = os.environ.get(key)
        if new_value is None:
            # 删除环境变量
            if key in os.environ:
                del os.environ[key]
        else:
            # 设置新值
            os.environ[key] = new_value

    try:
        # 进入代码块
        yield
    finally:
        # __exit__ 阶段：恢复原始值（无论是否有异常都会执行）
        for key, original_value in original_values.items():
            if original_value is None:
                # 原来不存在，现在删除
                if key in os.environ:
                    del os.environ[key]
            else:
                # 原来存在，恢复原值
                os.environ[key] = original_value
