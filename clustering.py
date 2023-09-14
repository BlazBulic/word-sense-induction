import numpy as np
import os
import json
import umap
import hdbscan
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def cluster_and_save(data, distance_metric, threshold, save_fig):
            if(threshold):
                total_sentences = len(sentence_embeddings)
                thr = int(0.05*total_sentences)
                file_ending = distance_metric + "_thr"
            else:
                thr = 5
                file_ending = distance_metric

            if(distance_metric == 'cosine'):
                cosine_distances = pairwise_distances(data, metric='cosine').astype(np.double)
                distance_metric = 'precomputed'
                data = cosine_distances

            # Perform HDBSCAN clustering
            clusterer = hdbscan.HDBSCAN(min_cluster_size=thr, min_samples=5, metric=distance_metric)
            cluster_labels = clusterer.fit_predict(data)

            # Get the probability scores for each data point
            probability_scores = clusterer.probabilities_

            # Initialize a dictionary to store representatives
            representatives_dict = {i: [] for i in np.unique(cluster_labels)}

            # Find the 5 representatives for each cluster based on highest probabilities
            num_representatives = 5
            for cluster_label in np.unique(cluster_labels):
                cluster_indices = np.where(cluster_labels == cluster_label)[0]
                cluster_probs = probability_scores[cluster_indices]

                # Find the indices of the top representatives
                top_indices = cluster_indices[np.argsort(cluster_probs)[-num_representatives:]]
                
                # Get the corresponding sentences for the top representatives
                top_representatives = [sentence_keys[i] for i in top_indices]
                
                representatives_dict[cluster_label] = top_representatives

            if(save_fig):
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                # Scatter plot of UMAP embeddings in 3D
                ax.scatter(X_umap[:, 0], X_umap[:, 1], X_umap[:, 2], s=5, c=cluster_labels)
                # Set labels for each axis
                ax.set_xlabel('UMAP Dimension 1')
                ax.set_ylabel('UMAP Dimension 2')
                ax.set_zlabel('UMAP Dimension 3')
                plt.title('UMAP Embeddings in 3D')
                plt.savefig(r"C:\\Users\\Blaž\\Desktop\\Diploma\\Code_data\\targeted_words_sl\\figures\\{}_{}.png".format(word, file_ending))

            # Create a dictionary to store year distribution for each cluster
            year_distribution_by_cluster = {i: {} for i in np.unique(cluster_labels)}
            # Populate the year distribution dictionary
            for cluster_label, sentence_key in zip(cluster_labels, sentence_keys):
                year = sentence_embedding_dict_year[sentence_key]["year"]
                if year in year_distribution_by_cluster[cluster_label]:
                    year_distribution_by_cluster[cluster_label][year] += 1
                else:
                    year_distribution_by_cluster[cluster_label][year] = 1

            # Calculate the total number of sentences in each cluster
            total_sentences_by_cluster = {cluster_label: sum(year_distribution.values()) for cluster_label, year_distribution in year_distribution_by_cluster.items()}

            # Write the closest sentences to a text file
            with open(r"C:\Users\Blaž\Desktop\Diploma\Code_data\targeted_words_sl\clusters\words_with_{}_meanings_clusters\{}_{}.txt".format(num,word,file_ending), "w", encoding="utf-8") as txt_file:
                txt_file.write(f"Number of clusters: {len(np.unique(cluster_labels))}\n")
                txt_file.write(f"Expected clusters: {num}\n\n")
                txt_file.write(f"Number all vectors: {num_of_sentences}\n")
                for cluster_label in np.unique(cluster_labels):
                    txt_file.write(f"Cluster {cluster_label}:\n")
                    txt_file.write(f"Number of vectors in this cluster: {np.sum(cluster_labels == cluster_label)}\n")
                    txt_file.write("Year Distribution:\n")
                    for year, count in year_distribution_by_cluster[cluster_label].items():
                        txt_file.write(f"Year {year}: {count}, {(count/total_sentences_by_cluster[cluster_label]*100):.2f}%\n")
                    
                    txt_file.write("\nClosest Sentences:\n")
                    for idx, sentence in enumerate(representatives_dict[cluster_label], start=1):
                        txt_file.write(f"{idx}. {sentence}\n")
                    txt_file.write("\n")

for num in [3,5]:

    folder_path = r"C:\Users\Blaž\Desktop\Diploma\Code_data\targeted_words_sl\embeddings\words_with_{}_meanings_embedded".format(num)

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            word = filename.split('_')[0]

            # Load data from the JSON file
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            sentence_embedding_dict = {}
            sentence_embedding_dict_year = {}
            num_of_sentences = len(data)
            for dict in data:
                if(dict["embedding"] == None):
                    num_of_sentences -= 1
                    continue
                year = dict["publish_year"]
                sentence = dict["sentence"]
                embedding = dict["embedding"]
                sentence_embedding_dict[sentence] =  embedding
                sentence_embedding_dict_year[sentence] =  {"embedding": embedding, "year": year}

            # Convert sentence embeddings dictionary to a list of embeddings and a list of sentence keys
            sentence_embeddings = list(sentence_embedding_dict.values())
            sentence_keys = list(sentence_embedding_dict.keys())
            num_of_sentences = len(sentence_keys)

            # Convert the list of embeddings to a NumPy array
            X = np.array(sentence_embeddings)
            X = np.squeeze(X)

            # Reduce dimensionality with UMAP
            umap_model = umap.UMAP(n_components=3, random_state=42)
            X_umap = umap_model.fit_transform(X)

            cluster_and_save(X_umap, 'euclidean', False, True)
            cluster_and_save(X_umap, 'euclidean', True, True)
            cluster_and_save(X_umap, 'cosine', False, True)
            cluster_and_save(X_umap, 'cosine', True, True)


print("KONČANO")