from typing import Optional, List


class ResultUserPreference:
    def __init__(self, actors: Optional[List[str]], genres: Optional[List[str]], countries: Optional[List[str]], year: str):
        self.actors = actors
        self.genres = genres
        self.countries = countries
        self.year = year

    def to_dict(self):
        return {
            "actors": self.actors,
            "genres": self.genres,
            "countries": self.countries,
            "year": self.year
        }
