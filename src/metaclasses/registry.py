from typing import Dict, Type, Any, List


_registries: Dict[str, Dict[str, Type[Any]]] = {}


def get_registry(registry_name: str) -> Dict[str, Type[Any]]:
    """
    获取指定名称的注册表。

    参数:
        registry_name: 注册表的名称

    返回:
        一个字典，键是类名，值是对应的类对象
    """
    if registry_name not in _registries:
        _registries[registry_name] = {}
    return _registries[registry_name]


class RegistryMeta(type):
    """
    自动注册子类的元类。

    用途：在定义类时，自动将其注册到全局注册表中，
         使其他代码可以通过名称或类型来发现和获取这些类。

    场景：
    - 插件系统：插件基类使用此元类，所有插件子类自动注册
    - 工厂模式：通过类型名称动态创建实例
    - 策略模式：根据配置选择不同的策略实现

    与装饰器和上下文管理器的区别：
    - 装饰器：增强函数/方法的行为（运行时增强）
    - 上下文管理器：管理资源的获取和释放（资源生命周期）
    - 元类：控制类的创建过程（类定义时的行为）

    工作原理：
    元类在类定义时被调用（而不是实例创建时），
    因此我们可以在类被定义的那一刻就将其注册到注册表中。

    使用方式：
        1. 定义一个基类，使用此元类
        2. 在基类中定义 registry_name 类属性，指定注册表名称
        3. 所有继承该基类的子类都会自动被注册

    示例:
        class PluginBase(metaclass=RegistryMeta):
            registry_name = "plugins"
            # 基类定义...

        class MyPlugin(PluginBase):
            # 这个类会自动注册到 "plugins" 注册表中
            pass

        # 获取注册表
        registry = get_registry("plugins")
        # registry 会包含 {'MyPlugin': MyPlugin}
    """

    def __new__(
        mcs: Type["RegistryMeta"],
        name: str,
        bases: tuple,
        namespace: dict,
    ) -> Type[Any]:
        """
        创建新类时调用此方法。

        参数:
            mcs: 元类本身
            name: 新类的名称
            bases: 父类元组
            namespace: 类的命名空间字典

        返回:
            新创建的类对象
        """
        # 使用 type 正常创建类
        new_class = super().__new__(mcs, name, bases, namespace)

        # 检查是否定义了 registry_name 类属性
        registry_name = getattr(new_class, 'registry_name', None)

        # 判断是否是基类：检查父类中是否有使用 RegistryMeta 的类
        # 如果父类中没有使用 RegistryMeta 的类，则这是基类，不注册
        # 如果父类中有使用 RegistryMeta 的类，则这是子类，注册
        is_subclass = False
        for base in bases:
            if isinstance(base, RegistryMeta):
                is_subclass = True
                break

        # 只有当有 registry_name 且是子类时才注册
        if registry_name is not None and is_subclass:
            registry = get_registry(registry_name)
            registry[name] = new_class

        return new_class
