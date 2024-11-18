def parse_multiline(string: str) -> str:
  """
  Function that allows the user to input line breaks.

  string -- The input string.
  """
  ESC_CHAR = '\\'
  escapable = {
    ESC_CHAR: None,
    'n': '\n'
  }

  out_string = ''

  escaped = False
  for char in string:
    if not escaped and char == ESC_CHAR:
      escaped = True
      continue

    if (escaped):
      if (char in escapable):
        escaped_char = escapable[char]
        if (escaped_char is not None):
          char = escaped_char
      else:
        out_string += ESC_CHAR

    escaped = False
    out_string += char

  return out_string


def colorize_number(number, remove_negative = False):
    if float(number) < 0: # negative (red)
        return f'[0m{"-" if not remove_negative else ""}[31m{number[1:]}'
    else: # positive (green)
        return f'[32m{number}'