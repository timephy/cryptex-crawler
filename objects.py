from dataclasses import dataclass


@dataclass
class Coin:
    name: str
    algorithm: str
    mined_24h: float
    revenue_24h: float
    profit_24h: float


@dataclass
class Card:
    name: str
    coins: list[Coin]
