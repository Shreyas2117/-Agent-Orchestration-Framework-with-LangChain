from .agent import create_basic_agent

def main():
    agent = create_basic_agent()
    print("🚀 Gemini LangChain Agent Console")

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Agent: Bye 👋")
            break
        try:
            print("Agent:", agent(user_input))
        except Exception as e:
            print("❌ Error while calling agent:", e)

if __name__ == "__main__":
    main()
