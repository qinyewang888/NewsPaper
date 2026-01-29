#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
热点新闻获取器
自动获取前一天的热点新闻，按类别分类并保存到桌面

版本: 1.0.0
作者: NewsPaper Team
许可证: MIT License
"""

import sys
import os
import datetime
import requests
import feedparser
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 版本信息
VERSION = "1.0.0"
APP_NAME = "热点新闻获取器"
APP_AUTHOR = "NewsPaper Team"

# 设置控制台编码为UTF-8（跨平台支持）
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        os.environ['PYTHONIOENCODING'] = 'utf-8'
else:
    # macOS 和 Linux: 设置环境变量确保UTF-8编码
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 国内新闻源RSS
DOMESTIC_RSS_SOURCES = [
    {'name': '澎湃新闻', 'url': 'https://www.thepaper.cn/feed_channel_25951'},
    {'name': '新浪新闻', 'url': 'https://news.sina.com.cn/roll'},
    {'name': '网易新闻', 'url': 'https://www.163.com/news/rss'},
    {'name': '腾讯新闻', 'url': 'https://news.qq.com/newsgn/rss_newsgn.xml'},
    {'name': '人民网', 'url': 'http://www.people.com.cn/rss/politics.xml'},
    {'name': '新华网', 'url': 'http://www.xinhuanet.com/rss.xml'},
    {'name': '央视新闻', 'url': 'https://rss.cctv.com/rss/cctvnews.xml'},
    {'name': '观察者网', 'url': 'https://www.guancha.cn/rss'},
    {'name': '36氪', 'url': 'https://36kr.com/feed'},
    {'name': '虎嗅', 'url': 'https://www.huxiu.com/rss/1.xml'},
]

# 国外新闻源RSS
INTERNATIONAL_RSS_SOURCES = [
    {'name': 'BBC中文', 'url': 'https://feeds.bbci.co.uk/zhongwen/simp/rss.xml'},
    {'name': 'BBC新闻', 'url': 'https://feeds.bbci.co.uk/news/rss.xml'},
    {'name': 'BBC科技', 'url': 'https://feeds.bbci.co.uk/news/technology/rss.xml'},
    {'name': 'CNN', 'url': 'http://rss.cnn.com/rss/edition.rss'},
    {'name': 'CNN科技', 'url': 'http://rss.cnn.com/rss/edition_technology.rss'},
    {'name': 'Reuters', 'url': 'https://www.reuters.com/rssFeed/worldNews'},
    {'name': 'Reuters科技', 'url': 'https://www.reuters.com/rssFeed/technologyNews'},
    {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/'},
    {'name': 'The Guardian', 'url': 'https://www.theguardian.com/world/rss'},
    {'name': 'NY Times', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'},
    {'name': 'WSJ', 'url': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml'},
    {'name': 'NPR', 'url': 'https://feeds.npr.org/1001/rss.xml'},
]

# 合并所有RSS源
ALL_RSS_SOURCES = DOMESTIC_RSS_SOURCES + INTERNATIONAL_RSS_SOURCES

# 新闻类别显示顺序
CATEGORY_ORDER = ['AI', '科技', '金融', '教育', '政策', '娱乐', '国际', '社会', '体育', '其他']

# 新闻类别关键词（更精确的匹配）
NEWS_CATEGORIES = {
    'AI': [' AI ', '人工智能', 'GPT', 'LLM', '大模型', '机器学习', '深度学习', '神经网络', '自然语言处理', 'NLP', '计算机视觉', 'ChatGPT', 'OpenAI', 'artificial intelligence', 'machine learning', 'deep learning', 'neural network', 'AI Lab', 'AI智能'],
    '科技': ['科技', '技术', '创新', '互联网', '5G', '6G', '芯片', '半导体', '电子', '数字化', '智能', 'Tech', 'technology', 'innovation', 'digital', 'startup', '卫星', '通信', 'software', 'hardware'],
    '金融': ['金融', '经济', '股市', '投资', '基金', '债券', '货币', '银行', '利率', '通胀', '通货膨胀', '降息', '加息', '融资', 'finance', 'economy', 'stock', 'market', 'investment', 'funding', 'IPO'],
    '教育': ['教育', '学校', '大学', '高校', '学生', '教师', '课程', '学习', '培训', '考试', '教学', 'education', 'university', 'school', 'college'],
    '政策': ['政策', '法规', '条例', '规定', '文件', '通知', '决定', '实施', '颁布', '发布', '国务院', '部委', '监管', '立法', '法律', 'policy', 'regulation', 'law', 'government'],
    '娱乐': ['娱乐', '明星', '电影', '电视剧', '综艺', '音乐', '演唱会', '艺人', '导演', '演员', '歌手', '网红', '剧集', '票房', '流量', 'entertainment', 'movie', 'film', 'music', 'celebrity', 'TV'],
    '国际': ['国际', '外交', '贸易', '战争', '冲突', '和平', '联合国', '国际关系', '乌克兰', 'Russia', 'Ukraine', 'Trump', 'Zelensky', 'international', 'diplomacy', 'trade war', 'war', 'conflict', 'peace', 'election', 'Myanmar'],
    '社会': ['社会', '民生', '就业', '医疗', '健康', '养老', '住房', '交通', '环境', '环保', 'society', 'health', 'employment', 'environment', 'hospital', 'care', 'wellness'],
    '体育': ['体育', '足球', '篮球', '奥运', '比赛', '运动', 'sport', 'football', 'basketball', 'olympic', 'game', 'tennis', 'defeats'],
    '其他': []  # 默认类别
}

# 配置常量
MAX_WORKERS = 8  # 最大并发线程数
RSS_TIMEOUT = 8  # RSS请求超时时间（秒）
MAX_ITEMS_PER_SOURCE = 15  # 每个源最多获取的新闻数量
MAX_DISPLAY_COUNT = 15  # 控制台最多显示的新闻数量

# 线程锁用于打印
print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    """线程安全的打印函数"""
    with print_lock:
        print(*args, **kwargs)

def categorize_news(title):
    """根据标题判断新闻类别"""
    title_lower = title.lower()
    # 在标题前后添加空格，避免部分匹配
    title_with_spaces = ' ' + title_lower + ' '
    
    # 按优先级检查类别（更具体的类别优先，排除"其他"）
    category_priority = [c for c in CATEGORY_ORDER if c != '其他']
    
    for category in category_priority:
        keywords = NEWS_CATEGORIES[category]
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # 对于英文关键词，检查单词边界；对于中文，直接检查
            if keyword_lower.isascii():
                # 英文关键词：检查单词边界
                if f' {keyword_lower} ' in title_with_spaces or title_lower.startswith(keyword_lower + ' ') or title_lower.endswith(' ' + keyword_lower):
                    return category
            else:
                # 中文关键词：直接检查
                if keyword in title:
                    return category
    
    # 如果没有匹配，返回"其他"
    return '其他'

def get_news_from_rss(rss_url, source_name, target_date=None, timeout=RSS_TIMEOUT, max_items=MAX_ITEMS_PER_SOURCE):
    """从RSS feed获取新闻（带超时控制）
    
    Args:
        rss_url: RSS源URL
        source_name: 新闻源名称
        target_date: 目标日期（date对象），如果为None则使用昨天
        timeout: 超时时间
        max_items: 最大获取数量
    """
    news_list = []
    try:
        # 使用requests获取RSS，设置超时
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(rss_url, headers=headers, timeout=timeout)
        response.raise_for_status()  # 检查HTTP状态码
        feed = feedparser.parse(response.content)
        
        # 如果没有指定目标日期，使用昨天
        if target_date is None:
            target_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        
        # 检查是否有条目
        if not hasattr(feed, 'entries') or not feed.entries:
            return []
        
        for entry in feed.entries[:max_items]:
            try:
                # 解析发布日期
                pub_date = None
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime.datetime(*entry.published_parsed[:6]).date()
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime.datetime(*entry.updated_parsed[:6]).date()
                except (ValueError, TypeError, IndexError):
                    pub_date = None
                
                # 只接受目标日期的新闻（如果没有日期信息，也接受，但标记为目标日期）
                if pub_date is None or pub_date == target_date:
                    title = entry.get('title', '').strip()
                    link = entry.get('link', '')
                    
                    if title and len(title) > 5:
                        news_list.append({
                            'title': title,
                            'url': link,
                            'source': source_name,
                            'date': pub_date or target_date
                        })
            except (KeyError, AttributeError, ValueError, TypeError):
                continue
        
    except requests.Timeout:
        safe_print(f"    [-] {source_name}: 超时")
        return []
    except requests.RequestException as e:
        safe_print(f"    [-] {source_name}: 网络错误 ({str(e)[:30]})")
        return []
    except Exception as e:
        safe_print(f"    [-] {source_name}: 失败 ({str(e)[:30]})")
        return []
    
    return news_list

def fetch_news_worker(source, target_date):
    """工作线程函数"""
    news_list = get_news_from_rss(source['url'], source['name'], target_date)
    if news_list:
        safe_print(f"    [+] {source['name']}: 找到 {len(news_list)} 条")
    return source['name'], news_list

def get_desktop_path():
    """获取桌面路径（跨平台支持）
    
    Returns:
        str: 桌面路径
    """
    if sys.platform == 'win32':
        # Windows: 优先使用注册表获取真实桌面路径
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
        except (ImportError, OSError):
            pass
        
        # 备用方案：尝试标准路径
        home = os.path.expanduser('~')
        possible_paths = [
            os.path.join(home, 'Desktop'),
            os.path.join(home, '桌面'),  # 中文系统
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # 如果都不存在，使用标准路径（即使不存在也会创建）
        return os.path.join(home, 'Desktop')
        
    elif sys.platform == 'darwin':  # macOS
        home = os.path.expanduser('~')
        desktop = os.path.join(home, 'Desktop')
        return desktop
        
    else:  # Linux 和其他 Unix 系统
        home = os.path.expanduser('~')
        desktop = os.path.join(home, 'Desktop')
        return desktop

def get_desktop_news_folder():
    """获取桌面上的每日新闻文件夹路径，如果不存在则创建
    
    Returns:
        str: 每日新闻文件夹路径
    """
    try:
        desktop = get_desktop_path()
        
        # 如果桌面路径不存在，尝试创建
        if not os.path.exists(desktop):
            try:
                os.makedirs(desktop, exist_ok=True)
            except Exception as e:
                # 如果无法创建桌面，使用用户主目录
                desktop = os.path.expanduser('~')
                print(f"[!] 警告: 无法访问桌面，将使用用户目录: {desktop}")
        
        # 创建每日新闻文件夹
        news_folder = os.path.join(desktop, '每日新闻')
        if not os.path.exists(news_folder):
            try:
                os.makedirs(news_folder, exist_ok=True)
                print(f"[*] 已创建文件夹: {news_folder}")
            except Exception as e:
                raise Exception(f"无法创建新闻文件夹 {news_folder}: {str(e)}")
        
        return news_folder
        
    except Exception as e:
        # 如果所有方法都失败，使用用户主目录
        fallback_path = os.path.join(os.path.expanduser('~'), '每日新闻')
        try:
            os.makedirs(fallback_path, exist_ok=True)
            print(f"[!] 警告: 使用备用路径: {fallback_path}")
            return fallback_path
        except:
            raise Exception(f"无法创建新闻文件夹，请检查文件权限: {str(e)}")

def open_file_with_default_app(file_path):
    """使用系统默认程序打开文件（跨平台）
    
    Args:
        file_path: 文件路径
    """
    try:
        if sys.platform == 'win32':
            os.startfile(file_path)
        elif sys.platform == 'darwin':  # macOS
            os.system(f'open "{file_path}"')
        else:  # Linux
            os.system(f'xdg-open "{file_path}"')
    except Exception as e:
        print(f"[!] 无法自动打开文件: {str(e)}")
        print(f"    请手动打开: {file_path}")

def save_to_markdown(news_by_category, unique_news, date_str):
    """将新闻保存为Markdown文件（按类别分类）
    
    Args:
        news_by_category: 按类别分类的新闻字典
        unique_news: 去重后的新闻列表
        date_str: 日期字符串（格式：YYYY-MM-DD）
    
    Returns:
        str: 保存的文件路径
    """
    # 获取保存文件夹（使用桌面路径）
    news_folder = get_desktop_news_folder()
    filename = os.path.join(news_folder, f"{date_str}.md")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 写入标题
            f.write(f"# 热点新闻日报 {date_str}\n\n")
            f.write(f"*自动生成于 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"**共 {len(unique_news)} 条热点新闻**\n\n")
            f.write("---\n\n")
            
            # 按类别写入新闻
            for category in CATEGORY_ORDER:
                if category in news_by_category and news_by_category[category]:
                    news_list = news_by_category[category]
                    f.write(f"## {category} ({len(news_list)} 条)\n\n")
                    
                    for i, news in enumerate(news_list, 1):
                        # 转义Markdown特殊字符
                        title = (news['title']
                                .replace('\\', '\\\\')
                                .replace('|', '\\|')
                                .replace('*', '\\*')
                                .replace('_', '\\_')
                                .replace('[', '\\[')
                                .replace(']', '\\]'))
                        # 来源作为标注
                        f.write(f"{i}. [{title}]({news['url']}) *({news['source']})*\n")
                    
                    f.write("\n")
            
            # 写入页脚
            f.write("---\n\n")
            f.write(f"*此日报由 {APP_NAME} v{VERSION} 自动生成*\n")
            f.write(f"*生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            f.write(f"*许可证: MIT License*\n")
        
        return filename
    except IOError as e:
        raise Exception(f"无法写入文件 {filename}: {str(e)}")
    except Exception as e:
        raise Exception(f"保存文件时出错: {str(e)}")

def get_yesterday_hot_news():
    """获取前一天的热点新闻（使用并发加速）"""
    print("=" * 70)
    print(f"{APP_NAME} v{VERSION}")
    print("=" * 70)
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_date = yesterday.date()
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    print(f"正在获取 {yesterday_str} 的热点新闻...")
    print(f"共 {len(ALL_RSS_SOURCES)} 个新闻源（国内: {len(DOMESTIC_RSS_SOURCES)}, 国外: {len(INTERNATIONAL_RSS_SOURCES)}）")
    print("=" * 70)
    print()
    
    all_news = []
    
    # 使用线程池并发获取新闻
    print(f"[*] 正在并发获取新闻（最多{MAX_WORKERS}个线程）...")
    print()
    
    success_count = 0
    fail_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务，传递目标日期
        future_to_source = {
            executor.submit(fetch_news_worker, source, yesterday_date): source 
            for source in ALL_RSS_SOURCES
        }
        
        # 收集结果
        for future in as_completed(future_to_source):
            try:
                source_name, news_list = future.result(timeout=10)
                all_news.extend(news_list)
                if news_list:
                    success_count += 1
            except Exception:
                source = future_to_source[future]
                fail_count += 1
                safe_print(f"    [-] {source['name']}: 处理失败")
    
    print()
    print(f"[*] 完成：成功 {success_count} 个源，失败 {fail_count} 个源")
    print()
    
    # 去重
    unique_news = []
    seen_titles = set()
    for news in all_news:
        title_lower = news['title'].lower().strip()
        # 更智能的去重：检查标题相似度
        if title_lower and len(news['title']) > 5:
            # 简单去重：完全相同的标题
            if title_lower not in seen_titles:
                unique_news.append(news)
                seen_titles.add(title_lower)
    
    # 按类别分类
    news_by_category = {}
    for news in unique_news:
        category = categorize_news(news['title'])
        if category not in news_by_category:
            news_by_category[category] = []
        news_by_category[category].append(news)
    
    # 显示结果
    print("=" * 70)
    print(f"{yesterday_str} 热点新闻 (共 {len(unique_news)} 条)")
    print("=" * 70)
    print()
    
    if not unique_news:
        print(f"{yesterday_str} 暂时没有找到热点新闻，请稍后再试。")
        print("提示：可能是网络问题或新闻源暂时不可用。")
        return
    
    # 显示类别统计
    print("\n类别统计：")
    for category in CATEGORY_ORDER:
        if category in news_by_category and news_by_category[category]:
            count = len(news_by_category[category])
            print(f"  {category}: {count} 条")
    print()
    
    # 按类别显示新闻
    for category in CATEGORY_ORDER:
        if category in news_by_category and news_by_category[category]:
            news_list = news_by_category[category]
            print("\n" + "=" * 70)
            print(f"【{category}】({len(news_list)} 条)")
            print("=" * 70)
            
            # 限制显示数量，避免输出过多
            display_count = min(len(news_list), MAX_DISPLAY_COUNT)
            for i, news in enumerate(news_list[:display_count], 1):
                print(f"{i}. {news['title']}")
                print(f"   来源: {news['source']} | 链接: {news['url']}")
            if len(news_list) > display_count:
                print(f"   ... 还有 {len(news_list) - display_count} 条新闻（已保存到文件）")
    
    print()
    print("=" * 70)
    print(f"新闻获取完成！共找到 {len(unique_news)} 条热点新闻")
    print("=" * 70)
    
    # 保存为Markdown文件
    try:
        filename = save_to_markdown(news_by_category, unique_news, yesterday_str)
        file_path = os.path.abspath(filename)
        print(f"\n[✓] 结果已保存到: {file_path}")
        
        # 自动打开文件
        try:
            print("[*] 正在打开新闻文件...")
            open_file_with_default_app(file_path)
        except Exception as e:
            print(f"[!] 无法自动打开文件: {str(e)}")
            print(f"    请手动打开: {file_path}")
            
    except Exception as e:
        print(f"\n[!] 保存文件时出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        get_yesterday_hot_news()
        
        # 如果是打包后的应用，等待用户按键后退出
        if getattr(sys, 'frozen', False):
            # 打包后的应用
            print("\n" + "=" * 70)
            print("按回车键退出...")
            try:
                input()
            except:
                pass
    except KeyboardInterrupt:
        print("\n\n程序已中断")
        if getattr(sys, 'frozen', False):
            try:
                input("按回车键退出...")
            except:
                pass
    except Exception as e:
        print(f"\n[错误] 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        print("请检查网络连接或稍后再试")
        if getattr(sys, 'frozen', False):
            try:
                input("\n按回车键退出...")
            except:
                pass
