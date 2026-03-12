"""
场景基类 - 所有游戏场景的父类
Base Scene - Parent class for all game scenes
"""

import pygame
from abc import ABC, abstractmethod
from typing import Optional


class BaseScene(ABC):
    """场景基类"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.running = True
        self.next_scene: Optional[str] = None

    @abstractmethod
    def handle_events(self, events: list):
        """处理事件"""
        pass

    @abstractmethod
    def update(self, delta_time: float):
        """更新逻辑"""
        pass

    @abstractmethod
    def draw(self):
        """绘制场景"""
        pass

    def handle_event(self, event: pygame.event.Event):
        """处理单个事件，子类可重写"""
        if event.type == pygame.QUIT:
            self.running = False
            self.next_scene = None  # 退出游戏

    def quit_scene(self):
        """退出当前场景"""
        self.running = False
