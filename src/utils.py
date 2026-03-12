"""
工具函数 - 游戏公共工具函数
Utility Functions - Common game utility functions
"""

import pygame
from src.resource_loader import resource_loader
from src.config import COLOR_WHITE, FONT_SIZE_SMALL


def draw_status_bar(
    screen: pygame.Surface,
    x: int,
    y: int,
    label: str,
    current: int,
    maximum: int,
    color: tuple,
    bar_width: int = 100,
    bar_height: int = 10,
    label_width: int = 35,
):
    """绘制状态条

    Args:
        screen: 屏幕 Surface
        x: X 坐标
        y: Y 坐标
        label: 标签文字
        current: 当前值
        maximum: 最大值
        color: 填充颜色
        bar_width: 条宽度
        bar_height: 条高度
        label_width: 标签宽度
    """
    small_font = resource_loader.get_font(FONT_SIZE_SMALL)

    # 标签
    label_text = small_font.render(f"{label}:", True, COLOR_WHITE)
    screen.blit(label_text, (x, y))

    # 背景条
    bar_x = x + label_width
    pygame.draw.rect(screen, (80, 80, 80), (bar_x, y + 2, bar_width, bar_height))

    # 实际条
    if maximum > 0:
        fill_width = int(bar_width * current / maximum)
        pygame.draw.rect(screen, color, (bar_x, y + 2, fill_width, bar_height))

    # 数值
    value_text = small_font.render(f"{current}/{maximum}", True, COLOR_WHITE)
    screen.blit(value_text, (bar_x + bar_width + 5, y))