
"""Definición de clases (profesiones) de D&D con sus habilidades."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict

from .abilities import Ability


@dataclass
class Class:
    """Representa una clase con dado de golpe, salvaciones y habilidades.

    - `hit_die`: número de caras del dado de golpe (por ejemplo 8, 10, 12).
    - `saving_throws`: lista de habilidades de salvación en las que la clase tiene competencia.
    - `abilities`: lista de `Ability` que la clase otorga o progresa por niveles.
    """

    name: str
    hit_die: int
    saving_throws: List[str]
    abilities: List[Ability] = field(default_factory=list)

    # Spellcasting support
    # - `caster_type` puede ser "Full", "Half", "Third" o None para clases sin magia.
    caster_type: Optional[str] = None
    # Mapa nivel de conjuro -> número máximo de huecos (por ejemplo {1:4, 2:3, ...})
    spell_slots_max: Optional[Dict[int, int]] = None
    # Conteo actual de huecos disponibles (misma forma que spell_slots_max). None si no aplica.
    spell_slots_current: Optional[Dict[int, int]] = None

    def add_ability(self, ability: Ability) -> None:
        self.abilities.append(ability)

    def is_spellcaster(self) -> bool:
        return self.caster_type is not None

    def set_spell_slots_max(self, slots: Optional[Dict[int, int]]) -> None:
        """Define los slots máximos y resetea los slots actuales en consecuencia.

        `slots` puede ser `None` para indicar que la clase no tiene slots.
        """
        if slots is None:
            self.spell_slots_max = None
            self.spell_slots_current = None
            return
        # copy to avoid external mutation
        self.spell_slots_max = {int(k): int(v) for k, v in slots.items()}
        # inicializar slots actuales como máximos
        self.spell_slots_current = {k: v for k, v in self.spell_slots_max.items()}

    def use_slot(self, level: int) -> bool:
        """Consume un hueco de nivel `level`. Devuelve True si se pudo consumir."""
        if not self.spell_slots_current or level not in self.spell_slots_current:
            return False
        if self.spell_slots_current[level] <= 0:
            return False
        self.spell_slots_current[level] -= 1
        return True

    def recover_slot(self, level: int, amount: int = 1) -> int:
        """Recupera hasta `amount` huecos de `level`. Devuelve la cantidad realmente recuperada."""
        if not self.spell_slots_current or not self.spell_slots_max or level not in self.spell_slots_current:
            return 0
        before = self.spell_slots_current[level]
        self.spell_slots_current[level] = min(self.spell_slots_max[level], before + int(amount))
        return self.spell_slots_current[level] - before

    def reset_slots(self) -> None:
        """Restaura los slots actuales a los máximos (por ejemplo tras un descanso).

        No hace nada si la clase no es lanzadora o no tiene slots definidos.
        """
        if not self.spell_slots_max:
            return
        self.spell_slots_current = {k: v for k, v in self.spell_slots_max.items()}

    def abilities_at_level(self, level: int) -> List[Ability]:
        """Devuelve las habilidades (o rasgos) que están disponibles al `level`.

        Una habilidad se considera "disponible" si tiene al menos un tier con
        nivel <= `level`.
        """
        return [a for a in self.abilities if a.available_at(level)]
