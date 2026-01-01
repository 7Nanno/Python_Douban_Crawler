import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def crawl_douban():
    """爬取豆瓣电影Top10"""
    print("🚀 开始爬取豆瓣电影...")
    
    url = "https://movie.douban.com/top250"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"✅ 访问成功！状态码: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找所有的电影条目
        items = soup.find_all('div', class_='item')
        print(f"🔍 找到 {len(items)} 个电影条目")
        
        if len(items) == 0:
            print("❌ 没找到电影数据")
            return []
        
        movies = []
        
        # 只取前10个
        for i, item in enumerate(items[:10], 1):
            try:
                # 找电影名称
                title_span = item.find('span', class_='title')
                if not title_span:
                    print(f"⚠️ 第{i}个电影没找到标题，跳过")
                    continue
                title = title_span.text
                
                # 找评分
                rating_span = item.find('span', class_='rating_num')
                if not rating_span:
                    print(f"⚠️ {title} 没找到评分，跳过")
                    continue
                rating = rating_span.text
                
                # 找评价人数
                star_div = item.find('div', class_='star')
                people = "未知"
                if star_div:
                    all_spans = star_div.find_all('span')
                    if len(all_spans) > 0:
                        people = all_spans[-1].text.replace('人评价', '').strip()
                
                # 添加到列表
                movies.append({
                    '电影名': title,
                    '评分': rating,
                    '评价人数': people
                })
                
                print(f"✅ {i}. {title} - {rating}分 ({people}人)")
                
            except Exception as e:
                print(f"⚠️ 解析第{i}个电影时出错: {e}")
                continue
        
        print(f"\n✅ 成功爬取 {len(movies)} 部电影")
        return movies
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        return []

def save_excel(movies):
    """保存到Excel"""
    if not movies:
        print("❌ 没有数据可保存")
        return
    
    try:
        df = pd.DataFrame(movies)
        filename = f"豆瓣Top10_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        df.to_excel(filename, index=False)
        
        print(f"\n🎉 成功！文件已保存：{filename}")
        print(f"📊 共保存 {len(movies)} 部电影\n")
        
        # 显示表格
        print("="*60)
        print(df.to_string(index=False))
        print("="*60)
        
    except Exception as e:
        print(f"❌ 保存Excel失败: {e}")

if __name__ == "__main__":
    print("="*60)
    print("     豆瓣电影Top10爬虫")
    print("="*60)
    
    movies = crawl_douban()
    save_excel(movies)
    
    print("\n" + "="*60)
    print("     ✨ 程序执行完成！")
    print("="*60)
