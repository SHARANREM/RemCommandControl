import os
import importlib.util
import json
import subprocess

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
    def load_installed_packages():

        os.makedirs(
            "plugins_data",
            exist_ok=True
        )

        if not os.path.exists(
            Brain.PACKAGE_DB
        ):
            return []

        try:

            with open(
                Brain.PACKAGE_DB,
                "r"
            ) as f:

                return json.load(f)

        except:

            return []

    @staticmethod
    def install_package(package):

        # print(
        #     f"Installing package: {package}"
        # )

        subprocess.run(
            [
                Brain.PLUGIN_PYTHON,
                "-m",
                "pip",
                "install",
                package
            ]
        )

    @staticmethod
    def save_installed_packages(packages):

        os.makedirs(
            "plugins_data",
            exist_ok=True
        )

        with open(
            Brain.PACKAGE_DB,
            "w"
        ) as f:

            json.dump(
                packages,
                f,
                indent=4
            )   

    @staticmethod
    def ensure_plugin_packages(module):

        installed = Brain.load_installed_packages()

        required = getattr(
            module,
            "required_packages",
            []
        )

        changed = False

        for package in required:

            if package not in installed:

                Brain.install_package(
                    package
                )

                installed.append(
                    package
                )

                changed = True

        if changed:

            Brain.save_installed_packages(
                installed
            )
    
    @staticmethod
    def execute(command_text):

        # print(os.getcwd())
        # print(Brain.PLUGIN_PYTHON)
        # print(os.path.exists(Brain.PLUGIN_PYTHON))

        command_text = command_text.strip()

        if not command_text:
            raise Exception("Empty command")

        if command_text.startswith("/"):
            command_text = command_text[1:]

        parts = command_text.split()

        command_name = parts[0]
        args = parts[1:]
        
        if command_name == "help":
            # print(Brain.PLUGIN_FOLDER)
            # print(os.getcwd())
            if not args:
    
                return {
                    "type": "help_list",
                    "data": Brain.get_plugins()
                }

            return {
                "type": "help_plugin",
                "data": Brain.get_plugin_help(
                    args[0]
                )
            }

        plugin_path = Brain.find_plugin(command_name)

        if not plugin_path:
            raise Exception(
                f"Plugin '{command_name}' not found"
            )

        module = Brain.load_plugin(
            command_name,
            plugin_path
        )

        Brain.ensure_plugin_packages(
            module
        )

        subprocess.Popen(
            [
                Brain.PLUGIN_PYTHON,
                plugin_path,
                *args
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # print(result.stdout)
        # print(result.stderr)

        return {
            "success": True
        }
    
    @staticmethod
    def find_plugin(plugin_name):

        if not os.path.exists(Brain.PLUGIN_FOLDER):
            os.makedirs(Brain.PLUGIN_FOLDER)

        for file in os.listdir(
            Brain.PLUGIN_FOLDER
        ):

            if not file.endswith(".py"):
                continue

            name = file[:-3]

            if name.lower() == plugin_name.lower():

                return os.path.join(
                    Brain.PLUGIN_FOLDER,
                    file
                )

        return None

    @staticmethod
    def load_plugin(plugin_name, plugin_path):

        spec = importlib.util.spec_from_file_location(
            plugin_name,
            plugin_path
        )

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(module)

        return module
    @staticmethod
    def get_plugins():

        plugins = {}

        for file in os.listdir(
            Brain.PLUGIN_FOLDER
        ):

            if not file.endswith(".py"):
                continue

            name = file[:-3]

            path = os.path.join(
                Brain.PLUGIN_FOLDER,
                file
            )

            try:

                module = Brain.load_plugin(
                    name,
                    path
                )

                # print(f"Loaded: {name}")

                plugins[name] = {
                    "description":
                        getattr(
                            module,
                            "description",
                            "No description"
                        )
                }

            except Exception as e:

                # print(
                #     f"FAILED: {name}"
                # )

                # print(e)
                pass

        return plugins
    
    @staticmethod
    def get_suggestions(text):

        text = text.strip()

        if text.startswith("/"):
            text = text[1:]

        parts = text.split()

        # COMMAND SUGGESTIONS
        if len(parts) <= 1:

            command_text = parts[0] if parts else ""

            suggestions = []

            for plugin in Brain.get_plugins():

                if not command_text:
                    suggestions.append("/" + plugin)

                elif plugin.lower().startswith(
                    command_text.lower()
                ):
                    suggestions.append("/" + plugin)

            return suggestions[:10]

        # ARGUMENT SUGGESTIONS
        plugin_name = parts[0]
        current_arg = parts[-1]

        plugin_path = Brain.find_plugin(plugin_name)

        if not plugin_path:
            return []

        try:

            module = Brain.load_plugin(
                plugin_name,
                plugin_path
            )

            plugin_suggestions = getattr(
                module,
                "suggestions",
                []
            )

            return [
                arg
                for arg in plugin_suggestions
                if arg.lower().startswith(
                    current_arg.lower()
                )
            ][:10]

        except:
            return []

    @staticmethod
    def get_plugin_help(plugin_name):

        plugin_path = Brain.find_plugin(
            plugin_name
        )

        if not plugin_path:
            raise Exception(
                f"Plugin '{plugin_name}' not found"
            )

        module = Brain.load_plugin(
            plugin_name,
            plugin_path
        )

        return getattr(
            module,
            "help",
            "No help available."
        )