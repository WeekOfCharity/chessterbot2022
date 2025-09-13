import re

SUBSTITUTIONS = [
  ("@", "a"),
  ("Д", "a"),
  ("4", "a"),
  ("ä", "a"),
  ("а", "a"),
  ("8", "b"),
  ("в", "b"),
  ("ь", "b"),
  ("©", "c"),
  ("с", "c"),
  ("¢", "c"),
  ("3", "e"),
  ("£", "e"),
  ("₤", "e"),
  ("€", "e"),
  ("е", "e"),
  ("ƒ", "f"),
  ("6", "g"),
  ("9", "g"),
  ("н", "h"),
  ("1", "i"),
  ("|", "i"),
  ("!", "i"),
  ("м", "m"),
  ("И", "n"),
  ("и", "n"),
  ("п", "n"),
  ("0", "o"),
  ("ö", "o"),
  ("Ø", "o"),
  ("Θ", "o"),
  ("о", "o"),
  ("ө", "o"),
  ("р", "p"),
  ("₱", "p"),
  ("Я", "r"),
  ("®", "r"),
  ("5", "s"),
  ("ß", "s"),
  ("$", "s"),
  ("§", "s"),
  ("7", "t"),
  ("т", "t"),
  ("†", "t"),
  ("ü", "u"),
  ("μ", "u"),
  ("√", "v"),
  ("Ш", "w"),
  ("×", "x"),
  ("Ж", "x"),
  ("¥", "y"),
  ("Ч", "y"),
  ("ү", "y"),
  ("у", "y"),
  ("2", "z")
]

substitution_from = ''.join([substitution[0] for substitution in SUBSTITUTIONS])
substitution_to = ''.join([substitution[1] for substitution in SUBSTITUTIONS])
substitution_table = str.maketrans(substitution_from, substitution_to)

BAD_WORDS = []
BLACKLIST_EXACT_WORDS = []

with open('bad_words.txt') as f:
  for line in f: BAD_WORDS.append(line.rstrip("\n"))

with open('blacklist_exact.txt') as f:
  for line in f: BLACKLIST_EXACT_WORDS.append(line.rstrip("\n"))

def findBadWord(message: str):
  lower_message = message.lower()
  substituted_message = lower_message.translate(substitution_table)
  cleaned_message = re.sub(r'[^a-z]', '', substituted_message)

  for word in BAD_WORDS:
    if word in cleaned_message:
      return word
  
  stripped_message = substituted_message.strip()

  for word in BLACKLIST_EXACT_WORDS:
    if stripped_message.startswith(word) or stripped_message.endswith(word) or f" {word} " in stripped_message:
      return word
    
  return None