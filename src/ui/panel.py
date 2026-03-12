"""
UI 面板组件 - 可复用的面板
UI Panel Component - Reusable panel
"""

import pygame
from typing import Optional, Tuple, List
from src.resource_loader import resource_loader
from src.config import COLOR_WHITE, COLOR_GOLD, COLOR_BLACK, FONT_SIZE_NORMAL, FONT_SIZE_SMALL


class Panel:
    """面板组件"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str = "",
        bg_color: Tuple[int, int, int] = (40, 40, 60),
        border_color: Tuple[int, int, int] = COLOR_GOLD,
        border_width: int = 2,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width

        self.content: List[str] = []
        self.buttons: List = []

    def add_content(self, text: str):
        """添加文本内容"""
        self.content.append(text)

    def clear_content(self):
        """清空内容"""
        self.content.clear()

    def add_button(self, button):
        """添加按钮到面板"""
        self.buttons.append(button)

    def handle_events(self, events: list) -> bool:
        """处理事件"""
        for event in events:
            for button in self.buttons:
                if button.handle_event(event):
                    return True
        return False

    def draw(self, screen: pygame.Surface):
        """绘制面板"""
        # 绘制背景
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # 绘制边框
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)

        # 绘制标题
        if self.title:
            font = resource_loader.get_font(FONT_SIZE_NORMAL)
            title_surface = font.render(self.title, True, COLOR_GOLD)
            screen.blit(title_surface, (self.rect.x + 10, self.rect.y + 10))

        # 绘制内容
        y_offset = self.rect.y + 40
        font_small = resource_loader.get_font(FONT_SIZE_SMALL)

        for line in self.content:
            text_surface = font_small.render(line, True, COLOR_WHITE)
            screen.blit(text_surface, (self.rect.x + 10, y_offset))
            y_offset += 25

        # 绘制按钮
        for button in self.buttons:
            button.draw(screen)


class InfoPanel(Panel):
    """信息面板 - 用于显示信息"""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        super().__init__(x, y, width, height, title)
        self.bg_color = (30, 30, 50)

    def set_info(self, info_dict: dict):
        """设置信息显示"""
        self.clear_content()
        for key, value in info_dict.items():
            self.add_content(f"{key}: {value}")


class SelectionPanel(Panel):
    """选择面板 - 用于选项列表"""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        super().__init__(x, y, width, height, title)
        self.selected_index = -1
        self.options: List[str] = []

    def set_options(self, options: List[str]):
        """设置选项列表"""
        self.options = options
        self.selected_index = -1

    def draw(self, screen: pygame.Surface):
        """绘制选择面板"""
        super().draw(screen)

        # 绘制选项高亮
        if 0 <= self.selected_index < len(self.options):
            font = resource_loader.get_font(FONT_SIZE_SMALL)
            y_offset = self.rect.y + 40 + self.selected_index * 25
            highlight_rect = pygame.Rect(self.rect.x + 5, y_offset - 3, self.rect.width - 10, 20)
            pygame.draw.rect(screen, (60, 60, 100), highlight_rect)
