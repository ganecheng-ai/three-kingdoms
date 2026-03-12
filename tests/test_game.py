"""
游戏基础测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfig:
    """配置测试"""

    def test_screen_size(self):
        """测试屏幕尺寸配置"""
        from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
        assert SCREEN_WIDTH > 0
        assert SCREEN_HEIGHT > 0
        assert SCREEN_WIDTH >= 800
        assert SCREEN_HEIGHT >= 600

    def test_fps(self):
        """测试帧率配置"""
        from src.config import FPS
        assert FPS > 0
        assert FPS <= 144

    def test_colors(self):
        """测试颜色定义"""
        from src.config import COLOR_WHITE, COLOR_BLACK, COLOR_RED
        assert len(COLOR_WHITE) == 3
        assert len(COLOR_BLACK) == 3
        assert len(COLOR_RED) == 3


class TestResourceLoader:
    """资源加载器测试"""

    def test_singleton(self):
        """测试单例模式"""
        from src.resource_loader import ResourceLoader
        loader1 = ResourceLoader()
        loader2 = ResourceLoader()
        assert loader1 is loader2


class TestGame:
    """游戏核心测试"""

    def test_game_import(self):
        """测试游戏类导入"""
        from src.game import Game
        assert Game is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
