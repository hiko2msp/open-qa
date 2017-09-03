import json
import unittest
from reply_pattern import ReplyPatternGspread

SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT', 'dummy service account')

class TestReplyPatternGspread(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        rp = ReplyPatternGspread(json.loads(SERVICE_ACCOUNT))
        self.assertEqual(
            rp.get_reply_messages('おはよう')[0]['reply_text'],
            'おはよう'
        )

    def test_save(self):
        rp = ReplyPatternGspread(json.loads(SERVICE_ACCOUNT))
        initial_length = rp.row_length

        rp.add_pattern('ABC', 'ABC')
        rp.save()
        self.assertEqual(rp.row_length, initial_length + 1)

        rp.delete_pattern('ABC')
        rp.save()

        self.assertEqual(rp.row_length, initial_length)

if __name__ == '__main__':
    unittest.main()
