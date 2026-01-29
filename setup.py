#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
热点新闻获取器 - 一键安装脚本
自动检测操作系统，打包应用，并创建快捷方式
支持 Windows、macOS、Linux
"""

import sys
import os
import platform
import subprocess
import shutil

# 设置控制台编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        os.environ['PYTHONIOENCODING'] = 'utf-8'
else:
    os.environ['PYTHONIOENCODING'] = 'utf-8'

APP_NAME = "热点新闻"
APP_NAME_EN = "HotNews"
ICON_FILE = "daily_newspaper_icon.ico"

def print_header():
    """打印标题"""
    print("=" * 70)
    print("热点新闻获取器 - 一键安装工具")
    print("=" * 70)
    print()

def get_desktop_path():
    """获取桌面路径"""
    if sys.platform == 'win32':
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            )
            desktop = winreg.QueryValueEx(key, 'Desktop')[0]
            winreg.CloseKey(key)
            if os.path.exists(desktop):
                return desktop
        except:
            pass
        
        home = os.path.expanduser('~')
        possible_paths = [
            os.path.join(home, 'Desktop'),
            os.path.join(home, '桌面'),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return os.path.join(home, 'Desktop')
    elif sys.platform == 'darwin':
        return os.path.join(os.path.expanduser('~'), 'Desktop')
    else:
        return os.path.join(os.path.expanduser('~'), 'Desktop')

def check_pyinstaller():
    """检查 PyInstaller 是否已安装"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """安装 PyInstaller"""
    print("[*] 正在安装 PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[✓] PyInstaller 安装成功！")
        return True
    except:
        print("[✗] PyInstaller 安装失败，请手动运行: pip install pyinstaller")
        return False

def build_app():
    """打包应用程序"""
    current_platform = platform.system()
    print(f"[*] 检测到系统: {current_platform} {platform.machine()}")
    print()
    
    # 检查 PyInstaller
    if not check_pyinstaller():
        print("[*] PyInstaller 未安装，正在安装...")
        if not install_pyinstaller():
            return None
        print()
    
    # 确定图标文件
    icon_path = None
    if current_platform == 'Windows':
        if os.path.exists(ICON_FILE):
            icon_path = ICON_FILE
    elif current_platform == 'Darwin':
        icon_file = "daily_newspaper_icon.icns"
        if os.path.exists(icon_file):
            icon_path = icon_file
    
    # 构建 PyInstaller 命令
    windowed_flag = "--console" if current_platform == 'Windows' else "--noconsole"
    
    cmd = [
        "pyinstaller",
        f"--name={APP_NAME}",
        "--onefile",
        windowed_flag,
        "--clean",
        "--noconfirm",
        "--hidden-import=feedparser",
        "--hidden-import=requests",
        "--hidden-import=concurrent.futures",
    ]
    
    if icon_path and os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
    
    cmd.append("NewsPaper.py")
    
    print("[*] 开始打包应用...")
    print(f"[*] 执行命令: {' '.join(cmd)}")
    print()
    
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
        print("[✓] 打包成功！")
        print()
        
        # 确定输出文件路径
        if current_platform == 'Windows':
            app_path = os.path.join("dist", f"{APP_NAME}.exe")
        elif current_platform == 'Darwin':
            app_path = os.path.join("dist", f"{APP_NAME}.app")
        else:
            app_path = os.path.join("dist", APP_NAME)
        
        if os.path.exists(app_path):
            return app_path
        else:
            print(f"[✗] 找不到打包后的文件: {app_path}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"[✗] 打包失败: {e}")
        return None

def create_windows_shortcut(app_path, desktop_path):
    """在 Windows 上创建桌面快捷方式"""
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut_path = os.path.join(desktop_path, f"{APP_NAME}.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = os.path.abspath(app_path)
        shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(app_path))
        if os.path.exists(ICON_FILE):
            shortcut.IconLocation = os.path.abspath(ICON_FILE)
        shortcut.save()
        print(f"[✓] 已创建桌面快捷方式: {shortcut_path}")
        return True
    except ImportError:
        # 如果没有 win32com，使用 PowerShell 创建快捷方式
        try:
            shortcut_path = os.path.join(desktop_path, f"{APP_NAME}.lnk")
            app_abs = os.path.abspath(app_path).replace('\\', '\\\\')
            work_dir = os.path.dirname(os.path.abspath(app_path)).replace('\\', '\\\\')
            ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{app_abs}"
$Shortcut.WorkingDirectory = "{work_dir}"
$Shortcut.Save()
'''
            result = subprocess.run(["powershell", "-Command", ps_script], 
                         capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[✓] 已创建桌面快捷方式: {shortcut_path}")
                return True
            else:
                raise Exception("PowerShell 创建快捷方式失败")
        except Exception as e:
            print(f"[!] 无法创建快捷方式: {e}")
            print("    提示: 可以手动将 dist\\热点新闻.exe 创建快捷方式到桌面")
            return False
    except Exception as e:
        print(f"[!] 创建快捷方式失败: {e}")
        print("    提示: 可以手动将 dist\\热点新闻.exe 创建快捷方式到桌面")
        return False

def create_macos_shortcut(app_path, desktop_path):
    """在 macOS 上创建桌面快捷方式和添加到应用程序"""
    try:
        # 1. 复制到应用程序文件夹
        applications_path = "/Applications"
        app_dest = os.path.join(applications_path, f"{APP_NAME}.app")
        
        print(f"[*] 正在复制应用到应用程序文件夹...")
        if os.path.exists(app_dest):
            shutil.rmtree(app_dest)
        shutil.copytree(app_path, app_dest)
        print(f"[✓] 已添加到应用程序: {app_dest}")
        
        # 2. 在桌面创建别名（快捷方式）
        alias_path = os.path.join(desktop_path, f"{APP_NAME}")
        try:
            # 使用 osascript 创建别名
            script = f'''
tell application "Finder"
    make alias file at POSIX file "{desktop_path}" to POSIX file "{app_dest}"
    set name of result to "{APP_NAME}"
end tell
'''
            subprocess.run(["osascript", "-e", script], check=True, 
                         capture_output=True)
            print(f"[✓] 已创建桌面快捷方式: {alias_path}")
        except:
            # 如果创建别名失败，至少应用已经添加到应用程序了
            print(f"[!] 无法创建桌面快捷方式，但应用已添加到应用程序")
            print(f"    您可以在启动台或应用程序文件夹中找到它")
        
        return True
    except Exception as e:
        print(f"[✗] 操作失败: {e}")
        return False

def create_linux_shortcut(app_path, desktop_path):
    """在 Linux 上创建桌面快捷方式和添加到应用程序菜单"""
    try:
        # 创建 .desktop 文件
        desktop_file = os.path.join(desktop_path, f"{APP_NAME_EN}.desktop")
        
        icon_path = ""
        if os.path.exists(ICON_FILE):
            icon_path = os.path.abspath(ICON_FILE)
        
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={APP_NAME}
Comment=热点新闻获取器 - 自动获取前一天的热点新闻
Exec={os.path.abspath(app_path)}
Icon={icon_path}
Terminal=false
Categories=Utility;News;
"""
        
        with open(desktop_file, 'w', encoding='utf-8') as f:
            f.write(desktop_content)
        
        # 添加执行权限
        os.chmod(desktop_file, 0o755)
        print(f"[✓] 已创建桌面快捷方式: {desktop_file}")
        
        # 尝试添加到应用程序菜单
        applications_menu = os.path.join(os.path.expanduser('~'), 
                                        '.local', 'share', 'applications')
        if not os.path.exists(applications_menu):
            os.makedirs(applications_menu, exist_ok=True)
        
        menu_file = os.path.join(applications_menu, f"{APP_NAME_EN}.desktop")
        shutil.copy2(desktop_file, menu_file)
        print(f"[✓] 已添加到应用程序菜单: {menu_file}")
        
        return True
    except Exception as e:
        print(f"[✗] 创建快捷方式失败: {e}")
        return False

def main():
    """主函数"""
    print_header()
    
    # 检查主程序文件
    if not os.path.exists("NewsPaper.py"):
        print("[✗] 错误: 找不到 NewsPaper.py 文件")
        print("    请确保在项目根目录运行此脚本")
        input("\n按回车键退出...")
        return
    
    # 打包应用
    app_path = build_app()
    if not app_path:
        print("\n[✗] 打包失败，请检查错误信息")
        input("\n按回车键退出...")
        return
    
    print()
    print("=" * 70)
    print("[*] 正在创建快捷方式...")
    print("=" * 70)
    print()
    
    # 获取桌面路径
    desktop_path = get_desktop_path()
    if not os.path.exists(desktop_path):
        try:
            os.makedirs(desktop_path, exist_ok=True)
        except:
            print(f"[!] 无法访问桌面路径: {desktop_path}")
            print("    快捷方式创建将跳过")
            input("\n按回车键退出...")
            return
    
    # 根据系统创建快捷方式
    current_platform = platform.system()
    success = False
    
    if current_platform == 'Windows':
        success = create_windows_shortcut(app_path, desktop_path)
    elif current_platform == 'Darwin':
        success = create_macos_shortcut(app_path, desktop_path)
    else:
        success = create_linux_shortcut(app_path, desktop_path)
    
    print()
    print("=" * 70)
    if success:
        print("[✓] 全部完成！")
        print()
        print(f"应用位置: {os.path.abspath(app_path)}")
        print(f"桌面快捷方式: {desktop_path}")
        if current_platform == 'Darwin':
            print("应用程序: /Applications/热点新闻.app")
        elif current_platform != 'Windows':
            print("应用程序菜单: ~/.local/share/applications/")
    else:
        print("[!] 打包完成，但快捷方式创建可能有问题")
        print(f"应用位置: {os.path.abspath(app_path)}")
        print("    您可以手动创建快捷方式")
    print("=" * 70)
    print()
    
    input("按回车键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] 操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n[✗] 发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        sys.exit(1)

