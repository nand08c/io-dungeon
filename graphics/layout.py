"""Layout: contenedor de `Tile`s y renderizado por región visible.

La clase `Layout` mantiene una cuadrícula de `Tile` (o `None`) y ofrece
un método `render` que dibuja únicamente las baldosas visibles en la
superficie destino, usando un `camera_offset` para implementar una cámara.
"""
from __future__ import annotations

from typing import Optional, Tuple, List

import pygame

from .tile import Tile


class Layout:
    """Contenedor de tiles en una cuadrícula rectangular.

    - `width` y `height` son la cantidad de tiles en X/Y.
    - `tile_size` es el tamaño en píxeles de cada baldosa (w,h).
    """

    def __init__(self, width: int, height: int, tile_size: Tuple[int, int]):
        self.width = width
        self.height = height
        self.tile_w, self.tile_h = tile_size
        self.grid: List[List[Optional[Tile]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]

    def set_tile(self, x: int, y: int, tile: Optional[Tile]):
        self.grid[y][x] = tile

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        return self.grid[y][x]

    def render(self, surface: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)):
        """Dibuja las baldosas visibles en `surface`.

        `camera_offset` es (px_x, px_y) indicando qué parte del layout está
        en la esquina superior izquierda de la superficie destino.
        """
        surf_rect = surface.get_rect()
        cam_x, cam_y = camera_offset

        start_x = max(0, cam_x // self.tile_w)
        start_y = max(0, cam_y // self.tile_h)
        end_x = min(self.width, (cam_x + surf_rect.width) // self.tile_w + 1)
        end_y = min(self.height, (cam_y + surf_rect.height) // self.tile_h + 1)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.grid[y][x]
                if tile is None:
                    continue
                px = x * self.tile_w - cam_x
                py = y * self.tile_h - cam_y
                tile.render(surface, (px, py), (self.tile_w, self.tile_h))

    def fill_from_path_grid(self, path_grid: List[List[Optional[str]]], default_orientation: float = 0.0):
        """Rellena la cuadrícula a partir de una matriz de rutas de imagen.

        Un `None` deja la celda vacía. Lanza FileNotFoundError si alguna ruta no existe.
        """
        if len(path_grid) != self.height or any(len(row) != self.width for row in path_grid):
            raise ValueError("path_grid size must match layout dimensions")
        for y, row in enumerate(path_grid):
            for x, path in enumerate(row):
                if path is None:
                    self.grid[y][x] = None
                else:
                    self.grid[y][x] = Tile.from_file(path, orientation=default_orientation)

    def fill_with_color(
        self,
        color: Tuple[int, ...],
        border_color: Optional[Tuple[int, ...]] = None,
        border_width: int = 1,
        orientation: float = 0.0,
        light: float = 1.0,
    ):
        """Rellena toda la cuadrícula con Tiles creados a partir de un color.

        Se crea un único `Tile` y se reutiliza en todas las celdas para ahorrar memoria.
        """
        tile = Tile.from_color(
            color,
            border_color=border_color,
            border_width=border_width,
            size=(self.tile_w, self.tile_h),
            orientation=orientation,
            light=light,
        )
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = tile
