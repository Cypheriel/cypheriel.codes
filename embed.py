from dataclasses import dataclass


@dataclass
class Embed:
    site_name: str = "cypheriel.codes"
    title: str = "Default Title"
    description: str = ""
    url: str = None
    color: str = "2d4268"
