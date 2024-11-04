from data.modules.controllers.command_controller import CommandController
from data.modules.managers.repository_manager import RepositoryManager
from data.modules.managers.error_manager import ErrorManager
from data.modules.managers.user_input_manager import UserInputManager
from data.modules.configs.constants import Constants
from data.modules.configs.base_classes.repository import Repository

class Program:
    def __init__(self):
        self.constants = Constants()
        self.base_classes = {"Repository": Repository}

        self.repository_manager = RepositoryManager(self.base_classes, self.constants)
        self.error_manager = ErrorManager()
        self.user_input_manager = UserInputManager()
        
        self.command_controller = CommandController(
            base_classes = self.base_classes,
            constants = self.constants,
            repository_manager = self.repository_manager,
            error_manager = self.error_manager,
            user_input_manager = self.user_input_manager,
        )

    def run(self):
        arguments = self.user_input_manager.getArguments()
        flags = self.user_input_manager.getFlags()
        self.command_controller.executeCommand(arguments, flags)