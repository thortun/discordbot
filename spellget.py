import requests
import json
import numpy as np

def find_closest_in_list(attempt, word_list):
	d = 10000
	closest = word_list[-1]
	for word in word_list:
		new_d = levenshtein(word.lower(), attempt)
		if new_d < d:
			d = new_d
			closest = word
	return closest

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def get_spell_from_string(string_attempt):
    query = string_attempt
    with open("data/spell-list.json") as fileID:
        spell_list = json.loads(fileID.read())
        spell_list_lower = [spell.lower() for spell in spell_list]
        if query not in spell_list_lower:
            query = find_closest_in_list(query, spell_list_lower)
    print("Getting spell %s" % query)
    r = requests.get("http://www.dnd5eapi.co/api/spells/%s" % query.replace(" ", "-"))
    return r.json()

if __name__ == "__main__":
	attempt = "Fireall"
	print(get_spell_from_string(attempt))