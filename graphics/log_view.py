"""LogView: vista de log/chat simple para Pygame.

Provee:
- `LogView`: clase que encapsula mensajes, render y visibilidad.
- `set_bottom_right` para posicionar en la esquina inferior derecha.
- `show` / `hide` para controlar visibilidad.
- `add_message` y `load_from_file` para cargar entradas.
"""
from __future__ import annotations

from typing import List, Tuple, Optional
import os
import pygame


class LogView:
    def __init__(self, font_name: Optional[str] = None, font_size: int = 16, padding: int = 8, bg_color=(0, 0, 0, 180), text_color=(255,255,255)):
        pygame.font.init()
        self.font = pygame.font.Font(font_name, font_size)
        self.padding = padding
        self.bg_color = bg_color
        self.text_color = text_color

        self.messages: List[str] = []
        self.visible: bool = True

        # rect y superficie se crean en set_bottom_right
        self.rect: Optional[pygame.Rect] = None
        self.surface: Optional[pygame.Surface] = None

    def set_bottom_right(self, screen_size: Tuple[int, int], margin: Tuple[int, int] = (10, 10), width_ratio: float = 0.4, height_ratio: float = 0.45):
        """Posiciona la vista en la esquina inferior derecha.

        - `width_ratio` fracción del ancho de la pantalla.
        - `height_ratio` fracción de la altura usada (por debajo de la mitad).
        """
        sw, sh = screen_size
        w = max(120, int(sw * width_ratio))
        h = max(80, int(sh * height_ratio))
        x = sw - margin[0] - w
        y = sh - margin[1] - h

        self.rect = pygame.Rect(x, y, w, h)
        # Superficie con alpha para fondo translucido
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def toggle(self):
        self.visible = not self.visible

    def add_message(self, msg: str) -> None:
        """Añade un mensaje al log (aplica strip)."""
        text = str(msg).rstrip("\n")
        self.messages.append(text)
        # limitar histórico razonable
        if len(self.messages) > 500:
            self.messages = self.messages[-500:]

    def load_from_file(self, path: str) -> None:
        """Lee líneas desde `path` y las añade al log (si existe)."""
        if not os.path.isfile(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                self.add_message(line.strip())

    def clear(self):
        self.messages.clear()

    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        words = text.split(" ")
        lines: List[str] = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if self.font.size(test)[0] <= max_width - 2 * self.padding:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def render(self, target: pygame.Surface) -> None:
        """Dibuja el log en `target` si está visible. Los mensajes más recientes aparecen abajo."""
        if not self.visible or self.surface is None or self.rect is None:
            return

        w, h = self.surface.get_size()
        # Clear background
        self.surface.fill((0, 0, 0, 0))
        # Draw translucent background
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill(self.bg_color)
        self.surface.blit(bg, (0, 0))

        # Prepare lines wrapped
        all_lines: List[str] = []
        for msg in self.messages:
            wrapped = self._wrap_text(msg, w)
            all_lines.extend(wrapped)

        # Render from bottom up until space runs out
        line_height = self.font.get_linesize()
        max_lines = (h - 2 * self.padding) // line_height
        lines_to_draw = all_lines[-max_lines:]

        y = h - self.padding - line_height * len(lines_to_draw)
        for line in lines_to_draw:
            surf_line = self.font.render(line, True, self.text_color)
            self.surface.blit(surf_line, (self.padding, y))
            y += line_height

        # Blit final surface to target
        target.blit(self.surface, (self.rect.x, self.rect.y))
