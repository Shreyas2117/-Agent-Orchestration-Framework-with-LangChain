from .agent_tools import run_agent_with_tools

def main():
    print("🚀 Milestone 2: Tool-Enabled Agent")
    print("Type 'exit' to quit.\n")

    while True:
        user = input("You: ")
        if user.lower() == "exit":
            break

        print("Agent:", run_agent_with_tools(user))

if __name__ == "__main__":
    main()
