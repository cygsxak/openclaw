#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单测试脚本，验证demo-xueqiu技能的基本功能
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xueqiu_stock_fetcher import XueqiuStockFetcher

def test_class_creation():
    """测试类是否能正常创建"""
    print("测试1: 创建XueqiuStockFetcher实例")
    try:
        fetcher = XueqiuStockFetcher("test_cookie_string")
        print("✓ 成功创建XueqiuStockFetcher实例")
        return True
    except Exception as e:
        print(f"✗ 创建实例失败: {e}")
        return False

def test_headers():
    """测试请求头是否正确设置"""
    print("\n测试2: 检查请求头设置")
    try:
        fetcher = XueqiuStockFetcher("test_cookie_string")
        if 'cookie' in fetcher.headers and fetcher.headers['cookie'] == "test_cookie_string":
            print("✓ Cookie正确设置到请求头")
        else:
            print("✗ Cookie未正确设置")
            return False
            
        if 'user-agent' in fetcher.headers:
            print("✓ User-Agent正确设置")
        else:
            print("✗ User-Agent未设置")
            return False
            
        print("✓ 请求头设置正常")
        return True
    except Exception as e:
        print(f"✗ 检查请求头失败: {e}")
        return False

def test_formatting():
    """测试表格格式化功能"""
    print("\n测试3: 测试表格格式化功能")
    try:
        fetcher = XueqiuStockFetcher("test_cookie_string")
        
        # 模拟股票数据（包含percent字段用于排序测试）
        mock_stocks = [
            {
                'symbol': 'SH600000',
                'name': '浦发银行',
                'current': 10.5,
                'prev_close': 10.2,
                'percent': 2.94
            },
            {
                'symbol': 'SZ000001',
                'name': '平安银行',
                'current': 15.8,
                'prev_close': 15.6,
                'percent': 1.28
            },
            {
                'symbol': 'SZ000002',
                'name': '招商银行',
                'current': 35.0,
                'prev_close': 36.0,
                'percent': -2.78
            }
        ]
        
        table_result = fetcher.format_watchlist_table(mock_stocks)
        print("✓ 表格格式化功能正常")
        print("\n示例输出:")
        print(table_result)
        return True
    except Exception as e:
        print(f"✗ 表格格式化失败: {e}")
        return False

def main():
    print("开始测试 demo-xueqiu 技能...")
    print("="*50)
    
    tests = [
        test_class_creation,
        test_headers,
        test_formatting
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n测试完成: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！demo-xueqiu 技能基本功能正常。")
    else:
        print("⚠️  部分测试未通过，请检查代码。")

if __name__ == "__main__":
    main()