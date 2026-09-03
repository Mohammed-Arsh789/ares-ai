from core.ai import AIClient


def main():

    ai = AIClient()

    print("=" * 50)
    print("ARES")
    print("Artificial Reasoning & Enhanced System")
    print("=" * 50)
    print("Type 'exit' to quit.")
    print("Type 'reset' to clear conversation.")
    print()

    while True:

        try:
            user_input = input("You > ").strip()

        except KeyboardInterrupt:
            print("\nARES > Goodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("ARES > Goodbye.")
            break

        if user_input.lower() == "reset":
            ai.reset()
            print("ARES > Conversation reset.")
            continue

        response = ai.ask(user_input)

        print(f"ARES > {response}")
        print()


if __name__ == "__main__":
    main()