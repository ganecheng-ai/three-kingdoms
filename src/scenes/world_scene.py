"""
世界地图场景 - 大地图界面
World Map Scene - Overworld map interface
"""

import pygame
import math
from typing import Dict, List, Optional
from .base_scene import BaseScene
from src.resource_loader import resource_loader
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GOLD,
    COLOR_BROWN, COLOR_DARK_GREEN, COLOR_SAND, COLOR_WATER,
    FONT_SIZE_NORMAL, FONT_SIZE_SMALL
)


class City:
    """城市类"""

    def __init__(self, name: str, x: int, y: int, owner: str = "neutral"):
        self.name = name
        self.x = x
        self.y = y
        self.owner = owner  # "wei", "shu", "wu", "neutral"
        self.population = 10000
        self.gold = 1000
        self.food = 1000
        self.soldiers = 1000
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)

        # 势力颜色
        self.owner_colors = {
            "wei": (100, 100, 200),  # 魏 - 蓝色
            "shu": (100, 200, 100),  # 蜀 - 绿色
            "wu": (200, 100, 100),   # 吴 - 红色
            "neutral": COLOR_BROWN    # 中立 - 棕色
        }

    def draw(self, screen: pygame.Surface):
        """绘制城市"""
        # 绘制城市区域
        color = self.owner_colors.get(self.owner, COLOR_BROWN)
        pygame.draw.circle(screen, color, (self.x, self.y), 25)
        pygame.draw.circle(screen, COLOR_WHITE, (self.x, self.y), 25, 2)

        # 绘制城市名称
        font = resource_loader.get_font(FONT_SIZE_SMALL)
        name_text = font.render(self.name, True, COLOR_WHITE)
        name_rect = name_text.get_rect(center=(self.x, self.y - 40))
        screen.blit(name_text, name_rect)

        # 绘制兵力
        soldier_text = font.render(f"{self.soldiers}", True, COLOR_WHITE)
        soldier_rect = soldier_text.get_rect(center=(self.x, self.y + 45))
        screen.blit(soldier_text, soldier_rect)

    def is_clicked(self, pos: tuple) -> bool:
        """检查是否被点击"""
        return self.rect.collidepoint(pos)


class WorldScene(BaseScene):
    """世界地图场景"""

    def __init__(self, screen: pygame.Surface, game):
        super().__init__(screen)
        self.game = game
        self.cities: Dict[str, City] = {}
        self.selected_city: Optional[City] = None
        self.player_faction = "shu"  # 玩家势力

        # 地图偏移（用于滚动）
        self.map_offset_x = 0
        self.map_offset_y = 0

        # 初始化城市
        self._init_cities()

    def _init_cities(self):
        """初始化三国城市"""
        # 魏国城市
        self.cities["luoyang"] = City("洛阳", 400, 300, "wei")
        self.cities["chang_an"] = City("长安", 350, 280, "wei")
        self.cities["xu_chang"] = City("许昌", 450, 320, "wei")
        self.cities["ye_cheng"] = City("邺城", 480, 280, "wei")

        # 蜀国城市
        self.cities["cheng_du"] = City("成都", 250, 400, "shu")
        self.cities["mian_zhu"] = City("绵竹", 270, 380, "shu")
        self.cities["han_zhong"] = City("汉中", 300, 350, "shu")
        self.cities["yong_an"] = City("永安", 350, 450, "shu")

        # 吴国城市
        self.cities["jian_ye"] = City("建业", 550, 400, "wu")
        self.cities["wu_chang"] = City("武昌", 500, 380, "wu")
        self.cities["chai_sang"] = City("柴桑", 520, 420, "wu")
        self.cities["mo_ling"] = City("秣陵", 580, 390, "wu")

        # 中立城市
        self.cities["jing_zhou"] = City("荆州", 450, 400, "neutral")
        self.cities["xiang_yang"] = City("襄阳", 420, 370, "neutral")

    def handle_events(self, events: list):
        """处理事件"""
        for event in events:
            self.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    self._handle_left_click(event.pos)
                elif event.button == 3:  # 右键点击
                    self.selected_city = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = "menu"
                    self.running = False

    def _handle_left_click(self, pos: tuple):
        """处理左键点击"""
        # 检查是否点击了城市
        for city in self.cities.values():
            if city.is_clicked(pos):
                self.selected_city = city
                break

        # 如果点击了空白处，取消选择
        if not self.selected_city or not self.selected_city.is_clicked(pos):
            pass  # 保持当前选择

    def update(self, delta_time: float):
        """更新逻辑"""
        # 世界地图场景的更新逻辑
        pass

    def draw(self):
        """绘制场景"""
        # 绘制背景
        self.screen.fill(COLOR_SAND)

        # 绘制地形
        self._draw_terrain()

        # 绘制城市
        for city in self.cities.values():
            city.draw(self.screen)

        # 绘制连接道路
        self._draw_roads()

        # 绘制 UI
        self._draw_ui()

        pygame.display.flip()

    def _draw_terrain(self):
        """绘制地形"""
        # 绘制水域
        water_areas = [
            pygame.Rect(600, 0, 200, SCREEN_HEIGHT),  # 东海
            pygame.Rect(0, 500, SCREEN_WIDTH, 50),    # 长江
        ]
        for water in water_areas:
            pygame.draw.rect(self.screen, COLOR_WATER, water)

        # 绘制山脉
        mountain_positions = [
            (200, 200), (300, 180), (350, 200),
            (150, 300), (200, 320),
        ]
        for mx, my in mountain_positions:
            pygame.draw.circle(self.screen, (100, 80, 60), (mx, my), 30)

    def _draw_roads(self):
        """绘制道路"""
        # 简单连接相邻城市
        city_list = list(self.cities.values())
        for i, city1 in enumerate(city_list):
            for city2 in city_list[i+1:]:
                distance = math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)
                if distance < 100:
                    pygame.draw.line(self.screen, COLOR_BROWN,
                                   (city1.x, city1.y), (city2.x, city2.y), 2)

    def _draw_ui(self):
        """绘制 UI"""
        # 顶部信息栏
        pygame.draw.rect(self.screen, (50, 50, 80), (0, 0, SCREEN_WIDTH, 40))
        pygame.draw.line(self.screen, COLOR_GOLD, (0, 40), (SCREEN_WIDTH, 40), 2)

        # 玩家势力信息
        font = resource_loader.get_font(FONT_SIZE_NORMAL)
        faction_names = {"shu": "蜀", "wei": "魏", "wu": "吴"}
        player_text = font.render(f"势力：{faction_names.get(self.player_faction, '未知')}", True, COLOR_WHITE)
        self.screen.blit(player_text, (10, 8))

        # 回合信息
        turn_text = font.render("第 1 回合", True, COLOR_WHITE)
        turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(turn_text, turn_rect)

        # 右侧按钮
        end_turn_btn = pygame.Rect(SCREEN_WIDTH - 120, 5, 110, 30)
        pygame.draw.rect(self.screen, COLOR_GOLD, end_turn_btn)
        end_text = resource_loader.get_font(FONT_SIZE_SMALL).render("结束回合", True, COLOR_BLACK)
        self.screen.blit(end_text, (SCREEN_WIDTH - 95, 13))

        # 如果选择了城市，显示城市信息
        if self.selected_city:
            self._draw_city_info()

    def _draw_city_info(self):
        """绘制城市信息面板"""
        panel_width = 250
        panel_height = 200
        panel_x = SCREEN_WIDTH - panel_width - 20
        panel_y = 60

        # 面板背景
        pygame.draw.rect(self.screen, (40, 40, 60),
                        (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, COLOR_GOLD,
                        (panel_x, panel_y, panel_width, panel_height), 2)

        font = resource_loader.get_font(FONT_SIZE_NORMAL)
        small_font = resource_loader.get_font(FONT_SIZE_SMALL)

        y_offset = panel_y + 10

        # 城市名称
        title = font.render(self.selected_city.name, True, COLOR_GOLD)
        self.screen.blit(title, (panel_x + 10, y_offset))
        y_offset += 35

        # 人口
        pop_text = small_font.render(f"人口：{self.selected_city.population}", True, COLOR_WHITE)
        self.screen.blit(pop_text, (panel_x + 10, y_offset))
        y_offset += 25

        # 兵力
        soldier_text = small_font.render(f"兵力：{self.selected_city.soldiers}", True, COLOR_WHITE)
        self.screen.blit(soldier_text, (panel_x + 10, y_offset))
        y_offset += 25

        # 金钱
        gold_text = small_font.render(f"金钱：{self.selected_city.gold}", True, COLOR_WHITE)
        self.screen.blit(gold_text, (panel_x + 10, y_offset))
        y_offset += 25

        # 粮草
        food_text = small_font.render(f"粮草：{self.selected_city.food}", True, COLOR_WHITE)
        self.screen.blit(food_text, (panel_x + 10, y_offset))
        y_offset += 35

        # 操作按钮
        btn_width = 70
        btn_height = 30
        btn_y = y_offset

        # 移动按钮
        move_btn = pygame.Rect(panel_x + 10, btn_y, btn_width, btn_height)
        pygame.draw.rect(self.screen, (100, 100, 150), move_btn)
        move_text = small_font.render("移动", True, COLOR_WHITE)
        self.screen.blit(move_text, (panel_x + 25, btn_y + 7))

        # 招兵按钮
        recruit_btn = pygame.Rect(panel_x + 90, btn_y, btn_width, btn_height)
        pygame.draw.rect(self.screen, (100, 150, 100), recruit_btn)
        recruit_text = small_font.render("招兵", True, COLOR_WHITE)
        self.screen.blit(recruit_text, (panel_x + 105, btn_y + 7))
