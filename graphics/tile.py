"""Clase Tile: representa una baldosa (5x5 pies) con una textura y orientación.

Provee una fábrica `from_file` para cargar una textura desde disco, caching
de versiones escaladas/rotadas y un método `render` para dibujarla en una
`pygame.Surface` destino.
"""
from __future__ import annotations

import os
from typing import Optional, Tuple

import pygame


class Tile:
    """Baldosa con textura y orientación.

    - La textura se carga desde un archivo con `from_file`.
    - `orientation` es el ángulo en grados (rotación CW aplicada sobre la textura).
    - `light` es un valor futuro para manejar iluminación (0.0-1.0).
    """

    def __init__(self, image: pygame.Surface, orientation: float = 0.0, light: float = 1.0):
        self._original: pygame.Surface = image
        self.orientation: float = float(orientation)
        self.light: float = float(light)
        self._cache: dict[Tuple[float, Tuple[int, int]], pygame.Surface] = {}

    @classmethod
    def from_file(cls, path: str, orientation: float = 0.0, light: float = 1.0) -> "Tile":
        """Carga una imagen desde `path` y crea un Tile.

        Lanza `FileNotFoundError` si el archivo no existe. Usa `convert_alpha()`
        para preservar transparencias y optimizar el blit.
        """
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Texture not found: {path}")
        image = pygame.image.load(path).convert_alpha()
        return cls(image, orientation=orientation, light=light)

    @classmethod
    def from_color(
        cls,
        color: Tuple[int, ...],
        border_color: Optional[Tuple[int, ...]] = None,
        border_width: int = 1,
        size: Tuple[int, int] = (64, 64),
        orientation: float = 0.0,
        light: float = 1.0,
    ) -> "Tile":
        """Crea un Tile con una `Surface` rellena de `color` y opcionalmente
        bordeada por `border_color`.

        - `color` y `border_color` deben ser tuplas RGB(A) aceptadas por Pygame.
        - `size` define el tamaño base (px) de la superficie de la baldosa.
        """
        surf = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        surf.fill(color)
        if border_color is not None and border_width > 0:
            pygame.draw.rect(surf, border_color, surf.get_rect(), border_width)
        return cls(surf, orientation=orientation, light=light)

    def get_surface(self, size: Tuple[int, int]) -> pygame.Surface:
        """Devuelve una `Surface` preparada (escalada y rotada) para `size`.

        Cacha combinaciones (orientación, tamaño) para evitar trabajo repetido.
        """
        key = (self.orientation % 360, size)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        surf = self._original
        if size != surf.get_size():
            surf = pygame.transform.smoothscale(surf, size)
        if (self.orientation % 360) != 0:
            surf = pygame.transform.rotate(surf, self.orientation)

        self._cache[key] = surf
        return surf

    def render(self, target: pygame.Surface, pos: Tuple[int, int], size: Tuple[int, int]):
        """Dibuja la baldosa en `target` en la posición `pos` (px) con `size` (px).

        `pos` es la esquina superior izquierda donde se renderiza la baldosa.
        """
        surf = self.get_surface(size)
        target.blit(surf, pos)
