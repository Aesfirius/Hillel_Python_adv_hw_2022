"""
helper scripts :)
"""

from translate import Translator


def translate_to(origin_text, from_lang, to_lang):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translation = translator.translate(origin_text)
    return translation
