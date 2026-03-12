"""
资源加载器 - 管理游戏资源
Resource Loader - Manage game resources
"""

import os
import pygame
from typing import Dict, Optional


class ResourceLoader:
    """游戏资源加载器"""

    _instance: Optional['ResourceLoader'] = None

    def __new__(cls) -> 'ResourceLoader':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # 资源目录
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(self.base_dir, 'resources')

        # 资源缓存
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music: Optional[str] = None
        self.fonts: Dict[str, pygame.font.Font] = {}

        # 默认字体
        self.default_font: Optional[pygame.font.Font] = None

        # 音量设置
        self.sound_volume = 0.7
        self.music_volume = 0.5

    def set_sound_volume(self, volume: float):
        """设置音效音量 (0.0-1.0)"""
        self.sound_volume = max(0.0, min(1.0, volume))
        pygame.mixer.set_volume(self.sound_volume)

    def set_music_volume(self, volume: float):
        """设置背景音乐音量 (0.0-1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def play_sound(self, name: str):
        """播放音效"""
        sound = self.load_sound(name)
        if sound:
            sound.set_volume(self.sound_volume)
            sound.play()

    def play_music(self, name: str, loops: int = -1):
        """播放背景音乐"""
        if self.load_music(name):
            self.set_music_volume(self.music_volume)
            pygame.mixer.music.play(loops=loops)

    def stop_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()

    def pause_music(self):
        """暂停背景音乐"""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """继续播放背景音乐"""
        pygame.mixer.music.unpause()

    def init_fonts(self):
        """初始化字体"""
        # 尝试加载中文字体
        font_names = [
            'SimHei',  # 黑体
            'Microsoft YaHei',  # 微软雅黑
            'WenQuanYi Micro Hei',  # 文泉驿微米黑
            'Noto Sans CJK SC',  # 思源黑体
            'AR PL UMing CN',  # 文泉驿正黑
            'DejaVu Sans',  # 备用字体
        ]

        loaded = False
        for font_name in font_names:
            try:
                self.default_font = pygame.font.SysFont(font_name, 24)
                loaded = True
                break
            except:
                continue

        if not loaded:
            # 使用默认字体
            self.default_font = pygame.font.Font(None, 24)

    def get_font(self, size: int = 24) -> pygame.font.Font:
        """获取字体"""
        if size == 24 and self.default_font:
            return self.default_font

        cache_key = f"font_{size}"
        if cache_key not in self.fonts:
            try:
                self.fonts[cache_key] = pygame.font.Font(None, size)
            except:
                self.fonts[cache_key] = self.default_font or pygame.font.Font(None, size)

        return self.fonts[cache_key]

    def load_image(self, name: str) -> pygame.Surface:
        """加载图片"""
        if name in self.images:
            return self.images[name]

        image_path = os.path.join(self.resources_dir, 'images', name)

        if os.path.exists(image_path):
            try:
                image = pygame.image.load(image_path).convert_alpha()
                self.images[name] = image
                return image
            except Exception as e:
                print(f"加载图片失败 {name}: {e}")

        # 返回占位图片
        placeholder = pygame.Surface((100, 100), pygame.SRCALPHA)
        placeholder.fill((128, 128, 128, 128))
        self.images[name] = placeholder
        return placeholder

    def load_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """加载音效"""
        if name in self.sounds:
            return self.sounds[name]

        sound_path = os.path.join(self.resources_dir, 'sounds', name)

        if os.path.exists(sound_path):
            try:
                sound = pygame.mixer.Sound(sound_path)
                self.sounds[name] = sound
                return sound
            except Exception as e:
                print(f"加载音效失败 {name}: {e}")

        return None

    def load_music(self, name: str) -> bool:
        """加载背景音乐"""
        music_path = os.path.join(self.resources_dir, 'sounds', name)

        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                self.music = name
                return True
            except Exception as e:
                print(f"加载音乐失败 {name}: {e}")

        return False

    def preload_resources(self):
        """预加载资源"""
        print("预加载资源...")
        self.init_fonts()

        # 预加载音效
        sound_types = ["click", "battle", "victory", "defeat", "march", "build"]
        for sound_type in sound_types:
            self.load_sound(f"{sound_type}.wav")
        print("  音效加载完成")

        # 预加载背景音乐
        self.load_music("bgm_main.wav")
        print("  背景音乐加载完成")

        print("资源加载完成")


# 全局资源加载器实例
resource_loader = ResourceLoader()
