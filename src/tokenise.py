#!/usr/bin/python3
from polyglot.text import Text
import os
import re
import sys

language = sys.argv[1]
type = sys.argv[2]

handle = open(type, encoding="UTF-8")
input_string = handle.read()
handle.close()

re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
filtered_string = re_pattern.sub(u'\uFFFD', input_string)

text = Text(filtered_string, hint_language_code=language)
print(language, text.language)
tokenised = text.words

outlanguage = open(language + type, "w", encoding="UTF-8")
outlanguage.write(" ".join(tokenised))
outlanguage.close()
