import json
import unittest

from main import gen_story_query, find_schedules, find_verdict, get_verdict

class TestSunnyJudgeAPI(unittest.TestCase):

	def test_gen_story_query(self):

		self.assertEqual(
			'https://api.jrf.org.tw/TPH/民事-105-重上-608',
			gen_story_query(
				court_code='TPH', 
				story_type='民事', story_year='105', story_word='重上', story_number='608')
			)

		self.assertEqual(
			'https://api.jrf.org.tw/TPH/民事-105-重上-608/verdict',
			gen_story_query(
				resources_type='verdict',
				court_code='TPH', 
				story_type='民事', story_year='105', story_word='重上', story_number='608')
			)


		self.assertEqual(
			'https://api.jrf.org.tw/TPH/民事-105-重上-608/schedules',
			gen_story_query(
				resources_type='schedules',
				court_code='TPH', 
				story_type='民事', story_year='105', story_word='重上', story_number='608')
			)

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