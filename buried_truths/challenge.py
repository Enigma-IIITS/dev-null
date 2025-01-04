"""
Module: buried_truths

This module defines a class `BuriedTruths` representing a
challenge related to exploring a layered `.xcf` file to uncover
hidden information. The class provides methods for generating
the question, validating the response, and providing the solution.
"""

from pathlib import Path
from config import SUBMISSION_LINK, FILE_LINK
from ....base_challenge import Challenge


class BuriedTruths(Challenge):
    """
    Represents a challenge where participants need to uncover
    hidden information within a layered `.xcf` file.

    This challenge requires participants to analyze the file using
    GIMP or a similar tool, navigate through its layers, and
    reveal the hidden flag.
    """

    # Path to the current script and the associated `.xcf` file
    SCRIPT_PATH: Path = Path(__file__).resolve()
    FILE_LOCATION: Path = SCRIPT_PATH.with_name("buried_truths.xcf")

    def __init__(self):
        """
        Initializes the BuriedTruths challenge with specific attributes:
        - Points: The points awarded for solving the challenge.
        - Penalty: The penalty for incorrect attempts.
        - Hints: A list of hints to guide participants.
        """
        hints = [
            (
                50,
                "Sometimes, what's hidden isn't in plain sight—it's layered beneath. "
                "Explore each layer carefully; what you seek may be just beneath the surface.",
            )
        ]
        super().__init__(points=150, penalty=30, hints=hints)

    async def get_file_location(self, team_id):
        """
        Retrieve the file location of the `.xcf` file for the challenge.

        Args:
            team_id (str): The ID of the team requesting the file.

        Returns:
            str: The path to the `.xcf` file.
        """
        return self.FILE_LOCATION

    async def generate_question(
        self, team_id: str
    ) -> dict:  # pylint: disable=unused-argument
        """
        Generate the full question details for a specific team.

        Args:
            team_id (str): The ID of the team for whom the question is generated.

        Returns:
            dict: A dictionary containing the title and description of the challenge.
        """
        # Load the question template from a text file
        path = self.SCRIPT_PATH.with_name("question.txt")
        question_template = self.get_question_template(path)

        # Format the question description with placeholders replaced
        description = question_template.format(
            submission_url=SUBMISSION_LINK,
            file_url=f"{FILE_LINK}?team_id={team_id}&challenge_id={self.challenge_id}",
            challenge_id=self.challenge_id,
        )

        # Store the expected flag in the database for validation purposes
        await self.db.teams.update_one(
            {"team_id": team_id},
            {
                "$set": {
                    "data_to_validate.BuriedTruths": {
                        "flag": "ENIGMA{M4sk3d_L4y3r_Unc0v3r3d}"
                    },
                }
            },
        )

        # Construct the question JSON with the title and description
        question_json = {"title": "Buried Truths", "description": description}
        return self.generate_full_question(question_json)
