my_list = "The quick brown fox jumps over the lazy dog is an English-language pangram—a sentence that contains all of the letters of the English alphabet. Owing to its brevity and coherence, it has become widely known."

def split_string(string, seperator="\n"):
	string = string.split(seperator)
	resp = [seperator.join(string[:int(len(string)/2)]),seperator.join(string[int(len(string)/2):])]
	# print(resp)
	return resp

def too_long(data):
	for item in data:
		if len(item) > target_length:
			return True
	return False


target_length = 20
if len(my_list) >= target_length:
	result = split_string(my_list, " ")
	while too_long(result):
		new_result = []
		for count, part in enumerate(result):
			halfed = split_string(part, " ")
			new_result.append(halfed[0])
			new_result.append(halfed[1])
		result = new_result
else:
	result = [" ".join(my_list)]
		# print(result)
# print(len(my_list))
print("\n".join(result))
