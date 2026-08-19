import os
import importlib.util
import json
import subprocess
import sys

class Brain:

    PLUGIN_FOLDER = "plugins"
    PLUGIN_PYTHON = os.path.join(
        "plugin_python",
        "Scripts",
        "python.exe"
    )

    PACKAGE_DB = os.path.join(
        "plugins_data",
        "installed_packages.json"
    )

    @staticmethod
    def get_python_exe():
        if os.path.exists(Brain.PLUGIN_PYTHON):
            return Brain.PLUGIN_PYTHON
        return sys.executable

    @staticmethod
    def load_installed_packages():
        os.makedirs("plugins_data", exist_ok=True)
        if not os.path.exists(Brain.PACKAGE_DB):
            return []
        try:
            with open(Brain.PACKAGE_DB, "r") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def get_missing_packages(command_text):
        command_text = command_text.strip()
        if not command_text:
            return []
        if command_text.startswith("/"):
            command_text = command_text[1:]

        parts = command_text.split()
        if not parts or parts[0] in ["help", "exit", "quit"]:
            return []

        plugin_name = parts[0]
        plugin_path = Brain.find_plugin(plugin_name)
        if not plugin_path:
            return []

        try:
            module = Brain.load_plugin(plugin_name, plugin_path)
            required = getattr(module, "required_packages", [])
            installed = Brain.load_installed_packages()
            return [pkg for pkg in required if pkg not in installed]
        except Exception:
            return []

    @staticmethod
    def install_package(package, status_callback=None):
        if status_callback:
            status_callback(f"Installing missing package: '{package}'... Please wait.")

        subprocess.run(
            [
                Brain.get_python_exe(),
                "-m",
                "pip",
                "install",
                package
            ],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        if status_callback:
            status_callback(f"Successfully installed '{package}'!")

    @staticmethod
    def save_installed_packages(packages):
        os.makedirs("plugins_data", exist_ok=True)
        with open(Brain.PACKAGE_DB, "w") as f:
            json.dump(packages, f, indent=4)

    @staticmethod
    def ensure_plugin_packages(module, status_callback=None):
        installed = Brain.load_installed_packages()
        required = getattr(module, "required_packages", [])
        changed = False

        for package in required:
            if package not in installed:
                Brain.install_package(package, status_callback=status_callback)
                installed.append(package)
                changed = True

        if changed:
            Brain.save_installed_packages(installed)
    
    @staticmethod
    def execute(command_text, status_callback=None):
        command_text = command_text.strip()
        if not command_text:
            raise Exception("Empty command")

        if command_text.startswith("/"):
            command_text = command_text[1:]

        parts = command_text.split()
        command_name = parts[0]
        args = parts[1:]
        
        if command_name == "help":
            if not args:
                return {
                    "type": "help_list",
                    "data": Brain.get_plugins()
                }
            return {
                "type": "help_plugin",
                "data": Brain.get_plugin_help(args[0])
            }

        plugin_path = Brain.find_plugin(command_name)
        if not plugin_path:
            raise Exception(f"Plugin '{command_name}' not found")

        module = Brain.load_plugin(command_name, plugin_path)
        
        # Check and install packages
        Brain.ensure_plugin_packages(module, status_callback=status_callback)

        if status_callback:
            status_callback(f"Executing /{command_name}...")

        subprocess.Popen(
            [
                Brain.get_python_exe(),
                plugin_path,
                *args
            ],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        return {"success": True}
    
    @staticmethod
    def find_plugin(plugin_name):
        if not os.path.exists(Brain.PLUGIN_FOLDER):
            os.makedirs(Brain.PLUGIN_FOLDER)

        for file in os.listdir(Brain.PLUGIN_FOLDER):
            if not file.endswith(".py"):
                continue
            name = file[:-3]
            if name.lower() == plugin_name.lower():
                return os.path.join(Brain.PLUGIN_FOLDER, file)

        return None

    @staticmethod
    def load_plugin(plugin_name, plugin_path):
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def get_plugins():
        plugins = {}
        if not os.path.exists(Brain.PLUGIN_FOLDER):
            return plugins

        for file in os.listdir(Brain.PLUGIN_FOLDER):
            if not file.endswith(".py"):
                continue
            name = file[:-3]
            path = os.path.join(Brain.PLUGIN_FOLDER, file)
            try:
                module = Brain.load_plugin(name, path)
                plugins[name] = {
                    "description": getattr(module, "description", "No description")
                }
            except Exception:
                pass

        return plugins
    
    @staticmethod
    def get_suggestions(text):
        text = text.strip()
        if text.startswith("/"):
            text = text[1:]

        parts = text.split()

        # Command suggestions
        if len(parts) <= 1:
            command_text = parts[0] if parts else ""
            suggestions = []
            for plugin in Brain.get_plugins():
                if not command_text:
                    suggestions.append("/" + plugin)
                elif plugin.lower().startswith(command_text.lower()):
                    suggestions.append("/" + plugin)
            return suggestions[:10]

        # Argument suggestions
        plugin_name = parts[0]
        current_arg = parts[-1]
        plugin_path = Brain.find_plugin(plugin_name)
        if not plugin_path:
            return []

        try:
            module = Brain.load_plugin(plugin_name, plugin_path)
            plugin_suggestions = getattr(module, "suggestions", [])
            return [
                arg for arg in plugin_suggestions
                if arg.lower().startswith(current_arg.lower())
            ][:10]
        except Exception:
            return []

    @staticmethod
    def get_plugin_help(plugin_name):
        plugin_path = Brain.find_plugin(plugin_name)
        if not plugin_path:
            raise Exception(f"Plugin '{plugin_name}' not found")
        module = Brain.load_plugin(plugin_name, plugin_path)
        return getattr(module, "help", "No help available.")