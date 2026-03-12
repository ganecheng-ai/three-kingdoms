"""
日志系统 - 游戏调试日志
Logger - Game debugging logs
"""

import os
import logging
from datetime import datetime


def get_log_file_path():
    """获取日志文件路径"""
    # 在用户目录下创建日志文件
    if os.name == 'nt':  # Windows
        log_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'ThreeKingdoms')
    else:  # Linux/macOS
        log_dir = os.path.join(os.path.expanduser('~'), '.three_kingdoms')

    # 确保目录存在
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'game.log')
    return log_file


def setup_logger():
    """设置日志记录器"""
    log_file = get_log_file_path()

    # 创建日志记录器
    logger = logging.getLogger('ThreeKingdoms')
    logger.setLevel(logging.DEBUG)

    # 清除已有的处理器
    logger.handlers.clear()

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# 全局日志记录器
logger = setup_logger()


def log_info(message):
    """记录信息日志"""
    logger.info(message)


def log_debug(message):
    """记录调试日志"""
    logger.debug(message)


def log_error(message):
    """记录错误日志"""
    logger.error(message)


def log_warning(message):
    """记录警告日志"""
    logger.warning(message)


def get_log_path():
    """获取日志文件路径"""
    return get_log_file_path()