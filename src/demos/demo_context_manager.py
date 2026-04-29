import os
from src.context_managers.temp_env import temp_env


def run_context_manager_demo():
    """
    运行上下文管理器演示。

    展示正常路径和异常路径下的上下文管理器行为。
    """
    print("\n" + "=" * 60)
    print("演示 2: 临时环境变量上下文管理器")
    print("=" * 60)

    print("\n[准备] 初始环境变量状态")
    print("-" * 40)
    original_debug = os.environ.get('DEBUG')
    original_test_var = os.environ.get('TEST_VAR')
    print(f"  DEBUG = {original_debug}")
    print(f"  TEST_VAR = {original_test_var}")

    print("\n[场景 1] 正常路径：设置临时环境变量")
    print("-" * 40)

    print(f"  [进入前] DEBUG = {os.environ.get('DEBUG')}, TEST_VAR = {os.environ.get('TEST_VAR')}")

    with temp_env({'DEBUG': 'true', 'TEST_VAR': 'hello'}):
        print(f"  [代码块内] DEBUG = {os.environ.get('DEBUG')}, TEST_VAR = {os.environ.get('TEST_VAR')}")

    print(f"  [退出后] DEBUG = {os.environ.get('DEBUG')}, TEST_VAR = {os.environ.get('TEST_VAR')}")

    print("\n[场景 2] 异常路径：代码块内抛出异常")
    print("-" * 40)

    print(f"  [进入前] DEBUG = {os.environ.get('DEBUG')}")

    try:
        with temp_env({'DEBUG': 'false'}):
            print(f"  [代码块内] DEBUG = {os.environ.get('DEBUG')}")
            print("  [代码块内] 现在抛出异常...")
            raise RuntimeError("测试异常")
    except RuntimeError as e:
        print(f"  捕获到异常: {e}")

    print(f"  [异常后] DEBUG = {os.environ.get('DEBUG')} (已恢复)")

    print("\n[场景 3] 删除临时环境变量（设置为 None）")
    print("-" * 40)

    # 先设置一个环境变量
    os.environ['TEMP_DELETE'] = 'to_be_deleted'
    print(f"  [进入前] TEMP_DELETE = {os.environ.get('TEMP_DELETE')}")

    with temp_env({'TEMP_DELETE': None}):
        print(f"  [代码块内] TEMP_DELETE = {os.environ.get('TEMP_DELETE')} (已删除)")

    print(f"  [退出后] TEMP_DELETE = {os.environ.get('TEMP_DELETE')} (已恢复)")

    # 清理
    if 'TEMP_DELETE' in os.environ:
        del os.environ['TEMP_DELETE']

    print("\n" + "=" * 60)
    print("说明：无论代码块内是否抛出异常，环境变量都会被恢复")
    print("这是通过 try-finally 机制保证的")
    print("=" * 60)
