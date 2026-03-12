"""
战斗场景 - 战斗界面
Battle Scene - Battle interface
"""

import pygame
import random
from typing import List, Optional
from .base_scene import BaseScene
from src.resource_loader import resource_loader
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GOLD,
    COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_BLACK,
    FONT_SIZE_LARGE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL
)


class Unit:
    """战斗单位"""

    def __init__(self, name: str, x: int, y: int, faction: str, soldiers: int = 1000):
        self.name = name
        self.x = x
        self.y = y
        self.faction = faction  # "player" or "enemy"
        self.soldiers = soldiers
        self.max_soldiers = soldiers
        self.attack = 50
        self.defense = 30
        self.morale = 100  # 士气

        # 颜色
        self.color = COLOR_GREEN if faction == "player" else COLOR_RED

        # 动画
        self.is_attacking = False
        self.attack_frame = 0

    def draw(self, screen: pygame.Surface):
        """绘制单位"""
        # 绘制部队
        unit_width = 60
        unit_height = 80

        # 部队背景
        pygame.draw.rect(screen, self.color,
                        (self.x - unit_width//2, self.y - unit_height//2,
                         unit_width, unit_height))
        pygame.draw.rect(screen, COLOR_WHITE,
                        (self.x - unit_width//2, self.y - unit_height//2,
                         unit_width, unit_height), 2)

        # 兵力条
        bar_width = 50
        bar_height = 8
        bar_x = self.x - bar_width // 2
        bar_y = self.y + 50

        # 背景条
        pygame.draw.rect(screen, (100, 0, 0),
                        (bar_x, bar_y, bar_width, bar_height))

        # 血量条
        health_ratio = self.soldiers / self.max_soldiers
        health_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, (0, 200, 0),
                        (bar_x, bar_y, health_width, bar_height))

        # 单位名称
        font = resource_loader.get_font(FONT_SIZE_SMALL)
        name_text = font.render(self.name, True, COLOR_WHITE)
        name_rect = name_text.get_rect(center=(self.x, self.y - 50))
        screen.blit(name_text, name_rect)

        # 兵力数
        soldier_text = font.render(f"{self.soldiers}", True, COLOR_WHITE)
        soldier_rect = soldier_text.get_rect(center=(self.x, self.y))
        screen.blit(soldier_text, soldier_rect)

    def take_damage(self, damage: int):
        """受到伤害"""
        actual_damage = max(10, damage - self.defense // 2)
        self.soldiers = max(0, self.soldiers - actual_damage)
        self.morale = max(0, self.morale - 10)

    def is_defeated(self) -> bool:
        """是否被击败"""
        return self.soldiers <= 0


class BattleScene(BaseScene):
    """战斗场景"""

    def __init__(self, screen: pygame.Surface, game, attacker=None, defender=None):
        super().__init__(screen)
        self.game = game
        self.attacker = attacker or Unit("我军", 300, 360, "player", 5000)
        self.defender = defender or Unit("敌军", 980, 360, "enemy", 5000)

        self.units: List[Unit] = [self.attacker, self.defender]

        self.battle_log: List[str] = []
        self.current_turn = "player"
        self.battle_over = False
        self.winner = None
        self._enemy_turn_timer = 0.0

        # 预生成战场装饰位置，避免每帧随机生成导致闪烁
        self._decorations = [
            (random.randint(0, SCREEN_WIDTH), random.randint(250, 550))
            for _ in range(10)
        ]

        # 初始日志
        self.battle_log.append("战斗开始！")
        self.battle_log.append(f"{self.attacker.name} vs {self.defender.name}")

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

                # 空格键继续
                if event.key == pygame.K_SPACE and not self.battle_over:
                    self._execute_turn()

    def _handle_click(self, pos: tuple):
        """处理点击"""
        # 攻击按钮
        attack_btn = pygame.Rect(100, 600, 120, 50)
        if attack_btn.collidepoint(pos) and self.current_turn == "player":
            self._execute_turn()

        # 撤退按钮
        retreat_btn = pygame.Rect(250, 600, 120, 50)
        if retreat_btn.collidepoint(pos) and self.current_turn == "player":
            self._retreat()

        # 结束战斗按钮（战斗结束后）
        if self.battle_over:
            end_btn = pygame.Rect(SCREEN_WIDTH//2 - 60, 500, 120, 50)
            if end_btn.collidepoint(pos):
                self.next_scene = "world"
                self.running = False

    def _execute_turn(self):
        """执行回合"""
        if self.battle_over:
            return

        if self.current_turn == "player":
            # 玩家攻击
            damage = random.randint(80, 150)
            critical = random.random() < 0.2

            if critical:
                damage *= 2
                self.battle_log.append(f"会心一击！{self.attacker.name}造成 {damage} 点伤害")
            else:
                self.battle_log.append(f"{self.attacker.name}攻击，造成 {damage} 点伤害")

            self.defender.take_damage(damage)
            self.attacker.is_attacking = True

            if self.defender.is_defeated():
                self._end_battle("player")
                return

            self.current_turn = "enemy"

        else:
            # 敌人攻击
            damage = random.randint(60, 120)
            self.battle_log.append(f"{self.defender.name}反击，造成 {damage} 点伤害")
            self.attacker.take_damage(damage)

            if self.attacker.is_defeated():
                self._end_battle("enemy")
                return

            self.current_turn = "player"

        # 保持日志数量
        if len(self.battle_log) > 6:
            self.battle_log = self.battle_log[-6:]

    def _retreat(self):
        """撤退"""
        self.battle_log.append("选择撤退...")
        if random.random() < 0.7:
            self.battle_log.append("撤退成功！")
            self.winner = "retreat"
            self.battle_over = True
        else:
            self.battle_log.append("撤退失败！被敌军追击！")
            self.attacker.take_damage(100)

    def _end_battle(self, winner: str):
        """结束战斗"""
        self.battle_over = True
        self.winner = winner

        if winner == "player":
            self.battle_log.append("战斗胜利！")
        else:
            self.battle_log.append("战斗失败...")

    def update(self, delta_time: float):
        """更新逻辑"""
        # 攻击动画
        if self.attacker.is_attacking:
            self.attacker.attack_frame += 1
            if self.attacker.attack_frame > 10:
                self.attacker.is_attacking = False
                self.attacker.attack_frame = 0

        # AI 回合延迟 - 使用计时器替代 delay 以避免阻塞事件处理
        if self.current_turn == "enemy" and not self.battle_over:
            self._enemy_turn_timer += delta_time
            if self._enemy_turn_timer >= 0.5:  # 500ms 延迟
                self._execute_turn()
                self._enemy_turn_timer = 0.0

    def draw(self):
        """绘制场景"""
        # 背景
        self.screen.fill((100, 80, 60))

        # 绘制战场
        self._draw_battlefield()

        # 绘制单位
        for unit in self.units:
            unit.draw(self.screen)

        # 绘制 UI
        self._draw_ui()

        pygame.display.flip()

    def _draw_battlefield(self):
        """绘制战场"""
        # 地面
        ground_rect = pygame.Rect(0, 250, SCREEN_WIDTH, 300)
        pygame.draw.rect(self.screen, (80, 100, 60), ground_rect)

        # 装饰 - 使用预生成的位置
        for x, y in self._decorations:
            pygame.draw.circle(self.screen, (60, 80, 40), (x, y), 5)

    def _draw_ui(self):
        """绘制 UI"""
        font = resource_loader.get_font(FONT_SIZE_NORMAL)
        small_font = resource_loader.get_font(FONT_SIZE_SMALL)

        # 顶部信息
        pygame.draw.rect(self.screen, (40, 40, 60), (0, 0, SCREEN_WIDTH, 60))

        turn_text = font.render(f"当前回合：{self.current_turn}", True, COLOR_WHITE)
        self.screen.blit(turn_text, (20, 18))

        # 战斗日志
        log_rect = pygame.Rect(20, 550, 600, 120)
        pygame.draw.rect(self.screen, (30, 30, 50), log_rect)
        pygame.draw.rect(self.screen, COLOR_GOLD, log_rect, 2)

        y = 560
        for log in self.battle_log:
            log_text = small_font.render(log, True, COLOR_WHITE)
            self.screen.blit(log_text, (30, y))
            y += 18

        # 行动按钮
        if not self.battle_over:
            # 攻击按钮
            attack_btn = pygame.Rect(100, 600, 120, 50)
            color = (200, 100, 100) if self.current_turn == "player" else (100, 100, 100)
            pygame.draw.rect(self.screen, color, attack_btn)
            attack_text = font.render("攻击", True, COLOR_WHITE)
            self.screen.blit(attack_text, (130, 615))

            # 撤退按钮
            retreat_btn = pygame.Rect(250, 600, 120, 50)
            pygame.draw.rect(self.screen, color, retreat_btn)
            retreat_text = font.render("撤退", True, COLOR_WHITE)
            self.screen.blit(retreat_text, (280, 615))

            # 提示
            if self.current_turn == "enemy":
                tip_text = font.render("敌军思考中...", True, COLOR_GOLD)
                self.screen.blit(tip_text, (400, 615))
        else:
            # 结束按钮
            end_btn = pygame.Rect(SCREEN_WIDTH//2 - 60, 500, 120, 50)
            pygame.draw.rect(self.screen, COLOR_GOLD, end_btn)
            result = "胜利" if self.winner == "player" else "失败"
            end_text = font.render(f"返回 ({result})", True, COLOR_BLACK)
            self.screen.blit(end_text, (SCREEN_WIDTH//2 - 50, 515))

            # 结果文字
            result_text = resource_loader.get_font(FONT_SIZE_LARGE).render(
                f"战斗{result}!", True, COLOR_GOLD if self.winner == "player" else COLOR_RED)
            result_rect = result_text.get_rect(center=(SCREEN_WIDTH//2, 450))
            self.screen.blit(result_text, result_rect)
