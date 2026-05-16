# Tutaj sobie zdefiniujemy kolejne elementy naszego modelu, czyli pomocnicze klase które będą w tym modelu reprezentowane.

from pydantic import BaseModel
from typing import Optional


class Point(BaseModel):
    