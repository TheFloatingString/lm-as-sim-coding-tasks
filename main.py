from github import Github
from dotenv import load_dotenv
import openai
import os
import argparse
import anthropic
import together

load_dotenv()


def run_command(provider: str, model: str, command: str):
    with open("numpy_contents.txt", "r") as f:
        directory_contents = f.read()

    if provider == "openai":
        openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a MacOS operating system. Given the following folder directory, when the user sends a terminal command, respond with the output of the command. Only return the output of the command, no other text.\n\nDirectory contents:\n\n{directory_contents}",
                },
                {"role": "user", "content": command},
            ],
        )
        print(response.choices[0].message.content)
    elif provider == "anthropic":
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        message = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=1,
            system=f"You are a MacOS operating system. Given the following folder directory, when the user sends a terminal command, respond with the output of the command. Only return the output of the command, no other text.\n\nDirectory contents:\n\n{directory_contents}",
            messages=[{"role": "user", "content": [{"type": "text", "text": command}]}],
        )
        print(message.content[0].text)

        # anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # response = anthropic_client.messages.create(
        #     model=model,
        #     messages=[
        #         {"role": "system", "content": f"You are a MacOS operating system. Given the following folder directory, when the user sends a terminal command, respond with the output of the command. Only return the output of the command, no other text.\n\nDirectory contents:\n\n{directory_contents}"},
        #         {"role": "user", "content": command}
        #     ]
        # )
        # print(response.content[0].text)


# def main():
#     run_command("uv run numpy/scripts/m1.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--provider", type=str, help="The provider to use", default="openai"
    )
    parser.add_argument(
        "--model", type=str, help="The model to use", default="gpt-4o-mini"
    )
    parser.add_argument("--command", type=str, help="The command to run")
    args = parser.parse_args()
    run_command(provider=args.provider, model=args.model, command=args.command)
