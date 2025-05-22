from typing import Optional, List
from uuid import UUID

import numpy as np


class UserPreference:
    def __init__(self, id: str, user_id: int, preference: Optional[List[float]], rated_film_ids: Optional[List[UUID]]):
        self.id = id
        self.user_id = user_id
        self.preference = preference
        self.rated_film_ids = rated_film_ids
