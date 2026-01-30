from graphics.tile import Tile
from dnd.classes import Class

class PlayerCharacter:
    name: str
    level: int
    character_class: Class
    profiency_bonus: int
    HP_max: int
    HP_current: int
    AC: int
    PP: int 
    movement_speed: int
    remaining_movement: int
    surf: Tile
    position: tuple[int, int]
    ability_scores: dict[str, int]
    ability_modifiers: dict[str, int]
    skill_proficiencies: list[str]
    skill_modifiers: dict[str, int]