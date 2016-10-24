#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse

def anagram(input_word, word_list):
	anagrams = []

	def anagram_recurse(input_word, word_list, possible_anagram, anagrams, count):
		for aword in word_list:
			if len(aword) > len(input_word):
				continue
			iw = input_word
			match = True
			for l in aword:
				c = iw.find(l)
				if c > -1:
					iw = iw[:c] + iw[c+1:]
				else:
					match = False
			if len(iw) < 1:
				# no letters left, this is a full anagram
				one_possible = possible_anagram + " " + aword
				anagrams.append(one_possible.strip())
			else:
				# if aword was in input_word, check whether more words can be taken out
				if match:
					# print(possible_anagarm + " " + aword + ": " + iw)
					count = anagram_recurse(iw, word_list, possible_anagram + " " + aword, anagrams, count)
		count += 1
		if count % 100 == 0:
			sys.stdout.write('.')
			sys.stdout.flush()
		return count

	callcount = anagram_recurse(input_word, word_list, '', anagrams, 0)
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

	words = set()
	filename = 'words.txt'
	if args.small:
		filename = 'small-words.txt'
	with open(filename) as f:
		for line in f:
			words.add(line.strip())
	# print(words)
	print("Words file ready. Generating anagrams.")

	anagrams = anagram(inword, words)
	print(anagrams)
