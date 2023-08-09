#!/usr/bin python3

import os
import pathlib as pl


def main():
    # Collect some data
    git_uncommitted_changes = os.popen("git status -s").read().strip() != ""
    git_username = os.popen("git config user.name").read().strip()
    git_email = os.popen("git config user.email").read().strip()
    git_repo_name = (
        os.popen("git remote get-url origin").read().split("/")[-1].split(".")[0]
    )

    # Ask for some data
    if git_uncommitted_changes:
        print("You have uncommitted changes. Please commit or stash them first.")
        exit(1)
    repo_name = (
        input(f"Enter the name of the repository [{git_repo_name}]: ") or git_repo_name
    )
    module_name = input(f"Enter the name of the module [{repo_name}]: ") or repo_name
    username = input(f"Enter your username [{git_username}]: ") or git_username
    email = input(f"Enter your email [{git_email}]: ") or git_email
    description = (
        input("Enter a short description of the project: ")
        or "A beautiful description."
    )

    # Print the data
    print(
        f"Using the following values:\n"
        f"\tRepository name: '{repo_name}'\n"
        f"\tModule name: '{module_name}'\n"
        f"\tAuthor: '{username} <{email}'>\n"
        f"\tDescription: '{description}'"
    )
    input("Press enter to continue...")

    # Replace the template values
    for file in pl.Path(".").glob("**/*"):
        if (
            file.is_file()
            and not file.name == "setup_template.py"
            and file.suffix in [".py", ".md", ".yml", ".yaml", ".toml", ".txt"]
        ):
            with open(file, "r") as f:
                content = f.read()

            content_before = content
            content = content.replace(
                "- [ ] Run `setup_template.py`", "- [x] Run `setup_template.py`"
            )
            content = content.replace("template-python-repository", repo_name)
            content = content.replace("APP_NAME", module_name)
            content = content.replace("app-name", module_name)
            content = content.replace("A beautiful description.", description)
            content = content.replace("reinder.vosdewael@childmind.org", email)
            content = content.replace("ENTER_YOUR_EMAIL_ADDRESS", email)
            content = content.replace("Reinder Vos de Wael", username)

            if not content == content_before:
                print(f"Updating {file}")
                with open(file, "w") as f:
                    f.write(content)

    if pl.Path(f"src/APP_NAME").exists():
        pl.Path(f"src/APP_NAME").rename(f"src/{module_name}")

    # Remove this file
    print("Removing setup_template.py")
    pl.Path("setup_template.py").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
