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
    """Returns a spell in json format given an attempt at typin
    the spell name. Queries dnd5eapi.co for spells.
    """
    assert len(string_attempt) < 150
    query = string_attempt.lower()                                                  # Typed spell name to find
    with open("data/spells.json") as fileID:                                        # Open the spell-file
        spells_json = json.loads(fileID.read())                                     # Read the spell-file
        spell_list = [entry["name"].lower() for entry in spells_json["results"]]    # Make a list of all spell names in lower in lower
        if query not in spell_list:
            query = find_closest_in_list(query, spell_list)                         # Find the closest match in the list of spells
    print("Getting spell %s" % query)
    r = requests.get("http://www.dnd5eapi.co/api/spells/%s" % query.replace(" ", "-"))
    return r.json()

if __name__ == "__main__":
    with open("data/spells.json") as fileID:                                        # Open the spell-file
        spells_json = json.loads(fileID.read())                                     # Read the spell-file
        print("Found %s spells." % len(spells_json["results"]))
