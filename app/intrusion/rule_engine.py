def check_rules(packet: dict):
    if packet["failed_logins"] > 5:
        return True
    if packet["packet_size"] > 1500:
        return True
    return False
