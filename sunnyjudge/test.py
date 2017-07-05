import json
import unittest
import urllib

from main import _gen_story_query, _gen_search_query, _search
from main import get_verdict, get_verdicts_by_time, get_schedules
from main import get_court, get_all_courts

class TestSunnyJudgeAPI(unittest.TestCase):

	def test_gen_story_query(self):

		self.assertEqual(
			'https://api.jrf.org.tw/TPH/民事-105-重上-608',
			_gen_story_query(
				court_code='TPH', 
				story_type='民事', story_year='105', story_word='重上', story_number='608')
			)

		self.assertEqual(
			'https://api.jrf.org.tw/TPH/民事-105-重上-608/verdict',
			_gen_story_query(
				resources_type='verdict',
				court_code='TPH', 
				story_type='民事', story_year='105', story_word='重上', story_number='608')
			)


		self.assertEqual(
			'https://api.jrf.org.tw/TPH/民事-105-重上-608/schedules',
			_gen_story_query(
				resources_type='schedules',
				court_code='TPH', 
				story_type='民事', story_year='105', story_word='重上', story_number='608')
			)

	def test_gen_search_query(self):

		goal_search_query = {
			'page': ['1'],
 			'q[adjudged_on_gteq]': ['2009-12-01'],
 			'q[adjudged_on_lteq]': ['2017-04-20'],
 			'q[judges_names_cont]': ['張靜'],
 			'q[lawyer_names_cont]': ['謝'],
 			'q[number]': ['608'],
 			'q[story_type]': ['民事'],
 			'q[word]': ['重上'],
 			'q[year]': ['105']
 		}

		gen_search_query = _gen_search_query(
			page=1, story_type='民事', word='重上', number=608, year=105, 
			judges_names_cont='張靜', lawyer_names_cont='謝', 
			adjudged_on_gteq='2009-12-01', adjudged_on_lteq='2017-04-20')

		gen_search_query = urllib.parse.parse_qs(gen_search_query)

		self.assertEqual(goal_search_query, gen_search_query)


	def test_get_schedules(self):

		(response_status, response_text) = get_schedules('TPH', '民事', '105', '重上', '608')
		self.assertEqual(200, response_status)

		content_200 = json.loads(response_text)
		self.assertEqual(type(content_200['schedules']), type([]))

		(response_status, response_text) = get_schedules('TPH', '民事', '105', '重上', '6008')
		content_404 = json.loads(response_text)

		self.assertEqual(404, response_status)
		self.assertEqual(content_404['message'], '案件不存在')

	def test_search(self):

		search_query = {
			'page': '1',
 			'q[adjudged_on_gteq]': '2009-12-01',
 			'q[adjudged_on_lteq]': '2017-04-20',
 			'q[judges_names_cont]': '張靜',
 			'q[lawyer_names_cont]': '謝',
 			'q[number]': '608',
 			'q[story_type]': '民事',
 			'q[word]': '重上',
 			'q[year]': '105'
 		}

		status, context, pagination = _search(
			page=1, adjudged_on_gteq='2009-12-01', adjudged_on_lteq='2017-04-20', 
			judges_names_cont='張靜', lawyer_names_cont='謝', 
			number=608, story_type='民事', word='重上', year=105)

		self.assertEqual(200, status)
		self.assertEqual(type(context), type({}))
		self.assertGreaterEqual(pagination, 1)

		status, context, pagination = _search(
			page=1, adjudged_on_gteq='2009-12-01', adjudged_on_lteq='2017-04-20', 
			judges_names_cont='張靜', lawyer_names_cont='謝', 
			number=608, story_type='民事', word='重上', year=1005)

		self.assertEqual(200, status)
		self.assertEqual(type(context), type({}))
		self.assertEqual(pagination, 0)

	# def test_find_verdict(self):

	# 	(response_status, response_text) = find_verdict('TPH', '民事', '105', '重上', '608')
	# 	self.assertEqual(200, response_status)

	# 	content_200 = json.loads(response_text)
	# 	self.assertEqual(type(content_200['verdict']), type({}))

	# 	(response_status, response_text) = find_verdict('TPH', '民事', '105', '重上', '6008')
	# 	content_404 = json.loads(response_text)

	# 	self.assertEqual(404, response_status)
	# 	self.assertEqual(content_404['message'], '案件不存在')

	def test_get_verdict(self):

		test_cases = [
			('TPH', '民事', '105', '重上', '608'),
			('KSB', '行政', '104', '訴'  , '157')]

		for test_case in test_cases:

			(response_status, verdict_content) = \
				get_verdict(test_case[0], test_case[1], test_case[2], test_case[3], test_case[4])
			self.assertEqual(200, response_status)

			target_keys = set({
				'identity', 'reason', 'adjudged_on', 'pronounced_on', 'court', 
				'judges_names', 'related_roles', 'lawyer_names', 'prosecutor_names', 
				'party_names', 'original_url', 'body', 'main_content'})

			verdict_keys = set({})

			for key in verdict_content.keys():
				verdict_keys.add(key)

			exist_all_keys = True

			if not target_keys == verdict_keys:
				exist_all_keys = False
				lack_keys = target_keys.difference(verdict_keys)
				print('The verdict lack %s keys' % lack_keys)

			self.assertTrue(exist_all_keys)

	def test_get_verdicts_by_time(self):

		response_status, verdict_content, verdict_pagination = _search(
			adjudged_on_gteq='2017-01-02', adjudged_on_lteq='2017-01-02', story_type='民事', page=1)

		verdict_number = verdict_content['pagination']['count']
		query_verdicts = get_verdicts_by_time(2017, 1, 2, 2017, 1, 2, '民事')

		self.assertEqual(len(query_verdicts), verdict_number)

	# 20170704 Y.D.: Test courts
	def test_get_all_courts_code(self):

		courts = get_all_courts()
		courts_number = len(courts['courts'])
		print('The number of courts are: %d' % courts_number)
		if courts_number > 23:
			self.assertTrue(True)
		else:
			self.assertTrue(False)

	# 20170704 Y.D.: Test court code to search
	def test_get_court_code(self):
		# Supreme court's code as the test case
		court_code = 'TPS'
		court_meta = get_court(court_code)
		if court_meta:
			self.assertEqual(court_meta['court']['name'], '最高法院')
		else:
			self.assertTrue(False)
		# Supreme court's incorrect code as the test case
		court_code = 'TPX'
		court_meta = get_court(court_code)
		if court_meta:
			self.assertEqual(court_meta['court']['name'], '最高法院')
		else:
			self.assertTrue(True)



if __name__ == '__main__':
	unittest.main()