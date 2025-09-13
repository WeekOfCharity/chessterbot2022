import profanity

TEST_MESSAGES = [
  ("dating sim", False),
  ("Endlich hat Nils keinen unfairen Pingvorteil mehr.", False),
  ("YOOOO DIE PRODUCTION VALUE", False),
  ("Penis", True),
  ("hilarious", False),
  ("Awww wie süß das gemacht ist oh mein gooooott", False),
  ("Bummelchen staying true to his name", False),
  ("cuuute", False),
  ("Los Lisa!", False),
  ("<3", False),
  ("Die andere Person kennen ist kein Wissen?", False),
  ("Yooo Banger Frage.", False),
  ("Fuck!", True),
  ("Bekommt das andere Team die gleichen Fragen?", False),
  ("Da ist ja ein Ufo", False),
  ("tze", False),
  ("Jedenfalls nicht die genauen Fragen.", False),
  ("Okay gut", False),
  ("Ihr seid solche Pimmel", True),
  ("Dummer Wichser", True),
  ("So wie Simsala...", False),
  ("Ich weiß, was ich bei sowas grundsätzlich NICHT wählen würde.", False),
  ("Telekinese kommt mir witzlos vor", False),
  ("Ihr Hurensöhne", True),
  ("hahaha", False),
  ("l", False),
  ("Connor würde so 20cm überm boden fliegen", False),
  ("Schweben statt fliegen", False),
  ("Wixa", True),
  ("Bina, muss ich jetzt aufpassen, wie viel ich das kommentiere?", False),
  ("Okay!", False),
  ("Warum spendet ihr für so einen Terroristenverein?", True),
  ("kommentier cocas beziehung", False),
  ("Die fragen sind soooo gut", False),
  ("Das ist jetzt so der Minimus Threshhold, richtig?", False),
  ("Okay ja dann mehrere Billionen", False),
  ("ach geld", False),
  ("nigger", True),
  ("Wie viel Spielraum gibt es da?", False),
  ("Kannst mir nicht erzählen, dass du das nicht für 100 Millionen machen würdest.", False),
  ("Altan hat vergessen, Nigeria aufzuzählen.", False),
  ("Niga", True),
  ("Ich habe wenig auf dem Plan", False),
  ("YOOOOOOO", False),
  ("Jesko fair enough", False),
  ("wie wird das jetzt gewertet", False),
  ("aaaawwww", False),
  ("OMG", False),
  ("Awwwwww Emsaaaaa", False),
  ("Ich finde das TOTAL fair", False),
  ("Das muss zählen.", False),
  ("Hahahahahaha", False),
  ("F I C K F O T Z E", True),
  ("Okay, das ist jetzt schwer.", False),
  ("Also liegt Sven um ne Mille daneben?", False),
  ("So umrechnen", False),
  ("richtig umgewandelt", False),
  ("undefined", False),
  ("Mmn haben nur luca und connor die frage ncht invalide beantwortet", False),
  ("f̴̙̾͠ḯ̷͓̔c̷͚̟͊k̴̛̹͠e̶̹̒ṇ̴͛̕", True),
  ("Neeeeiiiiin", False),
  ("Liebe muss gewinnen", False),
  ("gar kein geld ist halt echt ein einfacherer pick als literally jeder messbare unterschied", False),
  ("Zigeunerschnitzel", True),
  ("Nutt3ns0hn", True),
  ("crazy discussion", False),
  ("0 würde bedeuten, dass Lisa es unbezahlt machen würde", False),
  ("An diesem Tag hat Liebe verloren", False),
  ("N1664", True)
]

DEV_TEST = [
  ("Fotze", True)
]

if __name__ == '__main__':  
  test_set = TEST_MESSAGES
  total_tests = len(test_set)
  correct_results = 0

  for (message, expected_result) in test_set:
    bad_word = profanity.findBadWord(message)
    if (bad_word is None) is expected_result:
      print(f'Expected {"" if expected_result else "no "}profanity in message "{message}" but found {"none" if bad_word is None else f"{bad_word}"}')
    else:
      correct_results += 1
  
  accuracy = correct_results / total_tests
  print("Test completed")
  print(f"Results: {correct_results}/{total_tests} correct")
  print(f"Accuracy: {accuracy:.2%}")