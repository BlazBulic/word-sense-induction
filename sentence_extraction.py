import json
import os
import re


# Directory path where your JSON files are stored
root_directory = r"C:\Users\Blaž\Desktop\Diploma\eventregistry"  # Change this to the root folder containing subfolders with JSON files

# Function to extract sentences containing any of the search words from a text
def extract_sentences_with_search_words(text, search_words):
    sentences_with_words = []
    search_pattern = rf'\b({"|".join(re.escape(word) for word in search_words)})\b'
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    for sentence in sentences:
        match = re.search(search_pattern, sentence, re.IGNORECASE)
        if match:
            matched_word = match.group(0)
            sentences_with_words.append((sentence.strip(), matched_word))
    return sentences_with_words

for num in range(3,11):

    # Words you want to search for
    file_path = r"C:\Users\Blaž\Desktop\Diploma\Code_data\sense_inventory\lemma_count_{}.json".format(num)
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        if(len(data) == 0):
            json_file_path = r'C:\Users\Blaž\Desktop\Diploma\Code_data\meanings\words_with_{}_meanings\results.json'.format(num)
            results = []
            # Save the 'results' list as a JSON file
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(results, json_file, ensure_ascii=False, indent=4)

    search_words = list(data.keys())



    # List to store the results
    results = []

    # Loop through each JSON file in the directory
    for foldername, subfolders, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.json') or filename.endswith('.jsonl'):
                file_path = os.path.join(foldername, filename)

                # Read the JSON file
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    if(filename.endswith('.json')):
                        data = json.load(json_file)

                        # Access the "results" array inside the "articles" key
                        articles = data.get("articles", {}).get("results", []) 

                        # Assuming each JSON file contains an array of articles, loop through each article
                        for article in articles:
                            # Extract the necessary fields
                            article_title = article["title"]
                            publish_year = int(article['date'].split('-')[0])  # Assuming date is in format "YYYY-MM-DD"
                            article_content = article["body"]  # Change this field based on your dataset

                            # Extract sentences containing the exact selected word
                            sentences_with_exact_words = extract_sentences_with_search_words(article_content, search_words)

                            # Append the relevant information to the results list
                            for sentence, word in sentences_with_exact_words:
                                result = {
                                    'title': article_title,
                                    'publish_year': publish_year,
                                    'word': word,
                                    'sentence': sentence
                                }
                                results.append(result)

                    
                    elif(filename.endswith('.jsonl')):
                        data = [json.loads(line) for line in json_file]

                        for dict in data:
                            # Access the "results" array inside the "articles" key
                            articles = dict.get("articles", {}).get("results", []) 

                            # Assuming each JSON file contains an array of articles, loop through each article
                            for article in articles:
                                # Extract the necessary fields
                                article_title = article["title"]
                                publish_year = int(article['date'].split('-')[0])  # Assuming date is in format "YYYY-MM-DD"
                                article_content = article["body"]  # Change this field based on your dataset

                                # Extract sentences containing the exact selected word
                                sentences_with_exact_words = extract_sentences_with_search_words(article_content, search_words)

                                # Append the relevant information to the results list
                                for sentence, word in sentences_with_exact_words:
                                    result = {
                                        'title': article_title,
                                        'publish_year': publish_year,
                                        'word': word,
                                        'sentence': sentence
                                    }
                                    results.append(result)

    # File path for the JSON file
    json_file_path = r'C:\Users\Blaž\Desktop\Diploma\Code_data\meanings\words_with_{}_meanings\results.json'.format(num)

    # Save the 'results' list as a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)


