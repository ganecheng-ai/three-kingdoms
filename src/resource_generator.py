"""
资源生成器 - 程序化生成游戏资源
Resource Generator - Programmatically generate game resources
"""

import pygame
import os
import wave
import struct
import math
import random
import io
from typing import Tuple


class ResourceGenerator:
    """资源生成器"""

    def __init__(self, resources_dir: str):
        """初始化资源生成器

        Args:
            resources_dir: 资源目录路径
        """
        self.resources_dir = resources_dir
        self.images_dir = os.path.join(resources_dir, 'images')
        self.sounds_dir = os.path.join(resources_dir, 'sounds')
        self.fonts_dir = os.path.join(resources_dir, 'fonts')

        # 确保目录存在
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.sounds_dir, exist_ok=True)
        os.makedirs(self.fonts_dir, exist_ok=True)

    def generate_city_image(self, faction: str, size: int = 60) -> pygame.Surface:
        """生成城市图标

        Args:
            faction: 势力 (wei, shu, wu, neutral)
            size: 图标大小

        Returns:
            pygame.Surface 城市图标
        """
        colors = {
            "wei": (50, 50, 200),    # 蓝色
            "shu": (50, 200, 50),    # 绿色
            "wu": (200, 50, 50),     # 红色
            "neutral": (139, 90, 43),  # 棕色
        }
        color = colors.get(faction, colors["neutral"])

        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2

        # 绘制城市底座
        pygame.draw.rect(surface, color, (10, 30, size - 20, size - 30))
        pygame.draw.rect(surface, (255, 255, 255), (10, 30, size - 20, size - 30), 2)

        # 绘制城墙
        pygame.draw.polygon(surface, color, [
            (5, 30), (size - 5, 30), (size // 2, 10)
        ])
        pygame.draw.polygon(surface, (255, 255, 255), [
            (5, 30), (size - 5, 30), (size // 2, 10)
        ], 2)

        # 绘制城楼
        pygame.draw.rect(surface, (180, 140, 80), (center - 10, 15, 20, 15))
        pygame.draw.rect(surface, (255, 255, 255), (center - 10, 15, 20, 15), 1)

        # 绘制旗帜
        pygame.draw.line(surface, (255, 255, 255), (center, 15), (center, 5), 2)
        pygame.draw.polygon(surface, color, [(center, 5), (center + 12, 8), (center, 11)])

        return surface

    def generate_generalPortrait(self, general_name: str, faction: str, size: int = 80) -> pygame.Surface:
        """生成武将头像

        Args:
            general_name: 武将名称
            faction: 势力
            size: 头像大小

        Returns:
            pygame.Surface 武将头像
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # 背景
        pygame.draw.rect(surface, (40, 40, 60), (0, 0, size, size))

        # 边框颜色
        faction_colors = {
            "shu": (50, 200, 50),
            "wei": (50, 50, 200),
            "wu": (200, 50, 50),
            "neutral": (150, 150, 50),
        }
        border_color = faction_colors.get(faction, (255, 255, 255))

        # 绘制边框
        pygame.draw.rect(surface, border_color, (0, 0, size, size), 3)

        # 绘制简单的人物轮廓
        center_x = size // 2
        head_y = size // 3

        # 头部
        pygame.draw.circle(surface, (220, 180, 150), (center_x, head_y), 15)

        # 身体
        pygame.draw.polygon(surface, border_color, [
            (center_x - 25, size - 10),
            (center_x + 25, size - 10),
            (center_x, head_y + 20)
        ])

        # 装饰 - 星星表示稀有度
        star_y = 8
        for i in range(3):
            star_x = 15 + i * 25
            self._draw_star(surface, (star_x, star_y), 8, (255, 215, 0))

        return surface

    def _draw_star(self, surface: pygame.Surface, center: Tuple[int, int],
                   size: int, color: Tuple[int, int, int]):
        """绘制五角星"""
        cx, cy = center
        points = []
        for i in range(5):
            angle = math.radians(90 + i * 72)
            points.append((
                cx + int(size * math.cos(angle)),
                cy - int(size * math.sin(angle))
            ))
            inner_angle = math.radians(90 + (i * 72 + 36))
            points.append((
                cx + int(size * 0.4 * math.cos(inner_angle)),
                cy - int(size * 0.4 * math.sin(inner_angle))
            ))
        pygame.draw.polygon(surface, color, points)

    def generate_soldier_icon(self, soldier_type: str, size: int = 40) -> pygame.Surface:
        """生成士兵图标

        Args:
            soldier_type: 兵种类型 (infantry, cavalry, archer, siege)
            size: 图标大小

        Returns:
            pygame.Surface 士兵图标
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        colors = {
            "infantry": (100, 100, 100),
            "cavalry": (150, 100, 50),
            "archer": (100, 150, 50),
            "siege": (150, 50, 50),
        }
        color = colors.get(soldier_type, (128, 128, 128))

        center = size // 2

        if soldier_type == "infantry":
            # 步兵 - 盾牌形状
            pygame.draw.polygon(surface, color, [
                (center, 5), (size - 8, 15), (size - 8, size - 10),
                (center, size - 5), (8, size - 10), (8, 15)
            ])
            pygame.draw.rect(surface, (255, 255, 255),
                           (center - 2, 5, 4, size - 10))

        elif soldier_type == "cavalry":
            # 骑兵 - 马形状简化
            pygame.draw.rect(surface, color, (10, 15, 20, 15))
            pygame.draw.circle(surface, color, (25, 12), 8)
            pygame.draw.polygon(surface, color, [(25, 30), (35, 35), (25, 38)])

        elif soldier_type == "archer":
            # 弓兵 - 弓箭形状
            pygame.draw.arc(surface, color, (5, 5, 30, 30), -1.5, 1.5, 3)
            pygame.draw.line(surface, (255, 255, 255), (8, 20), (32, 20), 2)

        elif soldier_type == "siege":
            # 战车 - 车轮形状
            pygame.draw.rect(surface, color, (5, 15, 30, 15))
            pygame.draw.circle(surface, (80, 80, 80), (12, 32), 6, 3)
            pygame.draw.circle(surface, (80, 80, 80), (28, 32), 6, 3)

        return surface

    def generate_terrain_tile(self, terrain_type: str, size: int = 64) -> pygame.Surface:
        """生成地形瓦片

        Args:
            terrain_type: 地形类型 (plain, mountain, water, forest, city)
            size: 瓦片大小

        Returns:
            pygame.Surface 地形瓦片
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        if terrain_type == "plain":
            # 平原 - 绿色背景
            surface.fill((34, 139, 34))
            # 添加一些草的细节
            for _ in range(10):
                x = random.randint(5, size - 5)
                y = random.randint(5, size - 5)
                pygame.draw.circle(surface, (50, 180, 50), (x, y), 2)

        elif terrain_type == "mountain":
            # 山脉 - 棕色背景
            surface.fill((100, 80, 60))
            # 绘制山峰
            pygame.draw.polygon(surface, (139, 119, 101), [
                (size // 2, 10), (5, size - 5), (size - 5, size - 5)
            ])
            # 雪顶
            pygame.draw.polygon(surface, (255, 255, 255), [
                (size // 2, 10), (size // 2 - 10, 25), (size // 2 + 10, 25)
            ])

        elif terrain_type == "water":
            # 水域 - 蓝色背景
            surface.fill((65, 105, 225))
            # 波浪
            for y in range(10, size, 15):
                pygame.draw.arc(surface, (100, 150, 255),
                              (5, y, 20, 10), 0, 3.14, 2)
                pygame.draw.arc(surface, (100, 150, 255),
                              (25, y, 20, 10), 0, 3.14, 2)

        elif terrain_type == "forest":
            # 森林 - 深绿色背景
            surface.fill((0, 100, 0))
            # 树木
            for _ in range(8):
                x = random.randint(10, size - 10)
                y = random.randint(10, size - 10)
                pygame.draw.polygon(surface, (0, 139, 0), [
                    (x, y - 10), (x - 8, y + 5), (x + 8, y + 5)
                ])
                pygame.draw.polygon(surface, (0, 139, 0), [
                    (x, y - 5), (x - 6, y + 10), (x + 6, y + 10)
                ])

        elif terrain_type == "city":
            # 城市 - 灰色背景
            surface.fill((80, 80, 80))
            # 城市轮廓
            pygame.draw.rect(surface, (120, 120, 120), (10, 20, size - 20, size - 25))
            pygame.draw.polygon(surface, (100, 100, 100), [
                (15, 20), (size - 15, 20), (size // 2, 8)
            ])

        return surface

    def generate_ui_button(self, width: int, height: int,
                          color: Tuple[int, int, int],
                          hover: bool = False) -> pygame.Surface:
        """生成 UI 按钮

        Args:
            width: 按钮宽度
            height: 按钮高度
            color: 按钮颜色
            hover: 是否悬停状态

        Returns:
            pygame.Surface 按钮
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # 按钮背景
        btn_color = tuple(min(255, c + 40) for c in color) if hover else color
        pygame.draw.rect(surface, btn_color, (0, 0, width, height), border_radius=5)

        # 边框
        border_color = tuple(max(0, c - 30) for c in color)
        pygame.draw.rect(surface, border_color, (0, 0, width, height), 2, border_radius=5)

        # 高光
        if hover:
            pygame.draw.line(surface, (255, 255, 255), (5, 5), (width - 5, 5), 2)

        return surface

    def generate_flag(self, faction: str, width: int = 40,
                     height: int = 60) -> pygame.Surface:
        """生成势力旗帜

        Args:
            faction: 势力 (wei, shu, wu)
            width: 旗帜宽度
            height: 旗帜高度

        Returns:
            pygame.Surface 旗帜
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        colors = {
            "wei": (50, 50, 200),
            "shu": (50, 200, 50),
            "wu": (200, 50, 50),
        }
        flag_color = colors.get(faction, (128, 128, 128))

        # 旗杆
        pygame.draw.rect(surface, (139, 90, 43), (2, 0, 4, height))

        # 旗帜
        pygame.draw.polygon(surface, flag_color, [
            (6, 5), (width - 5, height // 3), (6, height // 2),
            (6, height // 2), (width - 8, height * 2 // 3), (6, height - 5)
        ])

        # 边框
        pygame.draw.polygon(surface, (255, 215, 0), [
            (6, 5), (width - 5, height // 3), (6, height // 2),
            (6, height // 2), (width - 8, height * 2 // 3), (6, height - 5)
        ], 2)

        return surface

    def generate_all_resources(self):
        """生成所有资源"""
        print("正在生成游戏资源...")

        # 生成城市图标
        for faction in ["wei", "shu", "wu", "neutral"]:
            city_img = self.generate_city_image(faction)
            save_path = os.path.join(self.images_dir, f"city_{faction}.png")
            pygame.image.save(city_img, save_path)
            print(f"  已生成：{save_path}")

        # 生成地形瓦片
        for terrain in ["plain", "mountain", "water", "forest", "city"]:
            terrain_img = self.generate_terrain_tile(terrain)
            save_path = os.path.join(self.images_dir, f"terrain_{terrain}.png")
            pygame.image.save(terrain_img, save_path)
            print(f"  已生成：{save_path}")

        # 生成士兵图标
        for soldier_type in ["infantry", "cavalry", "archer", "siege"]:
            soldier_img = self.generate_soldier_icon(soldier_type)
            save_path = os.path.join(self.images_dir, f"soldier_{soldier_type}.png")
            pygame.image.save(soldier_img, save_path)
            print(f"  已生成：{save_path}")

        # 生成旗帜
        for faction in ["wei", "shu", "wu"]:
            flag_img = self.generate_flag(faction)
            save_path = os.path.join(self.images_dir, f"flag_{faction}.png")
            pygame.image.save(flag_img, save_path)
            print(f"  已生成：{save_path}")

        print("图片资源生成完成!")

        # 生成音效
        print("正在生成音效...")
        sound_types = ["click", "battle", "victory", "defeat", "march", "build"]
        for sound_type in sound_types:
            wav_data = self.generate_sound_effect(sound_type)
            save_path = os.path.join(self.sounds_dir, f"{sound_type}.wav")
            with open(save_path, 'wb') as f:
                f.write(wav_data)
            print(f"  已生成：{save_path}")

        # 生成背景音乐
        print("正在生成背景音乐...")
        music_data = self.generate_background_music(60)  # 60 秒循环
        music_path = os.path.join(self.sounds_dir, "bgm_main.wav")
        with open(music_path, 'wb') as f:
            f.write(music_data)
        print(f"  已生成：{music_path}")

        print("资源生成完成!")

    def generate_sound_effect(self, sound_type: str) -> bytes:
        """生成音效 WAV 数据
        程序化生成简单的复古游戏音效

        Args:
            sound_type: 音效类型 (click, battle, victory, defeat, march, build)

        Returns:
            bytes WAV 格式音频数据
        """
        sample_rate = 22050
        duration = 0.3
        num_samples = int(sample_rate * duration)

        samples = []

        if sound_type == "click":
            # UI 点击音效 - 简短的滴答声
            for i in range(num_samples):
                t = i / sample_rate
                # 高频短促音
                value = int(127 * math.sin(2 * math.pi * 800 * t) * math.exp(-t * 30))
                samples.append(max(-128, min(127, value)))

        elif sound_type == "battle":
            # 战斗音效 - 撞击声
            duration = 0.5
            num_samples = int(sample_rate * duration)
            for i in range(num_samples):
                t = i / sample_rate
                # 低频撞击 + 噪声
                value = int(100 * math.sin(2 * math.pi * 150 * t) * math.exp(-t * 10))
                # 添加一些"噪声"模拟撞击
                noise = int(50 * (i % 7 - 3.5) / 3.5 * math.exp(-t * 15))
                samples.append(max(-128, min(127, value + noise)))

        elif sound_type == "victory":
            # 胜利音效 - 上升的琶音
            duration = 1.0
            num_samples = int(sample_rate * duration)
            notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
            for i in range(num_samples):
                t = i / sample_rate
                note_index = min(int(t * 4), 3)
                value = int(100 * math.sin(2 * math.pi * notes[note_index] * t))
                value = int(value * math.exp(-t * 3))
                samples.append(max(-128, min(127, value)))

        elif sound_type == "defeat":
            # 失败音效 - 下降的音调
            duration = 1.0
            num_samples = int(sample_rate * duration)
            for i in range(num_samples):
                t = i / sample_rate
                freq = 400 - 200 * t  # 频率下降
                value = int(100 * math.sin(2 * math.pi * freq * t) * math.exp(-t * 2))
                samples.append(max(-128, min(127, value)))

        elif sound_type == "march":
            # 行军音效 - 节奏鼓点
            duration = 0.8
            num_samples = int(sample_rate * duration)
            for i in range(num_samples):
                t = i / sample_rate
                # 模拟鼓点节奏
                beat = math.sin(2 * math.pi * 3 * t) > 0.7
                if beat:
                    value = int(80 * math.sin(2 * math.pi * 100 * t) * math.exp(-((t % 0.33) * 10)))
                else:
                    value = 0
                samples.append(max(-128, min(127, value)))

        elif sound_type == "build":
            # 建造音效 - 上升的叮当声
            duration = 0.6
            num_samples = int(sample_rate * duration)
            for i in range(num_samples):
                t = i / sample_rate
                freq = 600 + 300 * t  # 频率上升
                value = int(80 * math.sin(2 * math.pi * freq * t) * math.exp(-t * 5))
                samples.append(max(-128, min(127, value)))

        else:
            # 默认静音
            samples = [0] * num_samples

        # 生成 WAV 文件数据
        return self._create_wav_data(samples, sample_rate)

    def generate_background_music(self, duration: int = 60) -> bytes:
        """生成背景音乐 WAV 数据
        程序化生成简单的循环背景音乐

        Args:
            duration: 音乐时长 (秒)

        Returns:
            bytes WAV 格式音频数据
        """
        sample_rate = 22050
        num_samples = sample_rate * duration

        # 五声音阶：宫商角徵羽 (C D E G A)
        pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00]  # C4, D4, E4, G4, A4
        bass_pentatonic = [f / 2 for f in pentatonic]  # 低音

        samples = []
        beat_duration = 0.5  # 每个音符的时长

        for i in range(num_samples):
            t = i / sample_rate
            beat_index = int(t / beat_duration)

            # 主旋律 - 使用五声音阶
            melody_note = pentatonic[beat_index % 5]
            melody_phase = (t % beat_duration) / beat_duration

            # 伴奏低音
            bass_note = bass_pentatonic[(beat_index // 2) % 5]

            # 混合主旋律和伴奏
            melody_vol = math.sin(math.pi * melody_phase) * math.exp(-melody_phase * 0.5)
            bass_vol = 0.3 * math.sin(math.pi * melody_phase)

            melody = 60 * math.sin(2 * math.pi * melody_note * t) * melody_vol
            bass = 40 * math.sin(2 * math.pi * bass_note * t) * bass_vol

            # 添加和声
            harmony_note = pentatonic[(beat_index + 2) % 5]
            harmony = 30 * math.sin(2 * math.pi * harmony_note * t) * melody_vol * 0.5

            value = int(melody + bass + harmony)
            samples.append(max(-128, min(127, value)))

        return self._create_wav_data(samples, sample_rate)

    def _create_wav_data(self, samples: list, sample_rate: int) -> bytes:
        """创建 WAV 文件数据

        Args:
            samples: 音频样本列表 (-128 到 127)
            sample_rate: 采样率

        Returns:
            bytes WAV 格式数据
        """
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(1)  # 8 位
            wav_file.setframerate(sample_rate)

            for sample in samples:
                # 转换为 8 位无符号
                unsigned_sample = sample + 128
                wav_file.writeframes(struct.pack('B', max(0, min(255, unsigned_sample))))

        return buffer.getvalue()


# 全局生成器实例
def generate_resources():
    """生成游戏资源"""
    # 获取资源目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(base_dir, 'resources')

    generator = ResourceGenerator(resources_dir)
    generator.generate_all_resources()


if __name__ == "__main__":
    generate_resources()
