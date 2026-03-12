"""
AI 逻辑 - 三国游戏 AI 系统
AI Logic - Three Kingdoms game AI system
"""

import random
from typing import List, Dict, Optional
from src.entities import City, General
from src.entities.army import Army


class AIGeneral:
    """AI 决策类 - 负责单个势力 AI 决策"""

    def __init__(self, faction: str, difficulty: str = "normal"):
        """初始化 AI

        Args:
            faction: 势力名称 (wei, shu, wu)
            difficulty: 难度等级 (easy, normal, hard)
        """
        self.faction = faction
        self.difficulty = difficulty

        # 难度参数
        self.difficulty_params = {
            "easy": {
                "aggression": 0.3,      # 攻击性 0-1
                "expansion": 0.2,       # 扩张欲 0-1
                "development": 0.5,     # 发展欲 0-1
                "random_factor": 0.3,   # 随机因素
            },
            "normal": {
                "aggression": 0.5,
                "expansion": 0.5,
                "development": 0.5,
                "random_factor": 0.2,
            },
            "hard": {
                "aggression": 0.7,
                "expansion": 0.7,
                "development": 0.6,
                "random_factor": 0.1,
            },
        }

        self.params = self.difficulty_params.get(difficulty, self.difficulty_params["normal"])

        # 战略状态
        self.strategy = "development"  # development, expansion, war
        self.target_city: Optional[City] = None
        self.target_enemy: Optional[str] = None

    def decide_strategy(self, cities: List[City], armies: List[Army], enemy_factions: List[str]) -> str:
        """决定战略

        Args:
            cities: 拥有的城市列表
            armies: 拥有的军队列表
            enemy_factions: 敌方势力列表

        Returns:
            战略类型
        """
        if not cities:
            self.strategy = "expansion"
            return self.strategy

        # 计算总实力
        total_soldiers = sum(army.total_soldiers for army in armies)
        total_gold = sum(city.gold for city in cities)
        total_food = sum(city.food for city in cities)

        # 根据实力决定战略
        if total_soldiers < 5000:
            # 兵力不足，优先发展
            self.strategy = "development"
        elif total_gold > 2000 and total_food > 2000:
            # 资源充足，可以扩张
            if random.random() < self.params["aggression"]:
                self.strategy = "war"
            else:
                self.strategy = "development"
        else:
            self.strategy = "development"

        # 随机因素（只在不影响核心战略的情况下生效）
        if total_soldiers >= 5000 and random.random() < self.params["random_factor"]:
            strategies = ["development", "expansion", "war"]
            self.strategy = random.choice(strategies)

        return self.strategy

    def select_target_city(self, cities: List[City], my_cities: List[City]) -> Optional[City]:
        """选择攻击目标城市

        Args:
            cities: 所有城市列表
            my_cities: 我方城市列表

        Returns:
            目标城市
        """
        # 获取可攻击的城市（非我方城市）
        my_city_names = {city.name for city in my_cities}
        enemy_cities = [city for city in cities if city.name not in my_city_names]

        if not enemy_cities:
            return None

        # 选择最弱的城市
        weakest = min(enemy_cities, key=lambda c: c.soldiers)
        return weakest

    def select_target_enemy(self, factions: List[str]) -> Optional[str]:
        """选择攻击目标势力

        Args:
            factions: 所有势力列表

        Returns:
            目标势力
        """
        my_faction = self.faction
        enemies = [f for f in factions if f != my_faction]

        if not enemies:
            return None

        return random.choice(enemies)

    def manage_city(self, city: City) -> Dict[str, str]:
        """管理城市决策

        Args:
            city: 城市对象

        Returns:
            决策字典 {action: target}
        """
        actions = {}

        # 如果金钱充足，优先升级建筑
        if city.gold >= 500 and self.strategy == "development":
            # 优先升级农田或市集
            if city.food < 1000:
                actions["upgrade"] = "farm"
            elif city.gold < 1500:
                actions["upgrade"] = "market"
            else:
                actions["upgrade"] = "barracks"

        # 招兵
        if city.gold >= 500 and city.soldiers < city.max_soldiers * 0.8:
            if self.strategy == "war":
                actions["recruit"] = "cavalry"
            else:
                actions["recruit"] = "infantry"

        # 如果兵力不足，优先征兵
        if city.soldiers < 500:
            actions["recruit"] = "infantry"

        return actions

    def manage_army(self, army: Army, enemy_armies: List[Army]) -> Dict[str, str]:
        """管理军队决策

        Args:
            army: 军队对象
            enemy_armies: 敌方军队列表

        Returns:
            决策字典 {action: target}
        """
        actions = {}

        if army.is_defeated():
            actions["action"] = "retreat"
            return actions

        # 如果士气低落，休息
        if army.morale < 50:
            actions["action"] = "rest"
            return actions

        # 如果体力不足，休息
        if army.stamina < 50:
            actions["action"] = "rest"
            return actions

        # 发现敌方军队
        if enemy_armies:
            # 比较实力
            enemy_strength = sum(e.total_soldiers for e in enemy_armies)
            my_strength = army.total_soldiers

            if my_strength > enemy_strength * 1.5:
                # 实力占优，进攻
                actions["action"] = "attack"
                # 选择最弱的敌人
                weakest = min(enemy_armies, key=lambda a: a.total_soldiers)
                actions["target"] = weakest
            elif my_strength < enemy_strength * 0.5:
                # 实力劣势，撤退
                actions["action"] = "retreat"
            else:
                # 实力相当，防守
                actions["action"] = "defend"
        else:
            # 没有敌人，探索或移动
            actions["action"] = "move"

        return actions


class AIManager:
    """AI 管理器 - 管理所有 AI 势力"""

    def __init__(self):
        self.ai_generals: Dict[str, AIGeneral] = {}
        self.factions: List[str] = ["wei", "shu", "wu"]

    def register_faction(self, faction: str, difficulty: str = "normal"):
        """注册势力 AI

        Args:
            faction: 势力名称
            difficulty: 难度等级
        """
        if faction not in self.ai_generals:
            self.ai_generals[faction] = AIGeneral(faction, difficulty)

    def get_ai(self, faction: str) -> Optional[AIGeneral]:
        """获取势力 AI

        Args:
            faction: 势力名称

        Returns:
            AI 实例
        """
        return self.ai_generals.get(faction)

    def process_turn(self, faction: str, cities: Dict[str, City], armies: List[Army]) -> Dict[str, Dict]:
        """处理 AI 回合

        Args:
            faction: 势力名称
            cities: 所有城市
            armies: 所有军队

        Returns:
            决策字典
        """
        ai = self.ai_generals.get(faction)
        if not ai:
            return {}

        # 获取我方城市和军队
        my_cities = [c for c in cities.values() if c.owner == faction]
        my_armies = [a for a in armies if a.owner == faction]

        # 获取敌方势力
        enemy_factions = [f for f in self.factions if f != faction]

        # 决定战略
        strategy = ai.decide_strategy(my_cities, my_armies, enemy_factions)

        decisions = {
            "strategy": strategy,
            "cities": {},
            "armies": [],
        }

        # 城市决策
        for city in my_cities:
            city_decisions = ai.manage_city(city)
            if city_decisions:
                decisions["cities"][city.name] = city_decisions

        # 军队决策
        for army in my_armies:
            army_decisions = ai.manage_army(army, [])
            if army_decisions:
                decisions["armies"].append({
                    "army": army,
                    "decisions": army_decisions,
                })

        return decisions


class BattleAI:
    """战斗 AI - 负责战斗中的决策"""

    def __init__(self, army: Army, difficulty: str = "normal"):
        """初始化战斗 AI

        Args:
            army: 军队对象
            difficulty: 难度等级
        """
        self.army = army
        self.difficulty = difficulty

        # 难度参数
        self.params = {
            "easy": {"attack_chance": 0.4, "retreat_chance": 0.6},
            "normal": {"attack_chance": 0.6, "retreat_chance": 0.4},
            "hard": {"attack_chance": 0.8, "retreat_chance": 0.2},
        }.get(difficulty, {"attack_chance": 0.6, "retreat_chance": 0.4})

    def decide_action(self, enemy_army: Army) -> str:
        """决定战斗行动

        Args:
            enemy_army: 敌方军队

        Returns:
            行动类型 (attack, defend, retreat, special)
        """
        # 士气低落时优先撤退
        if self.army.morale < 30:
            return "retreat"

        # 计算实力对比
        my_power = self.army.attack_power + self.army.defense_power
        enemy_power = enemy_army.attack_power + enemy_army.defense_power

        power_ratio = my_power / max(1, enemy_power)

        # 实力占优时优先攻击
        if power_ratio > 1.5:
            if random.random() < self.params["attack_chance"]:
                return "attack"

        # 实力劣势时考虑撤退
        if power_ratio < 0.5:
            if random.random() < self.params["retreat_chance"]:
                return "retreat"
            return "defend"

        # 默认攻击
        return "attack"

    def select_target_unit(self, enemy_units: List) -> Optional:
        """选择攻击目标

        Args:
            enemy_units: 敌方单位列表

        Returns:
            目标单位
        """
        if not enemy_units:
            return None

        # 优先攻击最弱的单位
        return min(enemy_units, key=lambda u: u.soldiers if hasattr(u, 'soldiers') else u.hp)

    def use_strategy(self, enemy_army: Army) -> Optional[str]:
        """使用策略

        Args:
            enemy_army: 敌方军队

        Returns:
            策略名称
        """
        strategies = []

        # 根据情况选择策略
        if self.army.morale > 80:
            strategies.append("morale_boost")

        if self.army.stamina > 80:
            strategies.append("rush_attack")

        if self.army.total_soldiers > enemy_army.total_soldiers:
            strategies.append("encircle")

        if strategies:
            return random.choice(strategies)

        return None


class DiplomacyAI:
    """外交 AI - 负责外交决策"""

    def __init__(self, faction: str):
        """初始化外交 AI

        Args:
            faction: 势力名称
        """
        self.faction = faction
        self.relationships: Dict[str, int] = {}  # 与其他势力的关系值 -100 到 100

    def improve_relationship(self, target_faction: str, amount: int):
        """改善关系

        Args:
            target_faction: 目标势力
            amount: 改善值
        """
        current = self.relationships.get(target_faction, 0)
        self.relationships[target_faction] = min(100, current + amount)

    def worsen_relationship(self, target_faction: str, amount: int):
        """恶化关系

        Args:
            target_faction: 目标势力
            amount: 恶化值
        """
        current = self.relationships.get(target_faction, 0)
        self.relationships[target_faction] = max(-100, current - amount)

    def decide_alliance(self, target_faction: str) -> bool:
        """决定是否结盟

        Args:
            target_faction: 目标势力

        Returns:
            是否同意结盟
        """
        relationship = self.relationships.get(target_faction, 0)
        # 关系值大于 50 时同意结盟
        return relationship > 50

    def decide_war(self, target_faction: str) -> bool:
        """决定是否宣战

        Args:
            target_faction: 目标势力

        Returns:
            是否宣战
        """
        relationship = self.relationships.get(target_faction, 0)
        # 关系值小于 -50 时宣战
        return relationship < -50


# 全局 AI 管理器实例
ai_manager = AIManager()
