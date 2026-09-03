from core.brain import ARES


def main():

    ares = ARES()

    print("=" * 55)
    print("ARES")
    print("Artificial Reasoning & Enhanced System")
    print("=" * 55)
    print("Type 'exit' to quit.")
    print("Type 'reset' to reset conversation.")
    print()

    try:

        while True:

            user_input = input("You > ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":

                print("ARES > Goodbye.")
                break

            if user_input.lower() == "reset":

                ares.ai.reset()

                print("ARES > Conversation reset.")
                continue

            response = ares.respond(user_input)

            print(f"ARES > {response}")
            print()

    except KeyboardInterrupt:

        print("\nARES > Goodbye.")

    finally:

        ares.close()


if __name__ == "__main__":
    main()