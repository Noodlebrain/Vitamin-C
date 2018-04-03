import unittest
import re

import cards

class TestCardMethods(unittest.TestCase):

    def test_card_regex(self):
        results_list = re.findall(cards.card_regex,
        'You know, using [Accelerator] with [Accel Hyper] lets you have 4 dice attacking!'.lower().strip())

        self.assertEqual(results_list[0], 'accelerator')
        self.assertEqual(results_list[1], 'accel hyper')

    def test_trigger_true(self):
        content = '[QP] is a very balanced character.'
        self.assertTrue(cards.trigger(content))

    def test_trigger_false(self):
        content = 'Hello world!'
        self.assertFalse(cards.trigger(content))

    def test_hyper_regex(self):
        match = re.search(cards.card_regex, '[kai.hyper]')
        self.assertEqual(match.groups()[0].strip(), 'kai.hyper')
        match2 = re.search(cards.hyper_regex, match.groups()[0].strip())
        self.assertEqual(match2.groups()[0].strip(), 'kai')

if __name__ == '__main__':
    unittest.main()
