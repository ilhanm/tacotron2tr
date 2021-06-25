""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from .numbers import normalize_numbers
from .numbers import normalize_numbers_tr


# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

def turkish_letter_changer(text):
  text = text.replace("ı", "w")
  text = text.replace("I", "w")
  text = text.replace("ü", "q")
  text = text.replace("Ü", "q")
  text = text.replace("ş", "x")
  text = text.replace("Ş", "x")
  text = text.replace("ç", "j")
  text = text.replace("Ç", "j")
  return text

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('vb', 'vebenzeri'),
  ('vs', 'vesaire'),
  ('dr', 'doktor'),
  ('av', 'avukat'),
  ('MÖ', 'milattan önce'),# okunmuyo
  ('MS', 'milattan sonra'),
  ('TBMM', 'Türkiye Büyük Millet Meclisi'),
  ('TDK', 'Türk Dil Kurumu'),
  ('TC', 'Türkiye Cumhuriyeti'),
  ('mm', 'milimetre'),
  ('kg', 'kilogram'),
  ('km', 'kilometre'),
  ('mg', 'miligram'),
  ('Prof', 'Profesör'),
  ('haz', 'hazırlayan'),
  ('çev', 'çeviren'),# okunmuyo
  ('Alb', 'Albay'),
  ('Müh', 'Mühendis'),# okunmuyo
  ('no', 'Numara'),
  ('Opr', 'Operatör'),
  ('Org', 'Orgeneral'),
  ('Uzm', 'Uzman'),
  ('Yrd', 'Yardımcı'),
  ('Doç', 'Doçent'),# okunmuyo
  ('Yzb', 'Yüzbaşı'),
  ('mah', 'Mahallesi'),
  ('cad', 'Caddesi'),
  ('sok', 'Sokak'),
  ('Apt', 'Apartman'),
  ('Ecz', 'Eczane'),
  ('THY', 'Türk Hava Yolları'),
  ('MEB', 'Milli Eğitim Bakanlığı'),
  ('bkz', 'bakınız'),
  ('bul', 'Bulvarı'),
  ('gön', 'gönderen'),# okunmuyo
  ('lt', 'litre'),
  ('yy', 'yüzyıl'),
]]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text

def expand_numbers(text):
  return normalize_numbers(text)

def expand_numbers_tr(text):
  return normalize_numbers_tr(text)


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)

def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def english_cleaners(text):
  '''Pipeline for English text, including number and abbreviation expansion.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  return text

def turkish_cleaners(text):
  text = expand_numbers_tr(text)
  text = expand_abbreviations(text)
  text = turkish_letter_changer(text)
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text