# Out of Box 司法陽光網判決書API
開放政府開箱即用 - 爽爽CALL API

![status](https://img.shields.io/badge/status-developing-brightgreen.svg)
![version](https://img.shields.io/badge/version-0.1-blue.svg)
![develop](https://img.shields.io/badge/dev-0.2.7-ff69b4.svg)

## 安裝

## 0.2.7版本新增功能(測試中)

### 測試版本安裝
```python
pip install -i https://testpypi.python.org/pypi sunnyjudge
```

### 新增功能
1. 新增列出所有法院名稱與代碼功能
2. 新增查詢法院代號功能
3. 新增查詢法院功能(Ex: 找名稱有"臺北"的法院)
4. 新增一項裁判所有的法院裁定

### 修正
1. 刪除在新版本的判決書API不存在的鍵值
2. 修正issue #1

### 功能測試

#### 列出所有法院資料
```python
sj.get_all_courts()
```

回傳值：
```python
{'courts': 
	[
		{'code': 'TPS', 'name': '最高法院', 'simple_name': '最高院'},
		{'code': 'TPA', 'name': '最高行政法院', 'simple_name': '最高行'},
		{'code': 'TPP', 'name': '公務員懲戒委員會', 'simple_name': '公懲會'},
		{'code': 'TPH', 'name': '臺灣高等法院', 'simple_name': '高院'},
		{'code': 'LCD', 'name': '福建連江地方法院', 'simple_name': '連江地院'},
		{'code': 'KMD', 'name': '福建金門地方法院', 'simple_name': '金門地院'},
		{'code': 'KSY', 'name': '臺灣高雄少年及家事法院', 'simple_name': '高雄少家法院'},
		...
	]
}
```

#### 查詢代碼代表的法院(測試)
```python
sj.get_court(code='法院代號')
```

回傳值：
```python
{
	'court': 
		{
			'code': '法院代號', 
			'name': '法院全名', 
			'simple_name': '法院簡稱'
		}
}
```

範例：
```python
sj.get_court('TPD')
```
```python
{
	'court': {
		'code': 'TPD', 
		'name': '臺灣臺北地方法院', 
		'simple_name': '臺北地院'
	}
}
```

#### 用關鍵字搜尋法院(測試)
```python
sj.search_court(keyword='法院關鍵字')
```

回傳值：
```python
[
	{ 'code': '法院1的編號', 'name': '法院1的名稱', 'simple_name': '法院1簡稱' },
	{ 'code': '法院2的編號', 'name': '法院2的名稱', 'simple_name': '法院2簡稱' },
	{ 'code': '法院3的編號', 'name': '法院3的名稱', 'simple_name': '法院3簡稱' },
	...
]
```
範例：

```python
sj.search_court('高雄')
```
```python
[
	{'code': 'KSY', 'name': '臺灣高雄少年及家事法院', 'simple_name': '高雄少家法院'},
 	{'code': 'KSD', 'name': '臺灣高雄地方法院', 'simple_name': '高雄地院'},
 	{'code': 'KSH', 'name': '臺灣高等法院高雄分院', 'simple_name': '高雄高分院'},
	{'code': 'KSB', 'name': '高雄高等行政法院', 'simple_name': '高高行'}
]
```

Python版本：3.3+

所需的套件：requests

```
pip install sunnyjudge
```

## 如何使用

### 引入套件庫

```python
import sunnyjudge as sj
```

### 抓判決

```python
sj.get_verdict(court_code='法院代號', story_type='判決類型', story_year='判決年份(中華民國)', story_word='判決常用字別', story_number='判決字號')
```

回傳值：
```python
(http status code, json result)
```

範例：

```python
sj.get_verdict('TPH', '民事', '105', '重上', '608')
```
```python
(200, {'judges_names': [...],'lawyer_names': [...],'main_content': ...})
```

### 抓時間區間內的所有判決

```python
sj.get_verdicts_by_time(start_year='起始西元年',start_mon ='起始月',start_day ='起始日', end_year='結束西元年', end_mon ='結束月', end_day ='結束日', story_type='判決類型')
```

回傳值：
```
[{判決1}, {判決2}, {判決3}, ...]
```

範例：

```python
sj.get_verdicts_by_time(2017, 1, 2, 2017, 1, 2, '民事')
```
```python
[{'adjudged_on': '2017-01-02','main_content': ..... }, {....}, ....]
```

### 抓庭期

```python
sj.get_schedules(court_code='法院代號', story_type='判決類型', story_year='判決年份(中華民國)', story_word='判決常用字別', story_number='判決字號')
```

回傳值：
```python
(http status code, json result)
```

範例：

```python
sj.get_schedules('TPH', '民事', '105', '重上', '608')
```
```python
(200, '{"schedules":[{"story":{"identity":{"type":"民事","year":105,"word":"重上","number":608},"reason":"分配表異議之訴","adjudged_on":"2017-01-19" ...}]}'))
```

## TODO

以下功能陽光網API尚未齊全，未來會持續更新，也歡迎各位跳坑！

- 律師查詢
- 檢察官查詢
- 法官查詢

## 法院與其編碼對照表

Court Name | Court Code 
---|---
司法院－刑事補償 | TPC
司法院－訴願決定 | TPU
司法院職務法庭 | TPJ
最高法院 | TPS
最高行政法院 | TPA
公務員懲戒委員會 | TPP
臺灣高等法院 | TPH
臺灣高等法院－訴願決定 | TPH
臺北高等行政法院 | TPB
臺中高等行政法院 | TCB
高雄高等行政法院 | KSB
智慧財產法院 | IPC
臺灣高等法院 臺中分院 | TCH
臺灣高等法院 臺南分院 | TNH
臺灣高等法院 高雄分院 | KSH
臺灣高等法院 花蓮分院 | HLH
臺灣臺北地方法院 | TPD
臺灣士林地方法院 | SLD
臺灣新北地方法院 | PCD
臺灣宜蘭地方法院 | ILD
臺灣基隆地方法院 | KLD
臺灣桃園地方法院 | TYD
臺灣新竹地方法院 | SCD
臺灣苗栗地方法院 | MLD
臺灣臺中地方法院 | TCD
臺灣彰化地方法院 | CHD
臺灣南投地方法院 | NTD
臺灣雲林地方法院 | ULD
臺灣嘉義地方法院 | CYD
臺灣臺南地方法院 | TND
臺灣高雄地方法院 | KSD
臺灣橋頭地方法院 | CTD
臺灣花蓮地方法院 | HLD
臺灣臺東地方法院 | TTD
臺灣屏東地方法院 | PTD
臺灣澎湖地方法院 | PHD
福建高等法院金門分院 | KMH
福建金門地方法院 | KMD
福建連江地方法院 | LCD
臺灣高雄少年及家事法院 | KYS

## 參考資料
[司法陽光網判決書API](https://5fpro.github.io/raml-api-console/?raml=https://5fpro.github.io/jrf-sunny/api/index.raml)



