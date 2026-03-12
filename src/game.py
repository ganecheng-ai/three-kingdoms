"""
游戏核心 - 管理游戏状态和场景切换
Game Core - Manage game state and scene transitions
"""

import pygame
from typing import Dict, Type, Optional
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
from src.resource_loader import resource_loader
from src.scenes.base_scene import BaseScene
from src.scenes.menu_scene import MenuScene
from src.scenes.world_scene import WorldScene
from src.scenes.city_scene import CityScene
from src.scenes.battle_scene import BattleScene


class Game:
    """游戏主类"""

    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        pygame.mixer.init()

        # 创建窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        # 时钟
        self.clock = pygame.time.Clock()

        # 游戏状态
        self.running = True
        self.current_scene: Optional[BaseScene] = None
        self.scene_stack: list = []

        # 场景注册
        self.scenes: Dict[str, Type[BaseScene]] = {
            "menu": MenuScene,
            "world": WorldScene,
            "city": CityScene,
            "battle": BattleScene,
        }

        # 游戏数据
        self.player_faction = "shu"
        self.player_cities = []
        self.player_generals = []
        self.turn = 1

        # 初始化资源
        resource_loader.preload_resources()

    def switch_scene(self, scene_name: str):
        """切换场景"""
        if scene_name not in self.scenes:
            print(f"场景不存在：{scene_name}")
            return

        scene_class = self.scenes[scene_name]

        # 创建新场景
        if scene_name == "menu":
            self.current_scene = scene_class(self.screen, self)
        elif scene_name == "world":
            self.current_scene = scene_class(self.screen, self)
        elif scene_name == "city":
            # 传入当前选中的城市
            city = getattr(self.current_scene, 'selected_city', None) if self.current_scene else None
            self.current_scene = scene_class(self.screen, self, city)
        elif scene_name == "battle":
            attacker = getattr(self.current_scene, 'selected_city', None) if self.current_scene else None
            self.current_scene = scene_class(self.screen, self, attacker)
        else:
            self.current_scene = scene_class(self.screen, self)

    def push_scene(self, scene_name: str):
        """压入场景（用于子界面）"""
        if self.current_scene:
            self.scene_stack.append(self.current_scene)

        self.switch_scene(scene_name)

    def pop_scene(self):
        """弹出场景"""
        if self.scene_stack:
            self.current_scene = self.scene_stack.pop()

    def run(self):
        """运行游戏主循环"""
        # 从主菜单开始
        self.switch_scene("menu")

        while self.running:
            # 计算 delta time
            delta_time = self.clock.tick(FPS) / 1000.0

            # 处理事件
            if self.current_scene:
                events = pygame.event.get()
                self.current_scene.handle_events(events)

                # 检查场景切换
                if not self.current_scene.running:
                    if self.current_scene.next_scene is None:
                        # 退出游戏
                        self.running = False
                    else:
                        # 切换到新场景
                        next_scene = self.current_scene.next_scene
                        self.switch_scene(next_scene)
                    continue

                # 更新逻辑
                self.current_scene.update(delta_time)

                # 绘制
                self.current_scene.draw()

            # 更新显示
            pygame.display.flip()

        # 清理
        self.quit()

    def quit(self):
        """退出游戏"""
        pygame.quit()


