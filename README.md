# Out of Box 司法陽光網判決書API
開放政府開箱即用 - 爽爽CALL API

![status](https://img.shields.io/badge/status-developing-brightgreen.svg)
![version](https://img.shields.io/badge/version-0.1-blue.svg)

## 安裝

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



