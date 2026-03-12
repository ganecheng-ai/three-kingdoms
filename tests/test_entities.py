"""
武将系统测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGeneral:
    """武将类测试"""

    def test_create_general(self):
        """测试创建武将"""
        from src.entities import General
        guan_yu = General("guan_yu")
        assert guan_yu.name == "关羽"
        assert guan_yu.faction == "shu"
        assert guan_yu.wu_li == 97

    def test_create_general_by_name(self):
        """测试通过中文名称创建武将"""
        from src.entities import General
        liu_bei = General.create_by_name("刘备")
        assert liu_bei is not None
        assert liu_bei.faction == "shu"

        invalid = General.create_by_name("无效武将")
        assert invalid is None

    def test_get_all_generals(self):
        """测试获取所有武将"""
        from src.entities import General
        all_generals = General.get_all_generals()
        assert len(all_generals) > 0

        shu_generals = General.get_all_generals("shu")
        assert len(shu_generals) > 0
        assert "guan_yu" in shu_generals

        wei_generals = General.get_all_generals("wei")
        assert len(wei_generals) > 0

    def test_general_stats(self):
        """测试武将属性"""
        from src.entities import General
        zhao_yun = General("zhao_yun")
        assert zhao_yun.get_attack_power() > 0
        assert zhao_yun.get_defense_power() > 0
        assert zhao_yun.get_strategy_power() > 0

    def test_take_damage(self):
        """测试受到伤害"""
        from src.entities import General
        zhang_fei = General("zhang_fei")
        initial_hp = zhang_fei.hp
        damage = zhang_fei.take_damage(100)
        assert damage > 0
        assert zhang_fei.hp < initial_hp

    def test_heal(self):
        """测试治疗"""
        from src.entities import General
        liu_bei = General("liu_bei")
        liu_bei.take_damage(50)
        healed = liu_bei.heal(30)
        assert healed > 0
        assert liu_bei.hp > 0

    def test_gain_exp_and_level_up(self):
        """测试获得经验和升级"""
        from src.entities import General
        cao_cao = General("cao_cao")
        initial_level = cao_cao.level
        cao_cao.gain_exp(200)
        assert cao_cao.level > initial_level

    def test_faction_colors(self):
        """测试势力颜色"""
        from src.entities import General
        assert "shu" in General.FACTION_COLORS
        assert "wei" in General.FACTION_COLORS
        assert "wu" in General.FACTION_COLORS

    def test_get_info_dict(self):
        """测试获取信息字典"""
        from src.entities import General
        zhou_yu = General("zhou_yu")
        info = zhou_yu.get_info_dict()
        assert "姓名" in info
        assert info["姓名"] == "周瑜"
        assert "势力" in info
        assert "等级" in info


class TestCity:
    """城市类测试"""

    def test_create_city(self):
        """测试创建城市"""
        from src.entities import City
        chengdu = City("成都", 100, 200, "shu")
        assert chengdu.name == "成都"
        assert chengdu.x == 100
        assert chengdu.y == 200
        assert chengdu.owner == "shu"

    def test_city_faction_color(self):
        """测试势力颜色"""
        from src.entities import City
        city = City("洛阳", 0, 0, "wei")
        assert city.color == (100, 100, 200)

        neutral_city = City("荆州", 0, 0, "neutral")
        assert neutral_city.color == (139, 90, 43)

    def test_city_faction_name(self):
        """测试势力名称"""
        from src.entities import City
        city = City("建业", 0, 0, "wu")
        assert city.faction_name == "吴"

    def test_recruit_soldiers(self):
        """测试招募士兵"""
        from src.entities import City
        city = City("成都", 0, 0, "shu")
        initial_gold = city.gold
        initial_soldiers = city.soldiers

        success, count, cost = city.recruit_soldiers("infantry", 5)
        assert success is True
        assert count == 5
        assert cost == 50
        assert city.gold == initial_gold - 50
        assert city.soldiers == initial_soldiers + 5

    def test_recruit_soldiers_not_enough_gold(self):
        """测试金钱不足时招募失败"""
        from src.entities import City
        city = City("成都", 0, 0, "shu")
        city.gold = 10

        success, count, cost = city.recruit_soldiers("cavalry", 5)
        assert success is False
        assert count == 0
        assert cost == 0

    def test_collect_tax(self):
        """测试征收税款"""
        from src.entities import City
        city = City("成都", 0, 0, "shu")
        initial_gold = city.gold

        tax = city.collect_tax()
        assert tax > 0
        assert city.gold > initial_gold

    def test_collect_food(self):
        """测试征收粮草"""
        from src.entities import City
        city = City("成都", 0, 0, "shu")
        initial_food = city.food

        food = city.collect_food()
        assert food > 0
        assert city.food > initial_food

    def test_upgrade_building(self):
        """测试升级建筑"""
        from src.entities import City
        city = City("成都", 0, 0, "shu")
        initial_gold = city.gold

        success, cost = city.upgrade_building("farm")
        assert success is True
        assert cost == 200
        assert city.buildings["farm"] == 2
        assert city.gold == initial_gold - 200

    def test_upgrade_building_max_level(self):
        """测试建筑已满级时升级失败"""
        from src.entities import City
        city = City("成都", 0, 0, "shu")
        city.buildings["farm"] = 5

        success, cost = city.upgrade_building("farm")
        assert success is False
        assert cost == 0

    def test_add_remove_general(self):
        """测试添加和移除武将"""
        from src.entities import City, General
        city = City("成都", 0, 0, "shu")
        guan_yu = General("guan_yu")

        # 添加武将
        assert city.add_general(guan_yu) is True
        assert guan_yu in city.generals
        assert len(city.generals) == 1

        # 重复添加失败
        assert city.add_general(guan_yu) is False

        # 移除武将
        assert city.remove_general(guan_yu) is True
        assert guan_yu not in city.generals

    def test_get_info_dict(self):
        """测试获取城市信息字典"""
        from src.entities import City
        city = City("洛阳", 0, 0, "wei")
        info = city.get_info_dict()
        assert info["城市"] == "洛阳"
        assert info["势力"] == "魏"
        assert "人口" in info
        assert "兵力" in info
        assert "金钱" in info
        assert "粮草" in info

    def test_end_turn(self):
        """测试结束回合处理"""
        from src.entities import City
        city = City("成都", 0, 0, "shu")
        initial_population = city.population
        initial_food = city.food

        city.end_turn()
        assert city.population >= initial_population
        assert city.food > initial_food


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
