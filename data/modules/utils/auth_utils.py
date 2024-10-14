import sys

def checkStatusCode(status_code):
    status_code_string = str(status_code)
    is_successful = status_code_string.startswith("2")

    if not is_successful:
        print("Something has went wrong.\nError: The https request was not successful. This could happen due to an invalid or expired access token or due to a server-side error.")
        sys.exit(1)
