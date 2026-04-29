# 装饰器、上下文管理器、元类实战

本项目展示了 Python 中三个高级特性在工程项目中的常见用法：装饰器、上下文管理器和元类。

## 快速开始

在项目根目录下运行：

```bash
python run_demo.py
```

或

```bash
python -m run_demo
```

## 项目要求

分别说明装饰器、上下文管理器、元类的核心应用场景，举例三者在工程项目中的落地实践。

## 核心要点

### 1. 装饰器（Decorator）核心应用场景

**解决的问题：** 在不修改原有函数代码的前提下，增强函数的行为（如日志记录、性能统计、重试逻辑、权限检查等）。

**本示例体现：** 参数可配置的重试装饰器 `retry`，用于处理可能失败的操作（如网络请求、数据库操作）。

**核心特性：**
- 使用 `functools.wraps` 保持被装饰函数的 `__name__`、`__doc__` 等元信息
- 可配置：重试次数 `max_attempts`、退避延迟 `delay`、捕获异常类型 `exceptions`
- 支持普通函数；若需支持异步函数，需额外检测 `async def` 并使用 `asyncio.sleep`

**实现文件：** [src/decorators/retry.py](src/decorators/retry.py)

---

### 2. 上下文管理器（Context Manager）核心应用场景

**解决的问题：** 管理资源的获取和释放，确保无论代码块是否抛出异常，资源都能被正确清理。常见于文件操作、数据库连接、锁管理、临时状态修改等场景。

**本示例体现：** 使用 `@contextmanager` 实现的临时环境变量上下文管理器 `temp_env`，用于在代码块内临时修改环境变量，退出时自动恢复。

**异常处理说明：**
1. **进入时（__enter__）失败：** 如果在 `yield` 之前的代码抛出异常，不会执行 `__exit__` 逻辑。在本实现中，如果保存原值时失败，不会有清理操作。

2. **代码块内抛出异常：** `@contextmanager` 使用 `try-finally` 机制，确保 `yield` 之后的代码（即 `__exit__` 逻辑）无论是否有异常都会执行。这意味着即使代码块抛出异常，环境变量仍然会被恢复。

**实现文件：** [src/context_managers/temp_env.py](src/context_managers/temp_env.py)

---

### 3. 元类（Metaclass）核心应用场景

**解决的问题：** 控制类的创建过程。在类定义时（而非实例创建时）执行特定逻辑，如自动注册子类、约束子类行为、注入类属性等。

**与装饰器和上下文管理器的区别：**
- **装饰器：** 运行时增强函数/方法的行为（函数调用层面）
- **上下文管理器：** 管理资源的获取和释放（资源生命周期层面）
- **元类：** 控制类的创建过程（类定义层面）

**本示例体现：** 自动注册子类的元类 `RegistryMeta`，所有继承基类的子类会自动注册到全局注册表，适用于插件系统、工厂模式、策略模式等场景。

**使用方式：**
1. 定义基类时使用 `metaclass=RegistryMeta`
2. 在基类中定义 `registry_name` 类属性指定注册表名称
3. 所有子类自动注册，可通过 `get_registry(registry_name)` 获取

**实现文件：** [src/metaclasses/registry.py](src/metaclasses/registry.py)

---

## 参考实现

### 项目结构

```
.
├── run_demo.py              # 统一演示入口
├── README.md                # 本文档
└── src/
    ├── __init__.py
    ├── decorators/
    │   ├── __init__.py
    │   └── retry.py         # 重试装饰器
    ├── context_managers/
    │   ├── __init__.py
    │   └── temp_env.py      # 临时环境变量上下文管理器
    ├── metaclasses/
    │   ├── __init__.py
    │   └── registry.py      # 自动注册子类的元类
    └── demos/
        ├── __init__.py
        ├── demo_decorator.py        # 装饰器演示
        ├── demo_context_manager.py  # 上下文管理器演示
        └── demo_metaclass.py        # 元类演示
```

### 入口命令

**一次性运行所有演示：**
```bash
python run_demo.py
```

**单独运行各模块示例：**

装饰器：
```python
from src.decorators.retry import retry

@retry(max_attempts=3, delay=1.0)
def unstable_operation():
    pass
```

上下文管理器：
```python
from src.context_managers.temp_env import temp_env

with temp_env({'DEBUG': 'true'}):
    # 临时环境变量生效
    pass
# 离开后自动恢复
```

元类：
```python
from src.metaclasses.registry import RegistryMeta, get_registry

class PluginBase(metaclass=RegistryMeta):
    registry_name = "plugins"

class MyPlugin(PluginBase):
    pass

# 获取注册表
registry = get_registry("plugins")
# registry 包含 {'MyPlugin': MyPlugin}
```

### 依赖

仅依赖 Python 标准库，无需额外安装。

### 运行环境

Python 3.6+
