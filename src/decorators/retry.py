import time
import functools
from typing import Callable, Type, Tuple, Union, Optional, Any


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
) -> Callable:
    """
    一个参数可配置的重试装饰器。

    用途：在调用可能失败的函数时，自动重试指定次数，每次重试之间有固定退避延迟。
    常见场景：网络请求、数据库操作、外部API调用等可能因不稳定的操作。

    特点：
    1. 使用 functools.wraps 保持被装饰函数的元信息
    2. 可配置重试次数、退避延迟、捕获的异常类型
    3. 支持普通函数和异步函数的支持说明：
       - 本装饰器默认只支持普通同步函数
       - 如果要支持异步函数，需要使用 asyncio 并检测 coroutine 函数
       - 异步版本需要额外使用 async 版本需要额外处理：检查函数的

    参数:
        max_attempts: 最大尝试次数（包括首次调用）
        delay: 每次重试之间的延迟时间（秒）
        exceptions: 需要捕获并重试的异常类型，默认为 Exception

    示例:
        @retry(max_attempts=3, delay=0.5)
        def fetch_data():
            # 可能失败的操作
            pass
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[Exception] = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"[retry] 第 {attempt + 1} 次尝试失败，{type(e).__name__}: {e}，"
                              f"等待 {delay} 秒后重试...")
                        time.sleep(delay)

            # 最后一次尝试后仍然失败，重新抛出异常
            print(f"[retry] 所有 {max_attempts} 次尝试均失败，最后一次错误: "
                  f"{type(last_exception).__name__}: {last_exception}")
            raise last_exception

        return wrapper

    return decorator
