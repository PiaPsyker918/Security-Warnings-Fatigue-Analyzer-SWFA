
# Run all files in experiments folder.
# by PiaPsyker918

import importlib
import pkgutil
import experiments


def run_all():
    print("=== Running all experiments ===\n")

    for module_info in pkgutil.iter_modules(experiments.__path__):
        name = module_info.name

        if name == "run_all":
            continue

        print(f"--- Running {name} ---")

        module = importlib.import_module(f"experiments.{name}")

        if hasattr(module, "run"):
            module.run()
        else:
            print(f"{name} has no run() function")

        print()


if __name__ == "__main__":
    run_all()