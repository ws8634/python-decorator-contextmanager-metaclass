from src.metaclasses.registry import RegistryMeta, get_registry


def run_metaclass_demo():
    """
    运行元类演示。

    展示自动注册子类的元类行为。
    """
    print("\n" + "=" * 60)
    print("演示 3: 自动注册子类的元类")
    print("=" * 60)

    print("\n[说明] 定义基类时使用元类，所有子类自动注册到注册表")
    print("-" * 40)

    class PluginBase(metaclass=RegistryMeta):
        """
        插件基类。

        所有继承此类的插件都会自动注册到 'plugins' 注册表。
        """
        registry_name = "plugins"

        def execute(self):
            raise NotImplementedError("子类必须实现 execute 方法")

    print(f"  定义基类 PluginBase，registry_name = '{PluginBase.registry_name}'")

    print("\n[场景 1] 定义子类，观察自动注册")
    print("-" * 40)

    class PluginA(PluginBase):
        """插件 A"""

        def execute(self):
            return "PluginA executed"

    class PluginB(PluginBase):
        """插件 B"""

        def execute(self):
            return "PluginB executed"

    print("  定义了 PluginA 和 PluginB 两个子类")

    # 获取注册表
    registry = get_registry("plugins")
    print(f"  注册表中的类: {list(registry.keys())}")

    print("\n[场景 2] 通过注册表动态获取和使用类")
    print("-" * 40)

    # 通过类名获取类对象
    plugin_class = registry.get("PluginA")
    print(f"  从注册表获取 PluginA 类: {plugin_class}")

    # 创建实例并调用方法
    plugin_instance = plugin_class()
    result = plugin_instance.execute()
    print(f"  创建实例并执行: {result}")

    # 使用所有已注册的插件
    print("\n[场景 3] 遍历所有已注册的插件")
    print("-" * 40)

    for name, cls in registry.items():
        print(f"  插件: {name}")
        instance = cls()
        print(f"    执行结果: {instance.execute()}")

    print("\n[场景 4] 动态定义新类，演示即时注册")
    print("-" * 40)

    # 动态创建新类（模拟插件系统的延迟加载）
    class PluginC(PluginBase):
        """动态添加的插件 C"""

        def execute(self):
            return "PluginC executed (dynamically added)"

    print(f"  动态定义了 PluginC")
    print(f"  更新后的注册表: {list(registry.keys())}")

    # 使用新注册的插件
    plugin_c = registry["PluginC"]()
    print(f"  PluginC 执行结果: {plugin_c.execute()}")

    print("\n" + "=" * 60)
    print("说明：元类在类定义时被调用，因此子类可以自动注册")
    print("这在插件系统、工厂模式中非常有用")
    print("=" * 60)
