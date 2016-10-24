#!/usr/bin/env python
from __future__ import print_function
from collections import Counter
import os
import sys
import argparse


def anagram(input_word, word_list):
	lettercount = Counter(input_word)
	anagrams = []

	def anagram_recurse(lettercount, word_list, possible_anagram, anagrams, call_count):
		# number of letters
		wordlength = sum(lettercount.values())
		for aword in word_list:
			if len(aword) > wordlength:
				continue
			acount = word_list[aword]

			if len(acount - lettercount) == 0:
				# then every letter in aword is in input_word
				# take them out of input_word's count
				lettercount_copy = Counter(lettercount.elements())
				lettercount_copy.subtract(acount)

				count_values = sum(lettercount_copy.values())
				if count_values == 0:
					# no letters left, this is a full anagram
					one_possible = possible_anagram + " " + aword
					anagrams.append(one_possible.strip())
				elif count_values > 0:
					# if aword was in input_word and there are still letters left, check whether more words can be taken out
					call_count = anagram_recurse(lettercount_copy, word_list, possible_anagram + " " + aword, anagrams, call_count)
		call_count += 1
		if call_count % 10 == 0:
			sys.stdout.write('.')
			sys.stdout.flush()
		return call_count

	callcount = anagram_recurse(lettercount, word_list, '', anagrams, 0)
	print("Called " + str(callcount) + " times.")
	return anagrams




if __name__ == "__main__":
	description = "Typhon: Anagram Generator in Python"
	print(description)
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-w', '--word', type=str, required=True, help='Outbound call gateway')
	parser.add_argument('-s', '--small', action='store_true', help='Use small word list')

	args = parser.parse_args()
	inword = args.word.lower().replace(' ', '')

	words = {}
	filename = 'words.txt'
	if args.small:
		filename = 'small-words.txt'
	with open(filename) as f:
		for line in f:
			key = line.strip()
			words[key] = Counter(key)
	# print(words)
	print("Words file ready. Generating anagrams.")

	anagrams = anagram(inword, words)
	print(anagrams)
