"""
城市场景 - 城市管理界面
City Scene - City management interface
"""

import pygame
from typing import Optional
from .base_scene import BaseScene
from src.resource_loader import resource_loader
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GOLD,
    COLOR_BLACK, COLOR_BROWN, FONT_SIZE_LARGE, FONT_SIZE_NORMAL,
    FONT_SIZE_SMALL
)


class CityScene(BaseScene):
    """城市场景"""

    def __init__(self, screen: pygame.Surface, game, city=None):
        super().__init__(screen)
        self.game = game
        self.city = city
        self.selected_tab = "overview"  # overview, recruit, build, general

        # 按钮区域
        self.buttons = {}

    def handle_events(self, events: list):
        """处理事件"""
        for event in events:
            self.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = "world"
                    self.running = False

    def _handle_click(self, pos: tuple):
        """处理点击"""
        # 返回按钮
        back_rect = pygame.Rect(10, 10, 80, 35)
        if back_rect.collidepoint(pos):
            self.next_scene = "world"
            self.running = False

        # 标签页按钮
        tabs = [
            ("overview", "概况", 150),
            ("recruit", "招兵", 250),
            ("build", "建设", 350),
            ("general", "武将", 450),
        ]

        for tab_id, _, x in tabs:
            btn_rect = pygame.Rect(x, 60, 80, 35)
            if btn_rect.collidepoint(pos):
                self.selected_tab = tab_id
                break

    def update(self, delta_time: float):
        """更新逻辑"""
        pass

    def draw(self):
        """绘制场景"""
        # 背景
        self.screen.fill((60, 50, 40))

        # 绘制标题栏
        self._draw_header()

        # 绘制标签页
        self._draw_tabs()

        # 绘制内容区域
        self._draw_content()

        pygame.display.flip()

    def _draw_header(self):
        """绘制标题栏"""
        pygame.draw.rect(self.screen, (40, 40, 60), (0, 0, SCREEN_WIDTH, 50))
        pygame.draw.line(self.screen, COLOR_GOLD, (0, 50), (SCREEN_WIDTH, 50), 2)

        # 返回按钮
        back_rect = pygame.Rect(10, 10, 80, 35)
        pygame.draw.rect(self.screen, (150, 50, 50), back_rect)
        back_text = resource_loader.get_font(FONT_SIZE_NORMAL).render("返回", True, COLOR_WHITE)
        self.screen.blit(back_text, (25, 17))

        # 城市名称
        if self.city:
            title_font = resource_loader.get_font(FONT_SIZE_LARGE)
            title = title_font.render(f"{self.city.name}城", True, COLOR_GOLD)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 25))
            self.screen.blit(title, title_rect)

    def _draw_tabs(self):
        """绘制标签页"""
        tabs = [
            ("overview", "概况"),
            ("recruit", "招兵"),
            ("build", "建设"),
            ("general", "武将"),
        ]

        for i, (tab_id, text) in enumerate(tabs):
            x = 150 + i * 100
            color = COLOR_GOLD if self.selected_tab == tab_id else (100, 100, 100)
            btn_rect = pygame.Rect(x, 60, 80, 35)
            pygame.draw.rect(self.screen, color, btn_rect)
            btn_text = resource_loader.get_font(FONT_SIZE_NORMAL).render(text, True, COLOR_BLACK)
            self.screen.blit(btn_text, (x + 15, 67))

    def _draw_content(self):
        """绘制内容区域"""
        if self.selected_tab == "overview":
            self._draw_overview()
        elif self.selected_tab == "recruit":
            self._draw_recruit()
        elif self.selected_tab == "build":
            self._draw_build()
        elif self.selected_tab == "general":
            self._draw_generals()

    def _draw_overview(self):
        """绘制概况"""
        if not self.city:
            return

        font = resource_loader.get_font(FONT_SIZE_NORMAL)
        small_font = resource_loader.get_font(FONT_SIZE_SMALL)

        y = 120
        info_items = [
            ("人口", self.city.population),
            ("兵力", self.city.soldiers),
            ("金钱", self.city.gold),
            ("粮草", self.city.food),
        ]

        for label, value in info_items:
            label_text = font.render(f"{label}:", True, COLOR_WHITE)
            self.screen.blit(label_text, (100, y))

            value_text = font.render(str(value), True, COLOR_GOLD)
            self.screen.blit(value_text, (250, y))
            y += 50

        # 城市装饰
        city_rect = pygame.Rect(500, 120, 300, 200)
        pygame.draw.rect(self.screen, (80, 70, 60), city_rect)
        pygame.draw.rect(self.screen, COLOR_GOLD, city_rect, 2)

        city_label = small_font.render("城市预览", True, COLOR_WHITE)
        self.screen.blit(city_label, (580, 200))

    def _draw_recruit(self):
        """绘制招兵界面"""
        if not self.city:
            return

        font = resource_loader.get_font(FONT_SIZE_NORMAL)

        y = 120
        troops = [
            ("步兵", 100, 10),  # 名称，价格，数量
            ("骑兵", 200, 5),
            ("弓兵", 150, 8),
            ("战车", 500, 2),
        ]

        for name, cost, available in troops:
            # 兵种名称
            name_text = font.render(f"{name}", True, COLOR_WHITE)
            self.screen.blit(name_text, (100, y))

            # 价格
            cost_text = font.render(f"价格：{cost}金", True, COLOR_GOLD)
            self.screen.blit(cost_text, (250, y))

            # 可招募数量
            avail_text = font.render(f"可招募：{available}", True, COLOR_WHITE)
            self.screen.blit(avail_text, (400, y))

            # 招募按钮
            btn_rect = pygame.Rect(550, y, 80, 30)
            pygame.draw.rect(self.screen, (100, 150, 100), btn_rect)
            recruit_text = font.render("招募", True, COLOR_WHITE)
            self.screen.blit(recruit_text, (565, y + 5))

            y += 50

    def _draw_build(self):
        """绘制建设界面"""
        font = resource_loader.get_font(FONT_SIZE_NORMAL)

        y = 120
        buildings = [
            ("农田", "增加粮草产量", 200),
            ("市集", "增加金钱收入", 200),
            ("兵营", "加快招兵速度", 300),
            ("城墙", "提升城防", 500),
            ("武馆", "训练武将", 400),
        ]

        for name, desc, cost in buildings:
            # 建筑名称
            name_text = font.render(f"{name}", True, COLOR_WHITE)
            self.screen.blit(name_text, (100, y))

            # 描述
            desc_text = font.render(desc, True, (150, 150, 150))
            self.screen.blit(desc_text, (250, y))

            # 造价
            cost_text = font.render(f"{cost}金", True, COLOR_GOLD)
            self.screen.blit(cost_text, (550, y))

            # 建造按钮
            btn_rect = pygame.Rect(650, y, 80, 30)
            pygame.draw.rect(self.screen, (100, 150, 100), btn_rect)
            build_text = font.render("建造", True, COLOR_WHITE)
            self.screen.blit(build_text, (665, y + 5))

            y += 50

    def _draw_generals(self):
        """绘制武将界面"""
        font = resource_loader.get_font(FONT_SIZE_NORMAL)

        # 提示文字
        tip_text = font.render("武将系统开发中...", True, COLOR_WHITE)
        tip_rect = tip_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(tip_text, tip_rect)
