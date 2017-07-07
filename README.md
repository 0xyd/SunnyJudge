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

#### 引入套件
```python
import sunnyjudge as sj
```

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

