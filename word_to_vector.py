import torch
from transformers import BertTokenizer, BertModel
from transformers import AutoTokenizer, AutoModelForMaskedLM
import json
import os
import nltk
from nltk.tokenize import word_tokenize

torch.manual_seed(42)

if torch.cuda.is_available():
    torch.cuda.manual_seed(42)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# Load pre-trained BERT model and tokenizer
""" model_name = "bert-base-multilingual-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name, output_hidden_states=True) """

tokenizer = AutoTokenizer.from_pretrained("EMBEDDIA/sloberta")
model = AutoModelForMaskedLM.from_pretrained("EMBEDDIA/sloberta", output_hidden_states=True)

# Move the model to the GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

model.eval()

# Function to embed a word in a sentence
def word_to_bert_embedding(sentence, word):
    # Tokenize the sentence and convert to tensors
    tokens = word_tokenize(sentence, language='slovene')
    
    # Check if the word is in the list of tokens
    if((word not in tokens) or (len(tokens) > 512)):
        return None  # Skip processing for this word
    
    word_position = tokens.index(word)

    # Convert tokens to IDs
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    
    # Convert to a PyTorch tensor
    input_ids = torch.tensor(input_ids).unsqueeze(0).to(device)
    
    # Get the model's output embeddings
    with torch.no_grad():
        outputs = model(input_ids)
        hidden_states = outputs.hidden_states[-4:]
    
    # Get the word embedding from the last 4 layers
    word_embedding = torch.cat([hidden_states[i][0][word_position].unsqueeze(0) for i in range(4)], dim=0)
    word_embedding = torch.mean(word_embedding, dim=0)  # Average the embeddings from the last 4 layers

    # Normalize the word_embedding
    normalized_embedding = normalize_tensor(word_embedding)

    return normalized_embedding.cpu().detach().numpy()

# Function to normalize a tensor along a specified dimension
def normalize_tensor(tensor, dim=0, eps=1e-8):
    norm = torch.norm(tensor, p=2, dim=dim, keepdim=True)
    return tensor / (norm + eps)

# Root folder containing subfolders
root_folder = r'C:\Users\Blaž\Desktop\Diploma\Code_data\targeted_words_ml\embeddings'

# Iterate over subfolders
for num in range(3,11):  # Assuming subfolders are named from words_with_3_meanings_embedded to words_with_10_meanings_embedded
    subfolder_name = f'words_with_{num}_meanings_embedded'
    subfolder_path = os.path.join(root_folder, subfolder_name)

    # Check if the subfolder exists
    if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):

        # Iterate over JSON files in the subfolder
        for filename in os.listdir(subfolder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(subfolder_path, filename)

                # Load and process JSON file
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)

                # Get the BERT vector for the word in the sentences
                for dict in data:
                    sentence = dict["sentence"]
                    word = dict["word"]
                    word_embedding = word_to_bert_embedding(sentence, word)  # Replace with your word embedding function
                    if(word_embedding is None):
                        dict["embedding"] = word_embedding
                    else:
                        dict["embedding"] = word_embedding.tolist()

                # File path for the JSON file
                json_file_path = r'C:\Users\Blaž\Desktop\Diploma\Code_data\targeted_words_sl\embeddings\words_with_{}_meanings_embedded\{}_embedded.json'.format(num, word)

                # Save the 'results' list as a JSON file
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)

