from data.modules.controllers import CommandController
from data.modules.managers import RequestsManager, DataManager, ErrorManager, UserInputManager, ParseManager

class Program:
    def __init__(self):
        self.requests_manager = RequestsManager()
        self.data_manager = DataManager()
        self.error_manager = ErrorManager()
        self.user_input_manager = UserInputManager()
        self.parse_manager = ParseManager()
        
        self.command_controller = CommandController(
            requests_manager = self.requests_manager,
            data_manager = self.data_manager,
            error_manager = self.error_manager,
            user_input_manager = self.user_input_manager,
            parse_manager = self.parse_manager
        )

    def run(self):
        arguments = self.user_input_manager.getArguments()
        flags = self.user_input_manager.getFlags()
        self.command_controller.executeCommand(arguments, flags)