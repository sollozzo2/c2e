# c2e
This program aims to help English speakers pronounce Chinese words as accurately as possible without having to learn new sounds.
Pinyin, the romanization of Chinese characters, doesn't do the best job at representing accurate pronunciations of Chinese words.
For example, native English speakers, seeing that there is an "a" in "Jiang" (tɕi̯ɑŋ), will often pronounce it with æ, as in "at". Other systems of romanization, such as Wade-Giles (chiang), are also susceptible to this ambiguity.
![alt text](https://upload.wikimedia.org/wikipedia/en/5/5a/IPA_vowel_chart_2005.png)
However, the chart above shows that there is considerable difference between æ and ɑ, the actual vowel in jiang.
In terms of front-ness, æ is pronounced at the front of the mouth, while ɑ is pronounced at the back.
A closer equivalent would instead be ʌ - while not as open as ɑ, it is a closer alternative.
The program will therefore produce "jee-ung" with "jiang" as an input, giving a more accurate and comprehensible representation.
Another example is the letter 'x' in pinyin. English speakers will often pronounce it as 'z' - not very close to ɕ, its actual pronunciation.

How It Works
Input: Pinyin representation of a Chinese character
Step 1. Convert pinyin into ipa with a hashtable, e.g. meng	-> məŋ(it turns out pinyin doesn't accurately represent pronunciation in Chinese either, and there are only 400 Chinese pronunciations disregarding tone, so a dictionary will do.)
Step 2. Convert ipa into phonetic symbols used by cmudict, e.g. məŋ -> MAHNG (https://www.nltk.org/_modules/nltk/corpus/reader/cmudict.html)
Step 3. Go through the English vocabulary and find the English word whose pronunciation(s) best match that of the Chinese word, e.g. MAHNG -> mong
Sometimes a Chinese character has to be split into two English words for the most accurate results, as the program did with "jiang" (jee-ung).
Some interesting findings:
"bo" (pu̯ɔ) -> bois (technically French, but gets the job done. I wouldn't have made that connection.)

