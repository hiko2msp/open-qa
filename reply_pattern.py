#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import OrderedDict


class ReplyPattern():
    def __init__(self, filename='data/pattern.json'):
        self.filename = filename
        with open(filename) as f:
            self.pattern = json.load(f)

    def add_pattern(self, match, reply_text):
        self.pattern[match] = {
            'reply_text': reply_text
        }

    def delete_pattern(self, match):
        if self.pattern.get(match):
            del self.pattern[match]

    def get_reply_messages(self, message_text):
        match_value_list = []
        for match_pattern, value in self.pattern.items():
            if ReplyPattern.is_match(match_pattern, message_text):
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


def get_credentials(file_buffer):
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
    ]
    credentials = ServiceAccountCredentials.from_p12_keyfile_buffer(
            service_account_email='slackbot@our-lacing-579.iam.gserviceaccount.com',
            file_buffer=file_buffer,
            private_key_password='notasecret',
            scopes=scopes,
    )
    return credentials


class ReplyPatternGspread():
    def __init__(self, credential_dict):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            credential_dict,
            scopes=scopes
        )

        gc = gspread.authorize(credentials)
        gc.open_by_key('1z6n0eq-Y7Wcss7zQs_KglODJ7RSBTTzvT4uqf8FjqBo')
        sh = gc.open('ボットの会話')
        self.ws = sh.worksheets()[0]
        self.load()

    @staticmethod
    def create_reply_pattern_from_worksheet(ws):
        match_pattern_list = [acell.value for acell in ws.range('A2:A100') if acell.value]
        reply_text_list = [acell.value for acell in ws.range('B2:B100') if acell.value]
        pattern = OrderedDict()
        for match, reply_text in zip(match_pattern_list, reply_text_list):
            pattern[match] = {
                'reply_text': reply_text
            }

        return pattern

    def add_pattern(self, match, reply_text):
        self.pattern[match] = {
            'reply_text': reply_text
        }

    def delete_pattern(self, match):
        if self.pattern.get(match):
            del self.pattern[match]

    def get_reply_messages(self, message_text):
        reply_obj_list = []
        for match_pattern, reply_obj in self.pattern.items():
            if ReplyPatternGspread.is_match(match_pattern, message_text):
                reply_obj_list.append(reply_obj)

        return reply_obj_list

    def get_pattern(self):
        return self.pattern

    def load(self):
        self.pattern = ReplyPatternGspread.create_reply_pattern_from_worksheet(self.ws)
        self.row_length = max(
            len([acell.value for acell in self.ws.range('A2:A100') if acell.value]),
            len([acell.value for acell in self.ws.range('B2:B100') if acell.value])
        )

    def save(self):
        new_row_length = max(self.row_length, self.get_pattern_len())
        pattern_cell_list = self.ws.range('A2:A{}'.format(new_row_length + 1))
        reply_text_cell_list = self.ws.range('B2:B{}'.format(new_row_length + 1))

        for cell in pattern_cell_list:
            cell.value = ''
        for cell in reply_text_cell_list:
            cell.value = ''

        for i, (match_pattern, reply_obj) in enumerate(self.pattern.items()):
            pattern_cell_list[i].value = match_pattern
            reply_text_cell_list[i].value = reply_obj['reply_text']

        self.ws.update_cells(pattern_cell_list)
        self.ws.update_cells(reply_text_cell_list)

        self.pattern = ReplyPatternGspread.create_reply_pattern_from_worksheet(self.ws)
        self.row_length = max(
            len([acell.value for acell in self.ws.range('A2:A100') if acell.value]),
            len([acell.value for acell in self.ws.range('B2:B100') if acell.value])
        )

    def get_pattern_len(self):
        return len(self.pattern.keys())

    @staticmethod
    def is_match(match_pattern, text):
        return match_pattern in text
