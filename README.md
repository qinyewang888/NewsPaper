# 热点新闻获取器

跨平台的热点新闻获取工具，自动获取前一天的热点新闻，按类别分类并保存到桌面。

**版本**: 1.0.0  
**许可证**: MIT License  
**支持平台**: Windows、macOS、Linux

---

## 📋 目录

- [功能特点](#功能特点)
- [快速开始](#快速开始)
- [使用方法](#使用方法)
- [输出说明](#输出说明)
- [新闻源列表](#新闻源列表)
- [系统要求](#系统要求)
- [故障排除](#故障排除)
- [更新日志](#更新日志)
- [技术说明](#技术说明)
- [许可证](#许可证)

---

## ✨ 功能特点

- 🌍 **多源支持**: 22个新闻源（10个国内 + 12个国外）
- 📊 **智能分类**: 自动按类别分类（AI、科技、金融、教育、政策、娱乐、国际、社会、体育等）
- 📁 **自动保存**: 保存到桌面"每日新闻"文件夹（使用系统默认路径）
- ⚡ **快速高效**: 并发获取，速度快
- 📅 **自动获取**: 自动获取前一天的新闻
- 🔄 **智能去重**: 自动去除重复新闻
- 🚀 **自动打开**: 运行完成后自动打开生成的新闻文件
- 💻 **跨平台**: 支持 Windows、macOS、Linux
- 🎯 **简单易用**: 双击运行，无需配置

---

## 🚀 快速开始

### 方法一：一键安装（推荐）

**所有平台通用**：运行一个脚本即可完成安装！

**Windows:**
```bash
python setup.py
```

**macOS / Linux:**
```bash
python3 setup.py
```

脚本会自动：
- ✅ 检测您的操作系统
- ✅ 打包对应平台的应用
- ✅ 在桌面创建快捷方式
- ✅ 添加到应用程序（macOS/Linux）

安装完成后，直接双击桌面快捷方式即可使用！

---

### 方法二：使用已打包的应用

如果已经有打包好的应用：

**Windows:**
- 打开 `dist` 文件夹
- 双击 `热点新闻.exe` 运行

**macOS:**
- 打开 `dist` 文件夹
- 双击 `热点新闻.app` 运行
- 如果提示"无法打开"，请右键点击app，选择"打开"

**Linux:**
- 打开 `dist` 文件夹
- 运行 `./热点新闻`

---

### 方法三：运行源代码

**Windows:**
```bash
pip install -r requirements.txt
python NewsPaper.py
```

**macOS / Linux:**
```bash
pip3 install -r requirements.txt
python3 NewsPaper.py
```

---

## 📖 使用方法

### 方法一：使用打包好的应用（推荐）

#### Windows
1. 找到 `dist\热点新闻.exe` 文件
2. 双击运行
3. 程序会自动获取新闻并保存到桌面

#### macOS
1. 找到 `dist\热点新闻.app` 文件
2. 双击运行
3. 如果提示"无法打开"，请：
   - 右键点击app，选择"打开"
   - 或在"系统偏好设置 > 安全性与隐私"中允许
4. 程序会自动获取新闻并保存到桌面

**提示**：
- 可以将应用复制到桌面或任何位置
- 可以创建桌面快捷方式
- 不需要安装 Python，直接运行即可

### 方法二：运行源代码

#### Windows
```bash
python NewsPaper.py
```

#### macOS/Linux
```bash
python3 NewsPaper.py
```

---

## 📂 输出说明

### 文件位置
- **默认路径**: `桌面\每日新闻\YYYY-MM-DD.md`
- **文件格式**: Markdown 格式
- **文件命名**: 使用前一天的日期（例如：`2025-12-29.md`）

### 文件内容
- 按类别分类的新闻列表
- 每条新闻包含标题、链接和来源
- 自动生成时间和版本信息

### 自动功能
- 自动创建"每日新闻"文件夹（如果不存在）
- 自动打开生成的新闻文件
- 使用系统默认程序打开（Markdown 阅读器或文本编辑器）

---

## 📰 新闻源列表

### 国内新闻源（10个）
- 澎湃新闻
- 新浪新闻
- 网易新闻
- 腾讯新闻
- 人民网
- 新华网
- 央视新闻
- 观察者网
- 36氪
- 虎嗅

### 国外新闻源（12个）
- BBC中文
- BBC新闻
- BBC科技
- CNN
- CNN科技
- Reuters
- Reuters科技
- TechCrunch
- The Guardian
- NY Times
- WSJ
- NPR

---

## 💻 系统要求

- **Python**: 3.6 或更高版本（如果运行源代码）
- **网络连接**: 需要网络连接才能获取新闻
- **磁盘空间**: 约 50MB（打包后的应用）
- **操作系统**: Windows 7+、macOS 10.12+、Linux

---

## 📦 打包应用

### 🚀 一键安装（推荐）

**最简单的方式**：一个脚本，所有平台通用！

#### 所有平台通用方法

**Windows:**
```bash
python setup.py
```

**macOS / Linux:**
```bash
python3 setup.py
```

**就这么简单！** 脚本会自动：
- ✅ 检测您的操作系统
- ✅ 打包对应平台的应用
- ✅ 在桌面创建快捷方式
- ✅ macOS: 自动添加到应用程序文件夹
- ✅ Linux: 自动添加到应用程序菜单

**一键安装功能**：
- ✅ 跨平台：一个脚本，所有系统都能用
- ✅ 自动检测：自动识别 Windows、macOS、Linux
- ✅ 自动打包：自动安装依赖并打包应用
- ✅ 自动配置：自动创建快捷方式和添加到应用程序

---

### 打包后的文件
- **Windows**: `dist\热点新闻.exe` (约14MB) - 在 Windows 上打包
- **macOS**: `dist\热点新闻.app` (约20-30MB) - 在 macOS 上打包
- **Linux**: `dist\热点新闻` (约20-30MB) - 在 Linux 上打包

⚠️ **注意**：每个平台的可执行文件必须在对应平台上打包生成，无法跨平台编译。

### 创建发布包

#### 方法一：手动打包

1. 创建一个新文件夹，命名为 `热点新闻获取器_v1.0.0`

2. 根据平台复制文件：
   
   **Windows版本：**
   - `dist\热点新闻.exe`
   - `README.md`
   - `LICENSE`
   
   **macOS版本：**
   - `dist\热点新闻.app`
   - `README.md`
   - `LICENSE`

3. 将该文件夹压缩成 zip 文件

4. 压缩包就准备好了！

#### 最终压缩包内容

**Windows版本：**
```
热点新闻获取器_v1.0.0_Windows.zip
├── 热点新闻.exe      (约14MB)
├── README.md         (使用说明)
└── LICENSE           (MIT许可证)
```

**macOS版本：**
```
热点新闻获取器_v1.0.0_macOS.zip
├── 热点新闻.app      (约20-30MB)
├── README.md         (使用说明)
└── LICENSE           (MIT许可证)
```

#### 文件大小参考

- Windows exe: 约 14 MB
- macOS app: 约 20-30 MB
- README.md: 约 10 KB
- LICENSE: 约 1 KB

#### 发送给用户的说明

**Windows用户：**
1. 解压压缩包
2. 双击运行 `热点新闻.exe`
3. 程序会自动获取新闻并保存到桌面

**macOS用户：**
1. 解压压缩包
2. 双击运行 `热点新闻.app`
3. 如果提示"无法打开"，请：
   - 右键点击app，选择"打开"
   - 或在"系统偏好设置 > 安全性与隐私"中允许

---

## 🔧 故障排除

### 问题：找不到 Python

**Windows**:
- 确保已安装 Python 并添加到系统 PATH
- 从 [python.org](https://www.python.org/downloads/) 下载安装

**macOS**:
```bash
brew install python3
```

**Linux**:
```bash
sudo apt-get install python3
```

### 问题：依赖安装失败

尝试使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题：网络连接超时

- 检查网络连接
- 某些新闻源可能需要科学上网
- 程序会自动跳过无法访问的源
- 等待一段时间后重试

### 问题：文件保存失败

- 确保有桌面写入权限
- 检查桌面路径是否正确
- 如果桌面不可用，程序会自动使用用户主目录

### 问题：无法打开文件

- 确保系统已安装 Markdown 阅读器或文本编辑器
- 可以手动打开文件：`桌面\每日新闻\YYYY-MM-DD.md`

### 问题：打包后的应用无法运行

- 检查是否有杀毒软件拦截（添加信任即可）
- 确保文件完整性
- 尝试重新打包

---

## 📝 更新日志

### [1.0.0] - 2025-12-30

#### 新增功能
- ✨ 自动获取前一天的热点新闻
- ✨ 支持22个新闻源（10个国内 + 12个国外）
- ✨ 自动按类别分类（AI、科技、金融、教育、政策、娱乐、国际、社会、体育等）
- ✨ 自动保存到桌面"每日新闻"文件夹
- ✨ 自动打开生成的新闻文件
- ✨ 跨平台支持（Windows、macOS、Linux）
- ✨ 并发获取，速度快
- ✨ 智能去重
- ✨ 完整的错误处理和用户提示

#### 技术特性
- 使用 RSS feed 获取新闻，速度快
- 多线程并发处理（最多8个线程）
- 自动处理编码问题
- 完善的异常处理
- 使用系统默认路径（桌面）
- 自动检测桌面路径（支持中文系统）

#### 修复
- 修复了 Windows 中文路径问题
- 修复了 macOS 路径获取问题
- 优化了错误提示信息
- 改进了文件打开功能

---

## 🔬 技术说明

### 技术栈
- **语言**: Python 3.6+
- **主要库**: 
  - `feedparser` - RSS 解析
  - `requests` - HTTP 请求
  - `concurrent.futures` - 并发处理

### 架构特点
- **并发处理**: 使用线程池并发获取多个新闻源
- **智能分类**: 基于关键词匹配的新闻分类算法
- **路径处理**: 跨平台桌面路径自动检测
- **错误处理**: 完善的异常处理和用户提示
- **编码支持**: 自动处理 UTF-8 编码问题

### 性能优化
- 并发请求（最多8个线程）
- 请求超时控制（8秒）
- 智能去重算法
- 限制每个源的获取数量

---

## 📄 许可证

MIT License

Copyright (c) 2025 NewsPaper Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📞 反馈与支持

如有问题或建议，欢迎反馈。

---

**享受使用！** 🎉
