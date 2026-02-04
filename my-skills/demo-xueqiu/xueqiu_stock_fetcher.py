import json
import requests
from typing import Dict, List, Optional
import re


class XueqiuStockFetcher:
    """
    雪球网自选股获取器
    """
    
    def __init__(self, cookie_str: str):
        """
        初始化时传入完整的Cookie字符串
        
        Args:
            cookie_str: 完整的Cookie字符串
        """
        self.cookie_str = cookie_str
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'origin': 'https://xueqiu.com',
            'referer': 'https://xueqiu.com/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'cookie': cookie_str
        }
        
    def get_watchlist(self) -> Optional[List[Dict]]:
        """
        获取自选股列表
        
        Returns:
            包含股票信息的字典列表，如果失败则返回None
        """
        url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json"
        params = {
            'size': 1000,
            'category': 1,
            'pid': 17
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 检查是否成功获取数据
            if 'data' in data and 'stocks' in data['data']:
                return data['data']['stocks']
            else:
                print("未能从响应中找到股票数据:", data)
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return None
        except json.JSONDecodeError:
            print("响应不是有效的JSON格式")
            return None
    
    def get_stock_quotes(self, symbols: List[str]) -> Optional[Dict]:
        """
        批量获取股票报价信息
        
        Args:
            symbols: 股票代码列表，如 ['SH603129', 'SH560860']
            
        Returns:
            包含股票报价信息的字典，如果失败则返回None
        """
        if not symbols:
            return None
            
        symbol_str = ','.join(symbols)
        url = "https://stock.xueqiu.com/v5/stock/batch/quote.json"
        params = {
            'symbol': symbol_str,
            'extend': 'detail',
            'is_delay_hk': 'true'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取股票报价时发生错误: {e}")
            return None
    
    def format_watchlist_table(self, stocks: List[Dict]) -> str:
        """
        将股票数据格式化为表格
        
        Args:
            stocks: 股票数据列表
            
        Returns:
            格式化的表格字符串
        """
        if not stocks:
            return "没有找到自选股数据"
        
        # 按照涨跌幅倒序排序（从高到低）
        sorted_stocks = sorted(stocks, key=lambda x: x.get('percent', x.get('chg_pct', x.get('current', 0) - x.get('prev_close', 0))), reverse=True)
        
        # 准备表头
        table = f"{'股票代码':<12} {'股票名称':<15} {'涨跌幅':<10}\n"
        table += "-" * 40 + "\n"
        
        # 添加每一行数据
        for stock in sorted_stocks:
            symbol = stock.get('symbol', 'N/A')
            name = stock.get('name', 'N/A')[:14]  # 限制名称长度
            
            # 优先使用 percent 字段（来自quote数据），然后是计算值
            percentage_change = stock.get('percent', None)
            
            if percentage_change is not None and isinstance(percentage_change, (int, float)):
                # 如果有percent字段，直接使用
                change_str = f"{percentage_change:+.2f}%"
            else:
                # 否则尝试计算
                current = stock.get('current', 0)
                prev_close = stock.get('prev_close', 0)
                
                if prev_close and abs(prev_close) > 0.001 and abs(current - prev_close) / prev_close < 10:  # 涨跌幅不超过1000%
                    # 计算涨跌幅百分比
                    calculated_change = round((current - prev_close) / prev_close * 100, 2)
                    change_str = f"{calculated_change:+.2f}%"
                else:
                    change_str = "N/A"
            
            table += f"{symbol:<12} {name:<15} {change_str:<10}\n"
        
        return table
    
    def get_formatted_watchlist(self) -> str:
        """
        获取格式化的自选股列表
        
        Returns:
            格式化的自选股表格（按涨跌幅倒序排列）
        """
        # 第一步：获取自选股列表
        watchlist = self.get_watchlist()
        
        if not watchlist:
            return "未能获取到自选股列表，请检查Cookie是否正确或是否已过期。"
        
        # 提取所有股票代码
        symbols = []
        for stock in watchlist:
            symbol = stock.get('symbol')
            if symbol:
                symbols.append(symbol)
        
        if not symbols:
            return "未在自选股列表中找到任何股票代码。"
        
        # 第二步：批量获取股票详情
        quotes_data = self.get_stock_quotes(symbols)
        
        if not quotes_data:
            # 如果无法获取详细数据，则仅显示基础列表
            print("警告：无法获取股票详细信息，将使用基础数据进行显示。")
            return self.format_watchlist_table(watchlist)
        
        # 更新watchlist中的数据（如果有更详细的报价信息）
        if 'data' in quotes_data and 'items' in quotes_data['data']:
            quote_items = {}
            for item in quotes_data['data']['items']:
                if 'quote' in item:
                    symbol = item['quote'].get('symbol')
                    if symbol:
                        quote_items[symbol] = item['quote']
            
            # 更新原始列表中的数据
            for stock in watchlist:
                symbol = stock.get('symbol')
                if symbol in quote_items:
                    # 更新价格等信息，优先使用quote中的percent字段
                    quote_info = quote_items[symbol]
                    stock['current'] = quote_info.get('current', stock.get('current', 0))
                    stock['prev_close'] = quote_info.get('prev_close', stock.get('prev_close', 0))
                    # 优先使用API返回的percent字段
                    stock['percent'] = quote_info.get('percent', quote_info.get('chg_pct', stock.get('percent', None)))
        
        # 返回格式化后的表格（已按涨跌幅倒序排列）
        return self.format_watchlist_table(watchlist)


def main():
    """
    主函数，供测试使用
    """
    print("请输入雪球网的完整Cookie字符串：")
    cookie_input = input().strip()
    
    if not cookie_input:
        print("未输入Cookie，程序退出。")
        return
    
    fetcher = XueqiuStockFetcher(cookie_input)
    
    print("\n正在获取自选股列表...")
    result = fetcher.get_formatted_watchlist()
    
    print("\n自选股列表（按涨跌幅倒序排列）：")
    print(result)


if __name__ == "__main__":
    main()