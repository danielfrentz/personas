from enum import Enum


class MonologueIntent(str, Enum):
    EDUCATIONAL = "educational",
    PROBLEM_SOLVING = "problem_solving",
    LECTURE = "lecture",
    PROOF_REVIEW = "proof_review",