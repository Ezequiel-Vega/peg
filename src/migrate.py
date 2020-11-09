from flask_migrate import MigrateCommand
from flask_script import Manager
from entrypoint import main

app = main()
manager: Manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
