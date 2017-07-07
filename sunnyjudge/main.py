import re
import json
from datetime import datetime 
from urllib.parse import urlencode

import requests

SUNNY_JUDGE_API = 'https://api.jrf.org.tw'
SUNNY_JUDGE_COURT = 'https://api.jrf.org.tw/courts'
SUNNY_JUDGE_SEARCH_API = 'https://api.jrf.org.tw/search/stories?'

def _gen_story_query(resources_type='', **kwargs):
	'''
	resource_type: 'verdict' or 'schedule'
	'''
	court_code = None
	story_type, story_year, story_word, story_number = None, None, None, None

	for key, value in kwargs.items():

		if key == 'court_code':
			court_code = value
		elif key == 'story_type':
			story_type = value
		elif key == 'story_year':
			story_year = str(value)
		elif key == 'story_word':
			story_word = value
		elif key == 'story_number':
			story_number = str(value)

	story_query = '-'.join([story_type, story_year, story_word, story_number])

	if len(resources_type) > 0:
		query = '/'.join([SUNNY_JUDGE_API, court_code, story_query, resources_type])
	else:
		query = '/'.join([SUNNY_JUDGE_API, court_code, story_query])
	
	return query


def _gen_search_query(**kwargs):

	query = {
		'page': '',
		'q[adjudged_on_gteq]': '',
		'q[adjudged_on_lteq]': '',
		'q[judges_names_cont]': '',
		'q[lawyer_names_cont]': '',
		'q[number]': '',
		'q[story_type]': '',
		'q[word]': '',
		'q[year]': ''
	}

	for key, value in kwargs.items():

		if key == 'page':
			query[key] = value
		else:	
			key = 'q[' + key + ']'
			query[key] = value

	return urlencode(query)
	

def _search(**kwargs):

	search_request = SUNNY_JUDGE_SEARCH_API + _gen_search_query(**kwargs)
	search_response = requests.get(search_request)

	status = search_response.status_code
	context = json.loads(search_response.text)
	pagination = context['pagination']['pages']

	return (status, context, pagination)

# 20170704 Y.D.: Depricate the code
# def find_verdict(court_code, story_type, story_year, story_word, story_number):
# 	'''
# 	court_code: count's number
# 	story_type: '民事', '刑事' , '行政' or '公懲'
# 	story_year: Taiwan's year
# 	story_word: Type of verdict
# 	story_number: 判決編號
# 	'''
# 	query = _gen_story_query(
# 		'verdict', 
# 		court_code=court_code,
# 		story_type=story_type, story_year=story_year, 
# 		story_word=story_word, story_number=story_number)

# 	r = requests.get(query)

# 	return (r.status_code, r.text)

# 20170704 Y.D.: Get all courts
def get_all_courts():

	r = requests.get(SUNNY_JUDGE_COURT)

	if r.status_code == 200:
		return json.loads(r.text)
	else:
		print('Fail!')


# 20170704 Y.D.: Get court's code
def get_court(code):
	query = '/'.join([SUNNY_JUDGE_COURT, code])
	res = requests.get(query)
	if res.status_code == 200:
		return json.loads(res.text)
	else:
		print('Code %s is invalid.' % code)

# 20170706 Y.D.: Search courts' information
def search_court(keyword):

	keyword_regex = re.compile(keyword)
	courts  = get_all_courts()
	courts  = courts['courts']
	search_results = list(filter(
		lambda court: keyword_regex.search(court['name']), courts))
	
	if len(search_results) > 0:
		return search_results
	else:
		print('Keyword %s is invalid' % (keyword))
		return []

def get_schedules(court_code, story_type, story_year, story_word, story_number):
	'''
	court_code: count's number
	story_type: '民事', '刑事' , '行政' or '公懲'
	story_year: Taiwan's year
	story_word: Type of verdict
	story_number: 判決編號
	'''
	query = _gen_story_query(
		'schedules', 
		court_code=court_code,
		story_type=story_type, story_year=story_year, 
		story_word=story_word, story_number=story_number)

	r = requests.get(query)

	return (r.status_code, r.text)

def get_verdict(court_code, story_type, story_year, story_word, story_number):
	'''
	court_code: count's number
	story_type: '民事', '刑事' , '行政' or '公懲'
	story_year: Taiwan's year
	story_word: Type of verdict
	story_number: 判決編號
	'''
	# status_code, verdict = find_verdict(court_code, story_type, story_year, story_word, story_number)
	query = _gen_story_query(
		'verdict', 
		court_code=court_code,
		story_type=story_type, story_year=story_year, 
		story_word=story_word, story_number=story_number)

	r = requests.get(query)
	status_code = r.status_code
	verdict     = r.text

	if status_code == 200:

		verdict = json.loads(verdict)['verdict']
		content_url = verdict['body']['content_url']
		response = requests.get(content_url)

		if response.status_code == 200:

			verdict_content = json.loads(response.text)

			for key, content in verdict_content.items():
				verdict[key] = content

			available_keys = set({'identity', 'pronounced_on'})

			for key, content in verdict['story'].items():
				if key in available_keys:
					verdict[key] = content

			del verdict['story']

			return (status_code, verdict)
				
		return (status_code, {})

	return (status_code, {})


def get_verdicts_by_time(start_year, start_mon, start_day, end_year, end_mon, end_day, story_type):
	'''
	start_year: 起始西元年
	start_mon : 起始月
	start_day : 起始日
	end_year: 結束西元年
	end_mon : 結束月
	end_day : 結束日
	story_type: '民事', '刑事' , '行政' or '公懲'
	'''
	verdicts = []
	end_time = datetime(year=end_year, month=end_mon, day=end_day)
	end_time = end_time.strftime('%Y-%m-%d')
	start_time = datetime(year=start_year, month=start_mon, day=start_day)
	start_time = start_time.strftime('%Y-%m-%d')

	status, context, pagination = _search(
		adjudged_on_gteq=start_time, adjudged_on_lteq=end_time, story_type=story_type, page=1)

	for page in range(1, pagination+1):

		status, context, pagination = _search(
			adjudged_on_gteq=start_time, adjudged_on_lteq=end_time, story_type=story_type, page=page)

		if status == 200:

			stroies = context['stories']

			for story in stroies:
				
				court_code = story['court']['code']
				story_type = story['identity']['type']
				story_year = story['identity']['year']
				story_word = story['identity']['word']
				story_number = story['identity']['number']
				verdict_status, verdict_context = get_verdict(court_code, story_type, story_year, story_word, story_number)

				if verdict_status == 200:
					verdicts.append(verdict_context)

	return verdicts

def get_rules(court_code, story_type, story_year, story_word, story_number):
	'''
	court_code: count's number
	story_type: '民事', '刑事' , '行政' or '公懲'
	story_year: Taiwan's year
	story_word: Type of verdict
	story_number: 判決編號
	'''
	query = _gen_story_query(
		'rules', 
		court_code=court_code,
		story_type=story_type, story_year=story_year, 
		story_word=story_word, story_number=story_number)

	r = requests.get(query)
	status_code = r.status_code
	rules     = r.text

	if status_code == 200:
		rules = json.loads(rules)['rules']
		return (status_code, rules)
	else:
		err_msg = "The {0}-{1}-{2}-{3}-{4}'s rules cannot be found ".format(
			court_code, story_type, story_year, story_word, story_number)
		print(err_msg)
		return (status_code, [])




