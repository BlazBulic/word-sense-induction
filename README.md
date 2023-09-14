# word_sense_induciton

The repository includes code used in bachelor thesis with  the title: Word sense induction in Slovene using large language models.

Contents:
  - Files "sentence_extraction.py" and "split_depending_on_word" are used for data preproccesing.
  - File "word_to_vector.py" contains code for embedding a word in a sentence using the last 4 layers of mBERT model or SloBERTa model.
  - File "clustering.py" contains code for dimensionality reduction and clustering of word embeddings.
  - File "analiza_rezultatov" produces quantitative results of clusterings.
