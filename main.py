import json
import requests

from urllib import parse

SUNNY_JUDGE_API = 'https://api.jrf.org.tw'


def _gen_story_query(resources_type='', **kwargs):

	court_code = None
	story_type, story_year, story_word, story_number = None, None, None, None

	for key, value in kwargs.items():

		if key == 'court_code':
			court_code = value
		elif key == 'story_type':
			story_type = value
		elif key == 'story_year':
			story_year = value
		elif key == 'story_word':
			story_word = value
		elif key == 'story_number':
			story_number = value

	story_query = '-'.join([story_type, story_year, story_word, story_number])

	if len(resources_type) > 0:
		query = '/'.join([SUNNY_JUDGE_API, court_code, story_query, resources_type])
	else:
		query = '/'.join([SUNNY_JUDGE_API, court_code, story_query])
	
	return query


def gen_search_query(**kwargs):

	query = {
		'[adjudged_on_gteq]': '',
		'[adjudged_on_lteq]': '',
		'[judges_names_cont]': '',
		'[lawyer_names_cont]': '',
		'[number]': '',
		'[story_type]': '',
		'[word]': '',
		'[year] ': ''
	}

	

def find_schedules(court_code, story_type, story_year, story_word, story_number):

	query = _gen_story_query(
		'schedules', 
		court_code=court_code,
		story_type=story_type, story_year=story_year, 
		story_word=story_word, story_number=story_number)

	r = requests.get(query)

	return (r.status_code, r.text)

def find_verdict(court_code, story_type, story_year, story_word, story_number):

	query = _gen_story_query(
		'verdict', 
		court_code=court_code,
		story_type=story_type, story_year=story_year, 
		story_word=story_word, story_number=story_number)

	r = requests.get(query)

	return (r.status_code, r.text)


def get_verdict(court_code, story_type, story_year, story_word, story_number):

	status_code, verdict = find_verdict(court_code, story_type, story_year, story_word, story_number)

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
				
		return (status_code. result)

	return (status_code. result)


def get_verdicts_by_time(start_year, start_mon, start_day, end_year, end_mon, end_day):


