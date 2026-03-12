"""
AI 系统测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAIGeneral:
    """AI 决策类测试"""

    def test_create_ai(self):
        """测试创建 AI"""
        from src.ai import AIGeneral
        ai = AIGeneral(faction="wei")
        assert ai.faction == "wei"
        assert ai.difficulty == "normal"

    def test_create_ai_with_difficulty(self):
        """测试创建不同难度的 AI"""
        from src.ai import AIGeneral
        ai_easy = AIGeneral(faction="shu", difficulty="easy")
        ai_hard = AIGeneral(faction="wu", difficulty="hard")
        assert ai_easy.params["aggression"] == 0.3
        assert ai_hard.params["aggression"] == 0.7

    def test_decide_strategy_no_cities(self):
        """测试没有城市时的战略决策"""
        from src.ai import AIGeneral
        ai = AIGeneral(faction="wei")
        strategy = ai.decide_strategy([], [], ["shu", "wu"])
        assert strategy == "expansion"

    def test_decide_strategy_low_soldiers(self):
        """测试兵力不足时的战略决策"""
        from src.ai import AIGeneral, Army
        ai = AIGeneral(faction="wei")
        city = type('MockCity', (), {'gold': 1000, 'food': 1000})()
        army = Army(owner="wei")
        strategy = ai.decide_strategy([city], [army], ["shu"])
        assert strategy == "development"

    def test_select_target_city(self):
        """测试选择目标城市"""
        from src.ai import AIGeneral
        from src.entities import City

        ai = AIGeneral(faction="wei")
        my_city = City("洛阳", 100, 100, "wei")
        enemy_city1 = City("荆州", 200, 200, "shu")
        enemy_city2 = City("襄阳", 300, 300, "shu")

        enemy_city1.soldiers = 1000
        enemy_city2.soldiers = 500

        target = ai.select_target_city(
            [my_city, enemy_city1, enemy_city2],
            [my_city]
        )
        assert target == enemy_city2  # 选择兵力最弱的

    def test_select_target_enemy(self):
        """测试选择目标势力"""
        from src.ai import AIGeneral
        ai = AIGeneral(faction="wei")
        target = ai.select_target_enemy(["wei", "shu", "wu"])
        assert target in ["shu", "wu"]

    def test_manage_city_development(self):
        """测试城市管理 - 发展"""
        from src.ai import AIGeneral
        from src.entities import City

        ai = AIGeneral(faction="wei", difficulty="normal")
        ai.strategy = "development"
        city = City("洛阳", 100, 100, "wei")
        city.gold = 600
        city.food = 500

        actions = ai.manage_city(city)
        # 食物不足时优先升级农田
        if "upgrade" in actions:
            assert actions["upgrade"] == "farm"

    def test_manage_city_war(self):
        """测试城市管理 - 战争"""
        from src.ai import AIGeneral
        from src.entities import City

        ai = AIGeneral(faction="wei", difficulty="normal")
        ai.strategy = "war"
        city = City("洛阳", 100, 100, "wei")
        city.gold = 1000
        city.soldiers = 1000
        city.max_soldiers = 5000

        actions = ai.manage_city(city)
        # 战争状态下优先招募骑兵
        if "recruit" in actions:
            assert actions["recruit"] == "cavalry"

    def test_manage_army_rest(self):
        """测试军队管理 - 休息"""
        from src.ai import AIGeneral, Army

        ai = AIGeneral(faction="wei")
        army = Army(owner="wei")
        army.add_soldiers("infantry", 1000)
        army.morale = 30
        army.stamina = 30

        actions = ai.manage_army(army, [])
        assert actions.get("action") == "rest"

    def test_manage_army_attack(self):
        """测试军队管理 - 攻击"""
        from src.ai import AIGeneral, Army

        ai = AIGeneral(faction="wei")
        army = Army(owner="wei")
        army.add_soldiers("infantry", 2000)
        army.morale = 100
        army.stamina = 100

        enemy_army = Army(owner="shu")
        enemy_army.add_soldiers("infantry", 500)

        actions = ai.manage_army(army, [enemy_army])
        # 实力占优应该进攻
        assert actions.get("action") == "attack"


class TestAIManager:
    """AI 管理器测试"""

    def test_register_faction(self):
        """测试注册势力"""
        from src.ai import AIManager
        manager = AIManager()
        manager.register_faction("wei", "hard")
        assert "wei" in manager.ai_generals
        assert manager.ai_generals["wei"].difficulty == "hard"

    def test_get_ai(self):
        """测试获取 AI"""
        from src.ai import AIManager
        manager = AIManager()
        manager.register_faction("shu")
        ai = manager.get_ai("shu")
        assert ai is not None
        assert ai.faction == "shu"

    def test_process_turn(self):
        """测试处理回合"""
        from src.ai import AIManager
        from src.entities import City, Army

        manager = AIManager()
        manager.register_faction("wei")

        city = City("洛阳", 100, 100, "wei")
        city.gold = 1000
        city.food = 1000

        army = Army(owner="wei")
        army.add_soldiers("infantry", 1000)

        decisions = manager.process_turn("wei", {"洛阳": city}, [army])
        assert "strategy" in decisions
        assert "cities" in decisions
        assert "armies" in decisions


class TestBattleAI:
    """战斗 AI 测试"""

    def test_create_battle_ai(self):
        """测试创建战斗 AI"""
        from src.ai import BattleAI
        from src.entities import Army

        army = Army(owner="wei")
        battle_ai = BattleAI(army)
        assert battle_ai.army == army
        assert battle_ai.difficulty == "normal"

    def test_decide_action_attack(self):
        """测试战斗决策 - 攻击"""
        from src.ai import BattleAI
        from src.entities import Army

        my_army = Army(owner="wei")
        my_army.add_soldiers("infantry", 2000)
        my_army.morale = 100
        my_army.stamina = 100

        enemy_army = Army(owner="shu")
        enemy_army.add_soldiers("infantry", 500)

        battle_ai = BattleAI(my_army, difficulty="hard")
        action = battle_ai.decide_action(enemy_army)
        # 实力占优时应该攻击
        assert action == "attack"

    def test_decide_action_retreat(self):
        """测试战斗决策 - 撤退"""
        from src.ai import BattleAI
        from src.entities import Army

        my_army = Army(owner="wei")
        my_army.add_soldiers("infantry", 100)
        my_army.morale = 20  # 低士气

        enemy_army = Army(owner="shu")
        enemy_army.add_soldiers("infantry", 2000)

        battle_ai = BattleAI(my_army)
        action = battle_ai.decide_action(enemy_army)
        # 士气低落时应该撤退
        assert action == "retreat"

    def test_select_target_unit(self):
        """测试选择攻击目标"""
        from src.ai import BattleAI
        from src.entities import Army

        battle_ai = BattleAI(Army(owner="wei"))

        unit1 = type('MockUnit', (), {'soldiers': 500, 'hp': 100})()
        unit2 = type('MockUnit', (), {'soldiers': 200, 'hp': 50})()
        unit3 = type('MockUnit', (), {'soldiers': 800, 'hp': 150})()

        target = battle_ai.select_target_unit([unit1, unit2, unit3])
        assert target == unit2  # 选择最弱的


class TestDiplomacyAI:
    """外交 AI 测试"""

    def test_create_diplomacy_ai(self):
        """测试创建外交 AI"""
        from src.ai import DiplomacyAI
        dip_ai = DiplomacyAI("wei")
        assert dip_ai.faction == "wei"

    def test_improve_relationship(self):
        """测试改善关系"""
        from src.ai import DiplomacyAI
        dip_ai = DiplomacyAI("wei")
        dip_ai.improve_relationship("shu", 30)
        assert dip_ai.relationships.get("shu") == 30

    def test_worsen_relationship(self):
        """测试恶化关系"""
        from src.ai import DiplomacyAI
        dip_ai = DiplomacyAI("wei")
        dip_ai.worsen_relationship("shu", 30)
        assert dip_ai.relationships.get("shu") == -30

    def test_decide_alliance(self):
        """测试决定结盟"""
        from src.ai import DiplomacyAI
        dip_ai = DiplomacyAI("wei")
        dip_ai.improve_relationship("shu", 60)
        assert dip_ai.decide_alliance("shu") is True

        dip_ai.improve_relationship("wu", 40)
        assert dip_ai.decide_alliance("wu") is False

    def test_decide_war(self):
        """测试决定宣战"""
        from src.ai import DiplomacyAI
        dip_ai = DiplomacyAI("wei")
        dip_ai.worsen_relationship("shu", 60)
        assert dip_ai.decide_war("shu") is True

        dip_ai.worsen_relationship("wu", 40)
        assert dip_ai.decide_war("wu") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
