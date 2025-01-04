"""
Git Commit Challenge Module

This module contains the implementation of the Git Commit Challenge.
Participants need to find a specific commit containing a flag hidden within
the Git history.
"""

import re
import os
import shutil
import hashlib
from pathlib import Path

from config import SUBMISSION_LINK, FILE_LINK
from ....base_challenge import Challenge


class GitCommitChallenge(Challenge):
    """
    GitCommitChallenge class represents a challenge where participants
    need to find a hidden flag within a Git repository's commit history.
    """

    FLAG_LENGTH: int = 10
    SCRIPT_PATH: Path = Path(__file__).resolve()
    COMMITS_DIR_LOCATION: Path = SCRIPT_PATH.with_name("commits")
    REPO_DIR_LOCATION: Path = SCRIPT_PATH.with_name("repositories")

    def __init__(self):
        hints = [
            (50, "Try inspecting the commit history"),
        ]
        super().__init__(points=150, penalty=50, hints=hints)

    async def gen_repository(self, team_id: str) -> tuple[str, str]:
        """
        Generate a Git repository with a hidden flag in a commit message or file.

        Args:
            team_id (str): The ID of the team.

        Returns:
            tuple: A tuple containing the path to the repository and the flag value.
        """
        team = await self.db.get_team(team_id)
        repo_path = self.db.get_nested_value(
            team, "questions.GitCommitChallenge.location"
        )
        flag_value = self.db.get_nested_value(
            team, "data_to_validate.GitCommitChallenge.flag"
        )
        if repo_path and flag_value and os.path.exists(repo_path):
            print("Returning existing repository for git challenge", team_id)
            return repo_path, flag_value

        print("Generating new repository for git challenge", team_id)

        # Generate random flag value
        flag_1 = "c0mm1t_0r_d13_try1ng_"
        message = team_id + "Enigma Secret Hash"
        md5 = hashlib.md5()
        md5.update(message.encode())
        flag_2 = md5.hexdigest()

        flag = flag_1 + flag_2

        # Create repository directory
        repo_path = str(self.REPO_DIR_LOCATION / f"GitCommitChallenge_{team_id}")
        os.makedirs(repo_path, exist_ok=True)
        os.chdir(repo_path)

        # Step 1: Set the default branch to 'main' globally
        os.system("git config --global init.defaultBranch main")

        # Step 2: Check if the current branch is not 'main' before renaming it
        # This will help avoid issues if the branch is already 'main'
        current_branch = os.popen("git symbolic-ref --short HEAD").read().strip()

        if current_branch != "main":
            os.system("git branch -m main")  # Rename the current branch to 'main'

        # Step 3: Set global user configurations
        os.system("git config --global user.username 'Ns-AnoNymouS'")
        os.system("git config --global user.name 'Ns-AnoNymouS'")
        os.system("git config --global user.email 'lankotunaveen@gmail.com'")

        # Step 4: Initialize the Git repository if not already initialized
        # Check if git is already initialized (i.e., check if the .git directory exists)
        if not os.path.isdir(".git"):
            os.system("git init")

        # Fetch the commits from the commits directory and commit them to the repository
        for i in range(1, 7):
            commit_message = f"'Commit #{i + 1}'"
            with open(self.COMMITS_DIR_LOCATION / f"commit_{i}.py", "r") as f:
                with open(f"{repo_path}/main.py", "w") as file:
                    file.write(
                        f.read().replace("FLAG_1", flag_1).replace("FLAG_2", flag_2)
                    )

            os.system("git add main.py")
            os.system(f"git commit -m {commit_message}")

        # Zip the repository
        zip_file = self.REPO_DIR_LOCATION / f"GitCommitChallenge_{team_id}.zip"
        self.zip_folder(repo_path, zip_file)

        # Remove the repository directory
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        # Save flag and repository path in the database
        await self.db.teams.update_one(
            {"team_id": team_id},
            {
                "$set": {
                    "questions.GitCommitChallenge": {"location": str(zip_file)},
                    "data_to_validate.GitCommitChallenge": {
                        "flag": f"ENIGMA{{{flag}}}"
                    },
                }
            },
        )

        return zip_file, flag_value

    async def generate_question(self, team_id: str) -> dict:
        """
        Generate the full question description for the team.

        Args:
            team_id (str): The ID of the team.

        Returns:
            dict: The formatted question.
        """
        path = self.SCRIPT_PATH.with_name("question.txt")
        description = self.get_question_template(path).format(
            submission_url=SUBMISSION_LINK,
            challenge_id=self.challenge_id,
            file_url=f"{FILE_LINK}?team_id={team_id}&challenge_id={self.challenge_id}",
        )
        question_json = {"title": "Git Challenge", "description": description}
        return self.generate_full_question(question_json)

    async def get_file_location(self, team_id: str) -> str:
        """
        Get the location of the generated Git repository for the team.

        Args:
            team_id (str): The ID of the team.

        Returns:
            str: The location of the generated repository.
        """
        repo_path, _ = await self.gen_repository(team_id)
        return repo_path
