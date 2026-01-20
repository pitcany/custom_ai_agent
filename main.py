import argparse
import sys

sys.path.insert(0, ".")
from agent import TaskAutomationAgent


def interactive_mode(agent):
    """Run agent in interactive mode."""
    print("🤖 Starter Agent with GLM 4.7")
    print("Type your tasks or 'quit' to exit\n")

    while True:
        try:
            task = input("➤ Task: ").strip()

            if task.lower() in ("quit", "exit", "q"):
                print("Goodbye! 👋")
                break

            if not task:
                continue

            print("\n⏳ Processing...")
            result = agent.run(task)

            if result["success"]:
                print(f"\n✅ Result:\n{result['output']}")
                if result["steps"]:
                    print(f"\n📋 Steps taken: {len(result['steps'])}")
            else:
                print(f"\n❌ Error: {result['error']}")

            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}\n")


def single_task_mode(agent, task):
    """Execute a single task and exit."""
    print(f"⏳ Processing: {task}")
    result = agent.run(task)

    if result["success"]:
        print(f"\n✅ Result:\n{result['output']}")
        if result["steps"]:
            print(f"\n📋 Steps taken: {len(result['steps'])}")
    else:
        print(f"\n❌ Error: {result['error']}")


def main():
    parser = argparse.ArgumentParser(description="Starter Agent with GLM 4.7")
    parser.add_argument(
        "--task", "-t", type=str, help="Single task to execute (skip interactive mode)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    from config import Config

    agent = TaskAutomationAgent(Config)

    if args.task:
        single_task_mode(agent, args.task)
    else:
        interactive_mode(agent)


if __name__ == "__main__":
    main()
