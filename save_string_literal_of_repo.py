from github import Github
import os
from dotenv import load_dotenv
import argparse

load_dotenv()


def create_string_literal_of_repo_contents(repo_name: str, subfolder: str):
    string_literal = ""
    g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
    repo = g.get_repo(repo_name)
    contents = repo.get_contents(subfolder)
    print(contents)
    for content in contents:
        print(content)
        print(content.path)
        if content.type == "file":
            try:
                string_literal += f"{content.path}:\n[[START OF FILE]]\n{content.decoded_content.decode('utf-8')}\n[[END OF FILE]]\n\n"
            except:
                print(f"Error decoding content of {content.path}")
                continue
        elif content.type == "dir":
            # string_literal += f"{content.path}:\n"
            string_literal += create_string_literal_of_repo_contents(
                repo_name, f"{subfolder}/{content.name}"
            )

    return string_literal


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--repo_name", type=str, help="The name of the repo to save the contents of", default="thefloatingstring/lmops-test-samples")
    parser.add_argument(
        "--subfolder",
        type=str,
        help="The subfolder to save the contents of",
        default="numpy",
    )
    args = parser.parse_args()
    with open(f"{args.subfolder}_contents.txt", "w") as f:
        f.write(
            create_string_literal_of_repo_contents(
                "thefloatingstring/lmops-test-samples", args.subfolder
            )
        )
