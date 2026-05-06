import importlib
import pkgutil


class PluginRegistry:
    def __init__(self):
        self._plugins = {}

    def register(self, plugin_class):
        instance = plugin_class()
        self._plugins[instance.name] = instance

    def get_by_intent(self, intent):
        for plugin in self._plugins.values():
            if intent in plugin.intents:
                return plugin
        return None

    def list_all(self):
        return [{"name": p.name, "intents": p.intents} for p in self._plugins.values()]

    def autodiscover(self):
        from chatbot.plugins import builtins
        for _, module_name, _ in pkgutil.iter_modules(builtins.__path__):
            importlib.import_module(f"chatbot.plugins.builtins.{module_name}")


registry = PluginRegistry()
