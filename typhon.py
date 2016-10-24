#!/usr/bin/env python
from __future__ import print_function
from collections import Counter
import os
import sys
import argparse


def anagram(input_word, word_list, max_anagrams):
	lettercount = Counter(input_word)
	anagrams = []


	def forbidden_letters(worda, wordb):
		# does worda have any letters that are not in word b?
		for l in worda:
			if l not in wordb:
				return True
		return False


	print("Filtering words...")
	# print("Word count: " + str(len(word_list)))
	# filter out words that aren't going to work
	filtered_list = []
	for word in word_list:
		if len(word) > len(input_word):
			continue
		if forbidden_letters(word, input_word):
			continue
		filtered_list.append(word)
	# print("Filtered word count: " + str(len(filtered_list)))

	print("Building letter counts...")
	counter_list = {}
	for word in filtered_list:
		counter_list[word] = Counter(word)
	# print("counters: " + str(len(counter_list)))


	def anagram_recurse(lettercount, word_list, possible_anagram, anagrams, call_count, max_anagrams):
		if len(anagrams) >= max_anagrams:
			return call_count
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
					call_count = anagram_recurse(lettercount_copy, word_list, possible_anagram + " " + aword, anagrams, call_count, max_anagrams)
		call_count += 1
		if call_count % 100 == 0:
			sys.stdout.write('.')
			sys.stdout.flush()
		return call_count

	print("Searching...")
	callcount = anagram_recurse(lettercount, counter_list, '', anagrams, 0, max_anagrams)
	print("Called " + str(callcount) + " times.")
	return anagrams




if __name__ == "__main__":
	description = "Typhon: Anagram Generator in Python"
	print(description)
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-w', '--word', type=str, required=True, help='Outbound call gateway')
	parser.add_argument('-s', '--small', action='store_true', help='Use small word list')
	parser.add_argument('-o', '--outfile', type=str, help='Store results to output file')
	parser.add_argument('-m', '--max', type=int, default=50, help='Maximum number of anagrams to generate')

	args = parser.parse_args()
	inword = args.word.lower().replace(' ', '')

	words = []
	filename = 'words.txt'
	if args.small:
		filename = 'small-words.txt'
	with open(filename) as f:
		for line in f:
			words.append(line.strip())
	# print(words)
	print("Words file ready.")

	anagrams = anagram(inword, words, args.max)
	anagrams.sort()
	if args.outfile:
		print("Writing output file.")
		with open(args.outfile, 'w') as of:
			for ana in anagrams:
				of.write(ana + '\n')
	else:
		print("\n".join(anagrams))
