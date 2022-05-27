- <https://www.lojban.org/publications/wordlists/cmavo.txt>
- <https://www.lojban.org/publications/wordlists/gismu.txt>
- <https://www.lojban.org/publications/wordlists/rafsi.txt>
- <https://www.lojban.org/publications/wordlists/lujvo.txt>


- cmene
- fu'ivla
- quote with "zoi" or "la'o"
- "zei" for joining rafsi


Problem: a name can be anything
Ends with a pause (`.`)
The name should end with a consonant.

New algo:
next token, where the break is on a pause or a whitespace

Test is cmene (the last character)

fu'ivla
Stage 1: use a quote
Stage 2: make a cmene
Stage 3: long or short rafsi prefix, with hyphen
Stage 4: drop the prefix

hypen looks like ",r," or ",n,", with rarely ",l".
generally a hypen is a char of "yrnl"


brivla
always end in a vowel
always contain a consonant pair in the first five letters

