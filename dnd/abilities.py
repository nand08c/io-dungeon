"""Definiciones de habilidades para clases y personajes.

`Ability` guarda un nombre y una lista de niveles con su descripción correspondiente.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class Ability:
    """Representa una habilidad o rasgo que progresa por niveles.

    - `name`: nombre de la habilidad.
    - `tiers`: lista de pares `(nivel, descripcion)` indicando qué cambia en cada nivel.
    """

    name: str
    tiers: List[Tuple[int, str]] = field(default_factory=list)

    def add_tier(self, level: int, description: str) -> None:
        """Agrega un par (nivel, descripción). Mantiene la lista ordenada por nivel."""
        self.tiers.append((int(level), str(description)))
        self.tiers.sort(key=lambda t: t[0])

    def description_at(self, level: int) -> Optional[str]:
        """Devuelve la descripción aplicable para `level`.

        Si no hay una entrada exacta, devolverá la descripción del último tier
        cuyo nivel sea <= `level`. Si no existe ninguno, devuelve `None`.
        """
        applicable = None
        for lvl, desc in self.tiers:
            if lvl <= level:
                applicable = desc
            else:
                break
        return applicable

    def available_at(self, level: int) -> bool:
        """True si la habilidad tiene al menos un tier con `nivel` <= `level`."""
        return any(lvl <= level for lvl, _ in self.tiers)
