from pathlib import Path
from importlib import import_module

def register_all_subscriptions():
    # ✅ Corrección: apuntar correctamente a /app/modules
    modules_path = Path(__file__).resolve().parent.parent.parent / "modules"

    for module_dir in modules_path.iterdir():
        subscription_file = module_dir / "application" / "subscriptions" / "subscriptions.py"
        if subscription_file.exists():
            module_path = f"app.modules.{module_dir.name}.application.subscriptions"
            try:
                mod = import_module(module_path)
                if hasattr(mod, "subscribe_user_events"):
                    mod.subscribe_user_events()
                    print(f"✅ Suscripciones registradas para módulo: {module_dir.name}")
                elif hasattr(mod, "register_subscriptions"):
                    mod.register_subscriptions()
                    print(f"✅ Suscripciones registradas para módulo: {module_dir.name}")
            except Exception as e:
                print(f"⚠️  Error registrando suscripciones en {module_dir.name}: {e}")
