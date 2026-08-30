def ares_response(message):
    message = message.lower().strip()

    if message in ["hello", "hi", "hey"]:
        return "Hello. ARES systems are online."

    if "your name" in message:
        return "I am ARES, your personal AI assistant."

    if "how are you" in message:
        return "All systems operational."

    if message in ["bye", "exit", "quit"]:
        return None

    return "I don't know how to do that yet."


def main():
    print("=" * 45)
    print("              ARES v0.1")
    print("          SYSTEMS ONLINE")
    print("=" * 45)

    while True:
        user_message = input("\nYou: ")

        response = ares_response(user_message)

        if response is None:
            print("ARES: Goodbye.")
            break

        print(f"ARES: {response}")


if __name__ == "__main__":
    main()