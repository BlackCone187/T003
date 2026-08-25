def create_request(command, parameter=""):
    if parameter:
        return command + " " + parameter

    return command


def split_request(message):
    return message.split()