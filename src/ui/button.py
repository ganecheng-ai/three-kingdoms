"""
UI 按钮组件 - 可复用的按钮
UI Button Component - Reusable button
"""

import pygame
from typing import Optional, Callable, Tuple
from src.resource_loader import resource_loader
from src.config import COLOR_WHITE, COLOR_GOLD, COLOR_BLACK, FONT_SIZE_NORMAL


class Button:
    """按钮组件"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        callback: Optional[Callable] = None,
        bg_color: Tuple[int, int, int] = (100, 100, 150),
        hover_color: Tuple[int, int, int] = (150, 150, 200),
        text_color: Tuple[int, int, int] = COLOR_WHITE,
        font_size: int = FONT_SIZE_NORMAL,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size

        self.is_hovered = False
        self.is_clicked = False
        self.enabled = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件，返回是否触发了点击"""
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_clicked = True
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_hovered and self.is_clicked:
                if self.callback:
                    self.callback()
                return True
            self.is_clicked = False

        return False

    def draw(self, screen: pygame.Surface):
        """绘制按钮"""
        # 选择颜色
        if not self.enabled:
            color = (80, 80, 80)  # 禁用状态
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.bg_color

        # 绘制按钮背景
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_GOLD, self.rect, 2)

        # 绘制按钮文字
        font = resource_loader.get_font(self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def set_position(self, x: int, y: int):
        """设置位置"""
        self.rect.x = x
        self.rect.y = y

    def set_enabled(self, enabled: bool):
        """设置启用状态"""
        self.enabled = enabled
