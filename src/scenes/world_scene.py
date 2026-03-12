"""
世界地图场景 - 大地图界面
World Map Scene - Overworld map interface
"""

import pygame
import math
from typing import Dict, List, Optional
from .base_scene import BaseScene
from src.entities import City
from src.resource_loader import resource_loader
from src.animations import (
    AnimationManager, ScaleAnimation, FloatAnimation,
    ShakeAnimation, FadeAnimation, particle_system,
)
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GOLD,
    COLOR_BROWN, COLOR_DARK_GREEN, COLOR_SAND, COLOR_WATER,
    FONT_SIZE_NORMAL, FONT_SIZE_SMALL
)


class WorldScene(BaseScene):
    """世界地图场景"""

    def __init__(self, screen: pygame.Surface, game):
        super().__init__(screen)
        self.game = game
        self.cities: Dict[str, City] = {}
        self.selected_city: Optional[City] = None
        self.player_faction = "shu"  # 玩家势力
        self.turn = 1

        # 地图偏移（用于滚动）
        self.map_offset_x = 0
        self.map_offset_y = 0

        # 动画管理器
        self.animation_manager = AnimationManager()

        # 城市选择动画
        self.city_scale_anim: Optional[ScaleAnimation] = None

        # 浮动动画 - 用于选中的城市
        self.city_float = FloatAnimation(amplitude=3, frequency=2.0)

        # 震动动画 - 用于战斗提示
        self.shake_anim: Optional[ShakeAnimation] = None

        # 淡入动画
        self.fade_anim = FadeAnimation(fade_in=True, duration=0.5)

        # 按钮
        self.end_turn_btn = pygame.Rect(SCREEN_WIDTH - 120, 5, 110, 30)
        self.move_btn: Optional[pygame.Rect] = None
        self.recruit_btn: Optional[pygame.Rect] = None

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
        # 检查是否点击了结束回合按钮
        if self.end_turn_btn.collidepoint(pos):
            self._end_turn()
            return

        # 检查是否点击了城市信息面板的按钮
        if self.selected_city:
            if self.move_btn and self.move_btn.collidepoint(pos):
                self._move_to_city()
                return
            if self.recruit_btn and self.recruit_btn.collidepoint(pos):
                self._enter_city()
                return

        # 检查是否点击了城市
        for city in self.cities.values():
            if city.is_clicked(pos):
                self.selected_city = city
                # 播放点击音效和动画
                resource_loader.play_sound("click.wav")
                self.city_scale_anim = ScaleAnimation(start_scale=0.8, end_scale=1.0, duration=0.3)
                # 添加粒子效果
                particle_system.emit_explosion(city.x, city.y, COLOR_GOLD, count=15)
                return

        # 如果点击了空白处，不取消选择（保持当前选择）

    def _end_turn(self):
        """结束回合"""
        resource_loader.play_sound("march.wav")
        self.turn += 1
        # 所有城市执行回合结束处理
        for city in self.cities.values():
            city.end_turn()
        # 添加震动效果
        self.shake_anim = ShakeAnimation(intensity=5, duration=0.3)

    def _move_to_city(self):
        """移动到城市（进入城市管理界面）"""
        if self.selected_city:
            # 检查是否是玩家的城市
            if self.selected_city.owner == self.player_faction:
                resource_loader.play_sound("click.wav")
                self.game.current_city = self.selected_city
                self.next_scene = "city"
                self.running = False

    def _enter_city(self):
        """进入城市"""
        resource_loader.play_sound("click.wav")
        self._move_to_city()

    def update(self, delta_time: float):
        """更新逻辑"""
        # 更新动画
        if self.city_scale_anim:
            self.city_scale_anim.update(delta_time)
        self.city_float.update(delta_time)
        if self.shake_anim:
            self.shake_anim.update(delta_time)
        self.fade_anim.update(delta_time)
        self.animation_manager.update(delta_time)

        # 更新粒子系统
        particle_system.update(delta_time)

        # 世界地图场景的更新逻辑

    def draw(self):
        """绘制场景"""
        # 应用震动效果
        shake_offset = (0, 0)
        if self.shake_anim and not self.shake_anim.is_complete:
            shake_offset = self.shake_anim.get_offset()

        # 绘制背景
        self.screen.fill(COLOR_SAND)

        # 绘制地形
        self._draw_terrain()

        # 绘制连接道路
        self._draw_roads()

        # 绘制城市（带动画）
        for city in self.cities.values():
            scale = 1.0
            offset_y = 0

            # 选中城市的动画效果
            if self.selected_city == city:
                if self.city_scale_anim and not self.city_scale_anim.is_complete:
                    scale = self.city_scale_anim.get_scale()
                # 浮动效果
                offset_y = self.city_float.get_offset()

            city.draw(self.screen, scale=scale, offset_y=offset_y)

        # 绘制 UI
        self._draw_ui()

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
        turn_text = font.render(f"第 {self.turn} 回合", True, COLOR_WHITE)
        turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(turn_text, turn_rect)

        # 结束回合按钮
        pygame.draw.rect(self.screen, COLOR_GOLD, self.end_turn_btn)
        end_text = resource_loader.get_font(FONT_SIZE_SMALL).render("结束回合", True, COLOR_BLACK)
        self.screen.blit(end_text, (SCREEN_WIDTH - 95, 13))

        # 如果选择了城市，显示城市信息
        if self.selected_city:
            self._draw_city_info()

    def _draw_city_info(self):
        """绘制城市信息面板"""
        panel_width = 250
        panel_height = 220
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

        # 势力
        faction_names = {"shu": "蜀", "wei": "魏", "wu": "吴", "neutral": "中立"}
        faction_text = small_font.render(f"势力：{faction_names.get(self.selected_city.owner, '未知')}", True, COLOR_WHITE)
        self.screen.blit(faction_text, (panel_x + 10, y_offset))
        y_offset += 25

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

        # 移动/进入按钮
        self.move_btn = pygame.Rect(panel_x + 10, btn_y, btn_width, btn_height)
        is_player_city = self.selected_city.owner == self.player_faction
        move_color = (100, 150, 100) if is_player_city else (100, 100, 100)
        pygame.draw.rect(self.screen, move_color, self.move_btn)
        move_text = small_font.render("进入" if is_player_city else "移动", True, COLOR_WHITE)
        self.screen.blit(move_text, (panel_x + 25, btn_y + 7))

        # 招兵按钮（只有玩家城市可用）
        self.recruit_btn = pygame.Rect(panel_x + 90, btn_y, btn_width, btn_height)
        pygame.draw.rect(self.screen, move_color if is_player_city else (100, 100, 100), self.recruit_btn)
        recruit_text = small_font.render("招兵", True, COLOR_WHITE)
        self.screen.blit(recruit_text, (panel_x + 105, btn_y + 7))
