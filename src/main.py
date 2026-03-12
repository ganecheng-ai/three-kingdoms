"""
三国霸业 - 主入口
Three Kingdoms - Main Entry Point
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game
from src.logger import log_info, log_error, get_log_path


def main():
    """游戏主函数"""
    print("=" * 50)
    print("       三国霸业 Three Kingdoms")
    print("       Version 0.6.2")
    print("=" * 50)
    print()
    print(f"日志文件位置: {get_log_path()}")
    print("正在启动游戏...")

    log_info("=" * 50)
    log_info("三国霸业 v0.6.2 启动")
    log_info("=" * 50)

    try:
        log_info("初始化游戏...")
        game = Game()
        log_info("游戏初始化完成，开始运行主循环")
        game.run()
        log_info("游戏正常退出")
    except KeyboardInterrupt:
        log_info("用户中断游戏")
        print("\n游戏已退出")
    except Exception as e:
        log_error(f"游戏发生错误：{e}")
        print(f"\n游戏发生错误：{e}")
        import traceback
        traceback.print_exc()
        log_error(traceback.format_exc())
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
