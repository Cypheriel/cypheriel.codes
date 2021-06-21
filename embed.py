from dataclasses import dataclass


@dataclass
class Embed:
    site_name: str = "cypheriel.codes"
    title: str = "Default Title"
    description: str = ""
    url: str = ""
    color: str = "2d4268"


@dataclass
class OEmbed:
    title: str = ""
    description: str = ""
    author_name: str = ""
    author_url: str = "https://cypheriel.codes/"
    provider_name: str = "cypheriel.codes"
    provider_url: str = "https://cypheriel.codes/"
    color: str = "2d4268"

    def render(self):
        return {
            "embed": {
                "title": self.title,
                "description": self.description,
                "color": self.color,
            },
            "link": f"https://cypheriel.codes/oembed.json"
                    f"?author_name={self.author_name}&author_url={self.author_url}"
                    f"&provider_name={self.provider_name}&provider_url={self.provider_url}"
        }
