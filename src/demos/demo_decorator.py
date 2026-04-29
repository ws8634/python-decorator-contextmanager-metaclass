from src.decorators.retry import retry


def run_decorator_demo():
    """
    运行装饰器演示。

    展示正常路径和异常路径下的装饰器行为。
    """
    print("=" * 60)
    print("演示 1: 参数可配置的重试装饰器")
    print("=" * 60)

    print("\n[场景 1] 函数首次调用就成功（正常路径）")
    print("-" * 40)

    call_count = 0

    @retry(max_attempts=3, delay=0.1)
    def always_succeeds():
        """一个总是成功的函数"""
        nonlocal call_count
        call_count += 1
        print(f"  [always_succeeds] 第 {call_count} 次调用，返回 'success'")
        return "success"

    result = always_succeeds()
    print(f"  最终结果: {result}")
    print(f"  函数名称保持: {always_succeeds.__name__}")
    print(f"  文档字符串保持: {always_succeeds.__doc__}")

    print("\n[场景 2] 函数前两次失败，第三次成功（重试成功）")
    print("-" * 40)

    call_count_2 = 0

    @retry(max_attempts=3, delay=0.1)
    def succeeds_on_third():
        """一个在第三次调用时才成功的函数"""
        nonlocal call_count_2
        call_count_2 += 1
        if call_count_2 < 3:
            print(f"  [succeeds_on_third] 第 {call_count_2} 次调用，抛出 ValueError")
            raise ValueError(f"第 {call_count_2} 次调用失败")
        print(f"  [succeeds_on_third] 第 {call_count_2} 次调用，返回 'ok'")
        return "ok"

    try:
        result_2 = succeeds_on_third()
        print(f"  最终结果: {result_2}")
    except ValueError as e:
        print(f"  最终抛出异常: {e}")

    print("\n[场景 3] 函数所有尝试都失败（异常路径）")
    print("-" * 40)

    @retry(max_attempts=3, delay=0.1, exceptions=(ValueError,))
    def always_fails():
        """一个总是失败的函数"""
        print("  [always_fails] 调用，抛出 ValueError")
        raise ValueError("始终失败")

    try:
        always_fails()
    except ValueError as e:
        print(f"  最终抛出异常: {e}")

    print("\n" + "=" * 60)
