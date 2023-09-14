import json
import os

for num in range(3,11):
    
    file_path = r"C:\Users\Blaž\Desktop\Diploma\Code_data\sense_inventory\lemma_count_{}.json".format(num)

    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        if(len(data) == 0):
            continue

    search_words = list(data.keys())

    # File path for the existing JSON file
    input_json_file = r'C:\Users\Blaž\Desktop\Diploma\Code_data\meanings\words_with_{}_meanings\results.json'.format(num)

    # Read the existing JSON file
    with open(input_json_file, 'r', encoding='utf-8') as json_file:
        results = json.load(json_file)

    # Create a dictionary to hold results for each word
    word_results = {word: [] for word in search_words}

    # Organize the results based on the word
    for result in results:
        word = result['word']
        if(word.lower() == "gsm"):
            continue
        else:
            word_results[word.lower()].append(result)

    # Save the results for each word as separate JSON files
    for word, word_result in word_results.items():
        # File path for the JSON file
        json_file_path = os.path.join(r'C:\Users\Blaž\Desktop\Diploma\Code_data\meanings\words_with_{}_meanings'.format(num), f'{word}.json')

        # Save the 'word_result' list as a JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(word_result, json_file, ensure_ascii=False, indent=4)
