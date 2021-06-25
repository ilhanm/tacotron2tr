""" from https://github.com/keithito/tacotron """
import inflect
import re
import num2words


_inflect = inflect.engine()
_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
_pounds_re = re.compile(r'£([0-9\,]*[0-9]+)')
_dollars_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_liras_re = re.compile(r'\₺([0-9\.\,]*[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(st|nd|rd|th)')
_ordinal_re_tr = re.compile(r'[0-9]+(ıncı|inci|nci|üncü|uncu)')
_number_re = re.compile(r'[0-9]+')


def _remove_commas(m):
  return m.group(1).replace(',', '')


def _expand_decimal_point(m):
  return m.group(1).replace('.', ' point ')

def _expand_decimal_point_tr(m):
  return m.group(1).replace('.', ' nokta ')


def _expand_dollars(m):
  match = m.group(1)
  parts = match.split('.')
  if len(parts) > 2:
    return match + ' dolar'  # Unexpected format
  dollars = int(parts[0]) if parts[0] else 0
  cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
  if dollars and cents:
    dollar_unit = 'dolar' if dollars == 1 else 'dolar'
    cent_unit = 'sent' if cents == 1 else 'sent'
    return '%s %s, %s %s' % (dollars, dollar_unit, cents, cent_unit)
  elif dollars:
    dollar_unit = 'dolar' if dollars == 1 else 'dolar'
    return '%s %s' % (dollars, dollar_unit)
  elif cents:
    cent_unit = 'sent' if cents == 1 else 'sent'
    return '%s %s' % (cents, cent_unit)
  else:
    return 'sıfır dolar'

def _expand_lira(m):
  match = m.group(1)
  parts = match.split('.')
  if len(parts) > 2:
    return match + ' lira'  # Unexpected format
  liras = int(parts[0]) if parts[0] else 0
  kurus = int(parts[1]) if len(parts) > 1 and parts[1] else 0
  if liras and kurus:
    liras_unit = 'lira' if liras == 1 else 'lira'
    kurus_unit = 'kuruş' if kurus == 1 else 'kuruş'
    return '%s %s, %s %s' % (liras, liras_unit, kurus, kurus_unit)
  elif liras:
    liras_unit = 'lira' if liras == 1 else 'lira'
    return '%s %s' % (liras, liras_unit)
  elif kurus:
    kurus_unit = 'kuruş' if kurus == 1 else 'kuruş'
    return '%s %s' % (kurus, kurus_unit)
  else:
    return 'sıfır lira'


def _expand_ordinal(m):
  return _inflect.number_to_words(m.group(0))

def _expand_ordinal_tr(m):
  return num2words.num2words(m, lang="tr", to="ordinal")


def _expand_number(m):
  num = int(m.group(0))
  if num > 1000 and num < 3000:
    if num == 2000:
      return 'two thousand'
    elif num > 2000 and num < 2010:
      return 'two thousand ' + _inflect.number_to_words(num % 100)
    elif num % 100 == 0:
      return _inflect.number_to_words(num // 100) + ' hundred'
    else:
      return _inflect.number_to_words(num, andword='', zero='oh', group=2).replace(', ', ' ')
  else:
    return _inflect.number_to_words(num, andword='')


def expand_numbers_tr(m):
  num = int(m.group(0))
  if num != 0:
    return num2words.num2words(num, lang='tr')
  else:
    return 'sıfır'


def normalize_numbers(text):
  text = re.sub(_comma_number_re, _remove_commas, text)
  text = re.sub(_pounds_re, r'\1 pounds', text)
  text = re.sub(_dollars_re, _expand_dollars, text)
  text = re.sub(_decimal_number_re, _expand_decimal_point, text)
  text = re.sub(_ordinal_re, _expand_ordinal, text)
  text = re.sub(_number_re, _expand_number, text)
  return text

def normalize_numbers_tr(text):
  text = re.sub(_comma_number_re, _remove_commas, text)
  text = re.sub(_pounds_re, r'\1 sterlin', text)
  text = re.sub(_dollars_re, _expand_dollars, text)
  text = re.sub(_liras_re, _expand_lira, text)
  text = re.sub(_decimal_number_re, _expand_decimal_point_tr, text)
  text = re.sub(_ordinal_re_tr, _expand_ordinal_tr, text)
  text = re.sub(_number_re, expand_numbers_tr, text)
  return text

