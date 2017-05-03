import json
import unittest
import urllib

from main import _gen_story_query, _gen_search_query, find_schedules, find_verdict, get_verdict

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

		search_query = {
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
		gen_search_query = _gen_search_query(page=1, story_type='民事', word='重上', number=608, year=105, judges_names_cont='張靜', lawyer_names_cont='謝', adjudged_on_gteq='2009-12-01', adjudged_on_lteq='2017-04-20')
		gen_search_query = urllib.parse.parse_qs(gen_search_query)
		self.assertEqual(search_query, gen_search_query)


	def test_find_schedules(self):

		(response_status, response_text) = find_schedules('TPH', '民事', '105', '重上', '608')
		self.assertEqual(200, response_status)

		content = json.loads(response_text)
		self.assertEqual(type(content['schedules']), type([]))

	def test_find_verdict(self):

		(response_status, response_text) = find_verdict('TPH', '民事', '105', '重上', '608')
		self.assertEqual(200, response_status)

		content = json.loads(response_text)
		self.assertEqual(type(content['verdict']), type({}))

		# TODO: Test 404
		

	def test_get_verdict(self):

		(response_status, verdict_content) = get_verdict('TPH', '民事', '105', '重上', '608')

		self.assertEqual(200, response_status)

		target_keys = set({
			'identity', 'reason', 'adjudged_on', 'pronounced_on', 'court', 
			'judges_names', 'related_roles', 'lawyer_names', 'prosecutor_names', 
			'party_names', 'related_stories', 'original_url', 'body', 'main_content'})

		verdict_keys = set({})

		for key in verdict_content.keys():
			verdict_keys.add(key)

		exist_all_keys = True

		if not target_keys == verdict_keys:
			exist_all_keys = False
			lack_keys = target_keys.difference(verdict_keys)
			print('The verdict lack %s keys' % lack_keys)


		self.assertTrue(exist_all_keys)


if __name__ == '__main__':
	unittest.main()