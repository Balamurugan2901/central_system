def extract_features(packet: dict):
    return [
        packet["packet_size"],
        packet["failed_logins"],
        1 if packet["protocol"] == "TCP" else 0
    ]
