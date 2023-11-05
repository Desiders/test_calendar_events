from dataclasses import dataclass


@dataclass
class Claims:
    iss: str
    sub: str
    alg: str
    exp: int
