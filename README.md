# Pygame-GUI 项目

## 项目概述

这个项目是一个基于Pygame的简单GUI库示例，主要功能是创建和管理图形用户界面控件，如输入框（Entry）。项目结构清晰，易于扩展和维护。

## 项目结构

```
project_root/
│
├── example/
│   └── Entry_test.py  # 示例文件，展示如何使用pygame_gui库
│
├── src/
│   └── pygame_gui/
│       └── control/
│           ├── control.py  # 控制对象基类和控制器类
│           └── entry.py    # 输入框控件类
```

## 主要模块说明

### 1. control.py

- **ChangeChecker 类**：用于检测对象属性的变化，并在变化时调用指定的回调函数。
- **Controller 类**：用于管理和更新控制对象，如输入框。它维护一个控制对象列表，并可以添加或移除控制对象。

### 2. entry.py

- **Entry 类**：继承自 `Control` 类，实现了一个基本的输入框控件。它支持文本输入、光标移动和文本选择功能。

## 示例说明

`Entry_test.py` 文件展示了如何使用 `pygame_gui` 库来创建一个简单的应用程序，其中包含一个输入框控件。以下是示例代码的关键部分：

1. **导入必要的模块**：
   ```python
   import logging
   import coloredlogs
   import sys, os
   import pygame_gui
   import pygame
   ```

2. **设置日志记录**：
   ```python
   logging.basicConfig(level=logging.DEBUG, filename='example.log', filemode='w', encoding='utf-8', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   coloredlogs.install(level='DEBUG')
   ```

3. **初始化Pygame和控制器**：
   ```python
   pygame.init()
   screen = pygame.display.set_mode((800, 600))
   c = pygame_gui.Controller(screen)
   ```

4. **创建和添加输入框控件**：
   ```python
   entry = pygame_gui.entry.Entry(c, pygame.font.Font(r"C:\Windows\Fonts\HarmonyOS_Sans_SC_Bold.ttf", 20))
   entry.size = pygame.Vector2(200, 30)
   entry.text = "Hello, world!"
   c.add_control(entry)
   ```

5. **事件循环**：
   ```python
   while True:
       events = pygame.event.get()
       for event in events:
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
       screen.fill((0, 0, 255))
       c.update(events)
       pygame.display.update()
   ```

## 使用方法

1. 确保已安装所需的第三方库，如 `pygame` 和 `coloredlogs`。可以通过pip安装：
   ```bash
   pip install pygame coloredlogs
   ```

2. 将 `src` 目录添加到Python的模块搜索路径中，以便导入 `pygame_gui` 模块。

3. 运行 `Entry_test.py` 文件，启动示例程序：
   ```bash
   python example/Entry_test.py
   ```

## 注意事项

1. 本项目依赖于特定的字体文件路径（例如：`r"C:\Windows\Fonts\HarmonyOS_Sans_SC_Bold.ttf"`），请确保该路径下的字体文件存在，或者根据需要修改路径。

2. 项目中的日志记录可以帮助调试和了解程序运行过程中的详细信息。

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

```
MIT License
Copyright (c) 2025 xiaoxixi222
```
