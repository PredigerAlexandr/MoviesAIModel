from typing import Optional, List


class MovieEntity:
    def __init__(self, id: str, external_id: int, title: str, genres: Optional[List[str]], actors: Optional[List[str]],
                 created_year: int, created_countries: Optional[List[str]]):
        self.Id = id
        self.ExternalId = external_id
        self.Title = title
        self.Genres = genres
        self.Actors = actors
        self.CreatedYear = created_year
        self.CreatedCountries = created_countries

    def __repr__(self):
        return f"MovieEntity(Id={self.Id}, Title={self.Title}, CreatedYear={self.CreatedYear})"