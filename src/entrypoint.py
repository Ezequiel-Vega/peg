import os
from app import created_app
from dotenv import load_dotenv

def main():
    # Cargar variables de entorno
    load_dotenv()

    settings_module = os.environ.get('SETTING_MODULE_PEG', 'config.dev')

    app = created_app(settings_module)

    return app

if __name__ == '__main__':
    main().run()
