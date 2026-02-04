# 雪球网自选股查询技能 (demo-xueqiu)

此技能用于查询雪球网用户的自选股列表，并获取这些股票的详细信息。

## 功能说明

1. 获取用户自选股列表（最多1000只）
2. 查询每只股票的实时行情信息
3. 以表格形式展示股票代码、名称和涨跌幅

## 使用方法

1. 用户需提供雪球网的登录Cookie
2. 技能会自动获取自选股列表
3. 批量查询股票详情并格式化输出

## API 接口

### 1. 获取自选股列表
```
GET https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=1&pid=17
```

Headers:
```
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.9
Cookie: [用户提供的完整Cookie]
Origin: https://xueqiu.com
Referer: https://xueqiu.com/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

### 2. 获取股票详情
```
GET https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=SH603129,SH560860&extend=detail&is_delay_hk=true
```

Headers: 同上，使用与第一步相同的Cookie

## Cookie 要求

需要包含以下关键字段的完整Cookie：
- s
- cookiesu
- xq_a_token
- xqat
- xq_r_token
- xq_id_token
- xq_is_login
- u
- 以及其他必要验证字段