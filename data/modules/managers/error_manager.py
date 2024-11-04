import sys

class ErrorManager:
    
    def printErrorAndExit(self, error_text):
        print(f"Something has went wrong. Error: {error_text}")
        sys.exit(1)
    
    subcommand_not_passed_error = "A subcommand has not been passed. To check the list of available subcommands for the command entered, run 'help'."
    invalid_subcommand_error = "Invalid subcommand. To check the list of available subcommands for the command entered, run 'help'."