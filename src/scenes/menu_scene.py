"""
主菜单场景 - 游戏主菜单界面
Menu Scene - Main menu interface
"""

import pygame
import math
import random
from typing import List, Tuple
from .base_scene import BaseScene
from src.resource_loader import resource_loader
from src.animations import (
    FadeAnimation, PulseAnimation, FloatAnimation,
    AnimationManager, EasingType, particle_system,
)
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GOLD,
    COLOR_BLACK, GAME_TITLE, GAME_VERSION, FONT_SIZE_TITLE,
    FONT_SIZE_NORMAL, FONT_SIZE_SMALL
)


class MenuItem:
    """菜单项"""

    def __init__(self, text: str, callback: callable, position: Tuple[int, int]):
        self.text = text
        self.callback = callback
        self.position = position
        self.rect: pygame.Rect = None
        self.is_hovered = False
        self.is_selected = False

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, scale: float = 1.0):
        """绘制菜单项"""
        color = COLOR_GOLD if self.is_hovered or self.is_selected else COLOR_WHITE
        text_surface = font.render(self.text, True, color)

        if scale != 1.0:
            # 缩放文字
            text_surface = pygame.transform.scale(text_surface, (
                int(text_surface.get_width() * scale),
                int(text_surface.get_height() * scale)
            ))

        text_rect = text_surface.get_rect(center=self.position)
        self.rect = text_rect

        # 绘制背景
        if self.is_hovered or self.is_selected:
            bg_rect = text_rect.inflate(40, 10)
            pygame.draw.rect(screen, (50, 50, 50, 128), bg_rect)

        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos: Tuple[int, int]) -> bool:
        """检查鼠标悬停"""
        if self.rect:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """检查是否被点击"""
        if self.rect and self.rect.collidepoint(mouse_pos):
            self.callback()
            return True
        return False


class MenuScene(BaseScene):
    """主菜单场景"""

    def __init__(self, screen: pygame.Surface, game):
        super().__init__(screen)
        self.game = game
        self.menu_items: List[MenuItem] = []

        # 动画管理器
        self.animation_manager = AnimationManager()

        # 浮动动画 - 用于标题
        self.title_float = FloatAnimation(amplitude=5, frequency=1.5, start_phase=0)

        # 脉动动画 - 用于菜单项
        self.item_pulse = PulseAnimation(start_scale=1.0, end_scale=1.05, duration=1.5)

        # 淡入动画
        self.fade_anim = FadeAnimation(fade_in=True, duration=0.5)

        # 初始化菜单项
        self._init_menu_items()

        # 播放背景音乐
        resource_loader.play_music("bgm_main.wav", loops=-1)

    def _init_menu_items(self):
        """初始化菜单项"""
        font_large = resource_loader.get_font(FONT_SIZE_NORMAL)

        # 菜单项配置
        menu_config = [
            ("开始游戏", self._start_game, (SCREEN_WIDTH // 2, 350)),
            ("载入游戏", self._load_game, (SCREEN_WIDTH // 2, 420)),
            ("游戏设置", self._settings, (SCREEN_WIDTH // 2, 490)),
            ("退出游戏", self._quit_game, (SCREEN_WIDTH // 2, 560)),
        ]

        for text, callback, position in menu_config:
            item = MenuItem(text, callback, position)
            self.menu_items.append(item)

    def _start_game(self):
        """开始游戏"""
        resource_loader.play_sound("click.wav")
        # 添加淡出动画
        self.fade_anim = FadeAnimation(fade_in=False, duration=0.3, on_complete=lambda: setattr(self, '_pending_start_game', True))

    def _execute_start_game(self):
        """执行开始游戏（动画完成后）"""
        self.next_scene = "world"

    def _load_game(self):
        """载入游戏"""
        resource_loader.play_sound("click.wav")
        # TODO: 实现存档系统
        print("载入游戏 - 待实现")

    def _settings(self):
        """游戏设置"""
        resource_loader.play_sound("click.wav")
        # TODO: 实现设置界面
        print("游戏设置 - 待实现")

    def _quit_game(self):
        """退出游戏"""
        resource_loader.play_sound("click.wav")
        # 添加淡出动画
        self.fade_anim = FadeAnimation(fade_in=False, duration=0.3, on_complete=lambda: setattr(self, '_pending_quit_game', True))

    def _execute_quit_game(self):
        """执行退出游戏（动画完成后）"""
        self.running = False
        self.next_scene = None

    def handle_events(self, events: list):
        """处理事件"""
        for event in events:
            self.handle_event(event)

            if event.type == pygame.MOUSEMOTION:
                for item in self.menu_items:
                    item.check_hover(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    for item in self.menu_items:
                        if item.clicked(event.pos):
                            return

    def update(self, delta_time: float):
        """更新逻辑"""
        # 更新动画
        self.title_float.update(delta_time)
        self.item_pulse.update(delta_time)
        self.fade_anim.update(delta_time)
        self.animation_manager.update(delta_time)

        # 更新粒子系统
        particle_system.update(delta_time)

        # 检查淡出动画完成后的操作
        if self.fade_anim.is_complete:
            if hasattr(self, '_pending_start_game') and self._pending_start_game:
                self._execute_start_game()
                delattr(self, '_pending_start_game')
            if hasattr(self, '_pending_quit_game') and self._pending_quit_game:
                self._execute_quit_game()
                delattr(self, '_pending_quit_game')

    def draw(self):
        """绘制场景"""
        # 绘制背景
        self.screen.fill((30, 30, 50))

        # 绘制背景装饰 - 星星
        self._draw_stars()

        # 绘制游戏标题 (带浮动动画)
        title_font = resource_loader.get_font(FONT_SIZE_TITLE)
        title_offset = self.title_float.get_offset()
        title_text = title_font.render(GAME_TITLE, True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200 + title_offset))
        self.screen.blit(title_text, title_rect)

        # 绘制版本号
        version_font = resource_loader.get_font(FONT_SIZE_SMALL)
        version_text = version_font.render(f"v{GAME_VERSION}", True, COLOR_WHITE)
        version_rect = version_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(version_text, version_rect)

        # 绘制菜单项 (带脉动动画)
        pulse_scale = self.item_pulse.get_scale()
        for i, item in enumerate(self.menu_items):
            # 交错脉动效果
            phase = i * 0.2
            item_scale = 1.0 + (pulse_scale - 1.0) * math.sin(phase)
            if item.is_hovered:
                item_scale = 1.1

            item.draw(self.screen, resource_loader.get_font(FONT_SIZE_NORMAL), scale=item_scale)

        # 绘制装饰边框
        border_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_GOLD, border_rect, 3)

        # 绘制粒子效果
        particle_system.draw(self.screen)

        # 绘制淡入淡出效果
        if not self.fade_anim.is_complete:
            alpha = self.fade_anim.get_alpha()
            if alpha > 0:
                fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(alpha)
                self.screen.blit(fade_surface, (0, 0))

        pygame.display.flip()

    def _draw_stars(self):
        """绘制背景星星装饰"""
        current_time = pygame.time.get_ticks()
        random.seed(current_time // 1000)  # 每秒重新播种以保持稳定

        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            size = random.randint(1, 2)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), size)
