"""
三国霸业 - 主入口
Three Kingdoms - Main Entry Point
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game


def main():
    """游戏主函数"""
    print("=" * 50)
    print("       三国霸业 Three Kingdoms")
    print("       Version 0.3.0")
    print("=" * 50)
    print()
    print("正在启动游戏...")

    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n游戏已退出")
    except Exception as e:
        print(f"\n游戏发生错误：{e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
