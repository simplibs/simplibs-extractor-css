import random

import pytest

PIECES = ["a", ".b", "{", "}", ";", ":", " ", "  ", "\n", "\n\n", "/*", "*/", "'", '"', "//", "@import 'x';", "@use 'y';", "url(", ")", "x"]


@pytest.fixture(scope="session")
def stylesheet_samples() -> list[str]:
    """300 short random stylesheet-like texts (seeded), many of them damaged on purpose: one set for every test that compares two ways of doing the same thing."""
    rng = random.Random(31)
    return ["".join(rng.choice(PIECES) for _ in range(rng.randint(0, 14))) for _ in range(300)]
