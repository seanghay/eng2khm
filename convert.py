import csv
import re

RE_DIGIT = re.compile(r"\d+")

M_VOWELS = {
  "AA": "",
  "AE": "ែ",
  "AH": "ា",
  "AO": "ោ",
  "AW": "ៅ",  # Fixed from ោ to ៅ
  "AY": "ៃ",
  "EH": "េ",
  "ER": "ើ",
  "EY": "េ",
  "IH": "ិ",  # Fixed from ៊ី to ិ
  "IY": "ី",  # Fixed from ៊ី to ី
  "OW": "ូ",
  "OY": "យ",
  "UH": "ុ",  # Fixed from ៊ូ to ុ
  "UW": "ូ",
}

M_CONSONANTS = {
  "B": "ប",
  "CH": "ឆ",
  "D": "ដ",
  "DH": "ដ",
  "F": "ហ្វ",
  "G": "គ",
  "HH": "ហ",
  "JH": "ជ",
  "K": "ក",
  "L": "ល",
  "M": "ម",
  "N": "ន",
  "NG": "ង",
  "P": "ប",
  "R": "រ",
  "S": "ស",
  "SH": "ស",
  "T": "ត",
  "TH": "ត",
  "V": "វ",
  "W": "វ",
  "Y": "យ",
  "Z": "ស",
  "ZH": "ស",
}

# Add initial vowels (when vowel appears at start of word)
M_INITIAL_VOWELS = {
  "AA": "អា",
  "AE": "អែ",
  "AH": "អា",
  "AO": "អោ",
  "AW": "អៅ",
  "AY": "អៃ",
  "EH": "អេ",
  "ER": "អើ",
  "EY": "អេ",
  "IH": "អិ",
  "IY": "អី",
  "OW": "អូ",
  "OY": "អយ",
  "UH": "អុ",
  "UW": "អូ",
}


def transliterate(phonemes):
  phonemes = [RE_DIGIT.sub("", p) for p in phonemes]

  result = []
  pos = 0

  if phonemes[0] in M_INITIAL_VOWELS:
    result.append(M_INITIAL_VOWELS[phonemes[0]])
    pos = 1

  while pos < len(phonemes):
    current = phonemes[pos]

    if pos < len(phonemes) - 1 and current == "IH" and phonemes[pos + 1] == "R":
      result.append("ៀ")
      pos += 2
      continue

    if current in M_CONSONANTS:
      result.append(M_CONSONANTS[current])

      if (
        pos < len(phonemes) - 1
        and phonemes[pos + 1] in M_CONSONANTS
        and phonemes[pos + 1] not in ["Y", "W"]
      ):
        result.append("្")

    elif current in M_VOWELS:
      if M_VOWELS[current]:
        result.append(M_VOWELS[current])
    pos += 1

  if len(phonemes) >= 2 and phonemes[-2] == "AH":
    if result[-1] in "កងចញតនបមយរលវស":
      result.append("់")

  return "".join(result)


def main():
  with open("result.tsv", "w", encoding="utf-8") as outfile:
    writer = csv.writer(outfile, delimiter="\t")
    with open("cmudict.dict", encoding="utf-8") as infile:
      for line in infile:
        line = line.rstrip("\n")

        values = re.sub(r"#.+", "", line).split()
        if not values:
          continue

        word = re.sub(r"\(.*?\)", "", values[0])
        phonemes = values[1:]
        khmer = transliterate(phonemes)
        writer.writerow([word, " ".join(phonemes), khmer])


if __name__ == "__main__":
  main()
