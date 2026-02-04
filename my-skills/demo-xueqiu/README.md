# 雪球网自选股查询工具

这是一个用于获取雪球网自选股列表并显示实时行情的工具。

## 功能特性

1. 自动获取用户的自选股列表（最多1000只）
2. 批量查询所选股票的详细行情
3. 以表格形式展示股票代码、名称和涨跌幅
4. 智能处理异常数据，避免显示不合理的涨跌幅
5. 按涨跌幅倒序排列（从高到低）

## 使用方法

### 方法一：直接运行Python脚本

1. 运行脚本：
   ```bash
   python xueqiu_stock_fetcher.py
   ```

2. 在提示下输入雪球网的完整Cookie字符串

### 方法二：使用预设Cookie运行

创建一个运行脚本，预先填入Cookie：
   ```bash
   python run_with_cookie.py
   ```

### 方法三：在代码中使用类

```python
from xueqiu_stock_fetcher import XueqiuStockFetcher

# 创建实例，传入Cookie字符串
fetcher = XueqiuStockFetcher("your_cookie_string_here")

# 获取格式化的自选股列表
result = fetcher.get_formatted_watchlist()
print(result)
```

## Cookie获取方法

1. 登录雪球网（https://xueqiu.com）
2. 打开浏览器开发者工具（F12）
3. 进入Network（网络）标签页
4. 刷新页面或执行任意网络请求
5. 选择任一请求，查看Headers中的Cookie字段
6. 复制完整的Cookie值

## 注意事项

- Cookie可能有过期时间，请及时更新
- 请妥善保管Cookie信息，不要泄露给他人
- 遵守雪球网的使用条款和API频率限制
- 异常高的涨跌幅数据会被智能过滤，以显示更准确的信息
- 结果按涨跌幅倒序排列（从高到低）