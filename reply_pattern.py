#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

class ReplyPattern():
    def __init__(self, filename='data/pattern.json'):
        self.filename = filename
        with open(filename) as f:
            self.pattern = json.load(f)

    def add_pattern(self, match, reply_text):
        
        self.pattern[match] = {
            'reply_text': reply_text
        }

    def get_reply_messages(self, message_text):
        match_value_list = []
        for match_pattern, value in self.pattern.items():
            if is_match(match_pattern):
                match_value_list.append(value)

        return match_value_list

    def get_pattern(self):
        return self.pattern

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.pattern, indent=2, ensure_ascii=False))
        
    @staticmethod
    def is_match(match_pattern, text):
        return match_pattern in text
