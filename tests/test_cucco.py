# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import os
import sys

# Add sources to path
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH + '/../')

from cucco import Cucco

with open('tests/test_cases.json', 'r') as data:
    TESTS_DATA = json.load(data)

class TestCucco:

    _cucco = None

    @staticmethod
    def _tests_generator(test):
        for test in TESTS_DATA['tests'][test[5:]]:
            yield (test['after'],
                   test['before'],
                   test['characters'] if 'characters' in test else '',
                   test['kwargs'] if 'kwargs' in test else dict(),
                   test['message'])

    def setup_method(self):
        self._cucco = Cucco()

    def test_normalize(self, request):
        for after, before, _, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.normalize(before, **kwargs) == after, message

    def test_remove_accent_marks(self, request):
        for after, before, _, _, message in self._tests_generator(request.node.name):
            assert self._cucco.remove_accent_marks(before) == after, message

    def test_remove_stop_words(self, request):
        for after, before, _, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.remove_stop_words(before, **kwargs) == after, message

        # Test lazy load
        self._cucco = Cucco(lazy_load=True)
        for after, before, _, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.remove_stop_words(before, **kwargs) == after, message

    def test_replace_characters(self, request):
        for after, before, characters, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.replace_characters(text=before, characters=characters, **kwargs) == after, message

    def test_replace_emails(self, request):
        for after, before, _, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.replace_emails(text=before, **kwargs) == after, message

    def test_replace_emojis(self, request):
        for after, before, _, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.replace_emojis(text=before, **kwargs) == after, message

    def test_remove_extra_whitespaces(self, request):
        for after, before, _, _, message in self._tests_generator(request.node.name):
            assert self._cucco.remove_extra_whitespaces(before) == after, message

    def test_replace_hyphens(self, request):
        for after, before, _,  kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.replace_hyphens(text=before, **kwargs) == after, message

    def test_replace_punctuation(self, request):
        for after, before, _, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.replace_punctuation(text=before, **kwargs) == after, message

    def test_replace_symbols(self, request):
        for after, before, _, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.replace_symbols(text=before, **kwargs) == after, message

    def test_replace_urls(self, request):
        for after, before, _, kwargs, message in self._tests_generator(request.node.name):
            assert self._cucco.replace_urls(text=before, **kwargs) == after, message
