def is_valid_command(command, allowed_commands):
    return command in allowed_commands


def has_parameter(command, parts):
    if command in ["ping", "tracert", "nslookup"]:
        return len(parts) >= 2

    return True