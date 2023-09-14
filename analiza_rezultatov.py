import os

def analiza_rezultatov(file_path, exact_matches, one_over_matches, one_over_year_spike, povprečno_odstopanje, ix_poskusa):
    # Open the file for reading
    with open(file_path, 'r', encoding="utf-8") as file:
        # Read the first two lines
        line1 = file.readline().split(":")[1].strip()
        line2 = file.readline().split(":")[1].strip()
        line3 = file.readline()
        line4 = file.readline().split(":")[1].strip()
        line5 = file.readline().split(" ")[1].strip()
        line5 = line5.replace(":","")

        # Convert the values to appropriate data types if needed
        if(int(line5) == -1):
            number_of_clusters = int(line1)    
        else:
            number_of_clusters = int(line1) + 1
        expected_clusters = int(line2)

        lines = file.readlines()

        year_distribution = {}

        # Flag to indicate if we're inside the "Year Distribution" section
        inside_year_distribution = False

        # Iterate through each line in the text
        for line in lines:
            if line.startswith("Year Distribution:"):
                inside_year_distribution = True
            if line.startswith("Closest Sentences:"):
                inside_year_distribution = False
            elif inside_year_distribution and line.strip() and not line.startswith("Year Distribution:"):  # Check if it's not an empty line
                # Split the line into year and count/percentage parts
                parts = line.strip().split(': ')
                year = parts[0].replace("Year ", "")
                count_percentage = parts[1].split(', ')
                percentage = float(count_percentage[1].replace('%', ''))
                year_distribution[year] = {'Percentage': percentage}


        if(number_of_clusters == expected_clusters + 1):
            exact_matches[ix_poskusa-1] = exact_matches[ix_poskusa-1] + 1
        if(number_of_clusters == expected_clusters + 2):
            one_over_matches[ix_poskusa-1] = one_over_matches[ix_poskusa-1] + 1
        if(number_of_clusters>expected_clusters+1 and number_of_clusters<=expected_clusters+100):
            povprečno_odstopanje[ix_poskusa-1] = povprečno_odstopanje[ix_poskusa-1] +  ((number_of_clusters-1)-expected_clusters)
        if(number_of_clusters<=expected_clusters):
            povprečno_odstopanje[ix_poskusa-1] = povprečno_odstopanje[ix_poskusa-1] + (expected_clusters-(number_of_clusters-1))


for num in range(3,11):

    folder_path = r"C:\Users\Blaž\Desktop\Diploma\Code_data\clusters_word_sl\words_with_{}_meanings_clusters".format(num)

    if(num <= 5):
        exact_matches = [0,0,0,0]
        one_over_matches = [0,0,0,0]
        one_over_year_spike = [0,0,0,0]
        povprečno_odstopanje = [0,0,0,0]
        total_words = 0

    for filename in os.listdir(folder_path):
        total_words += 1
        if filename.endswith("_euclidean.txt"):
           analiza_rezultatov(os.path.join(folder_path, filename), exact_matches, one_over_matches, one_over_year_spike, povprečno_odstopanje, 1)
        if filename.endswith("_euclidean_thr.txt"):
           analiza_rezultatov(os.path.join(folder_path, filename), exact_matches, one_over_matches, one_over_year_spike, povprečno_odstopanje, 2)
        if filename.endswith("_cosine.txt"):
           analiza_rezultatov(os.path.join(folder_path, filename), exact_matches, one_over_matches, one_over_year_spike, povprečno_odstopanje, 3)
        if filename.endswith("_cosine_thr.txt"):
           analiza_rezultatov(os.path.join(folder_path, filename), exact_matches, one_over_matches, one_over_year_spike, povprečno_odstopanje, 4)

    if(num <= 4 or num == 10):
        total_words = int(total_words/4)

    file_path = r"C:\Users\Blaž\Desktop\Diploma\Code_data\analiza_sl\analiza_rezultatov_besed_z_{}_pomeni.txt".format(num)

    with open(file_path, "w") as file:
        file.write("Besede z {} pomeni\n".format(num))
        file.write("Poskus 1: Euclidean\n")
        file.write("Exact matches za poskus 1 = {}/{} v procentih: {}\n".format(exact_matches[0], total_words, exact_matches[0]/total_words*100))
        file.write("One over matches za poskus 1 = {}/{} v procentih: {}\n".format(one_over_matches[0], total_words, one_over_matches[0]/total_words*100))
        file.write("Povprečno odstopanje = {}\n".format(povprečno_odstopanje[0]/total_words))
        file.write("Poskus 2: Euclidean_thr\n")
        file.write("Exact matches za poskus 2 = {}/{} v procentih: {}\n".format(exact_matches[1], total_words, exact_matches[1]/total_words*100))
        file.write("One over matches za poskus 2 = {}/{} v procentih: {}\n".format(one_over_matches[1], total_words, one_over_matches[1]/total_words*100))
        file.write("Povprečno odstopanje = {}\n".format(povprečno_odstopanje[1]/total_words))
        file.write("Poskus 3: Cosine\n")
        file.write("Exact matches za poskus 3 = {}/{} v procentih: {}\n".format(exact_matches[2], total_words, exact_matches[2]/total_words*100))
        file.write("One over matches za poskus 3 = {}/{} v procentih: {}\n".format(one_over_matches[2], total_words, one_over_matches[2]/total_words*100))
        file.write("Povprečno odstopanje = {}\n".format(povprečno_odstopanje[2]/total_words))
        file.write("Poskus 4: Cosine_thr\n")
        file.write("Exact matches za poskus 4 = {}/{} v procentih: {}\n".format(exact_matches[3], total_words, exact_matches[3]/total_words*100))
        file.write("One over matches za poskus 4 = {}/{} v procentih: {}\n".format(one_over_matches[3], total_words, one_over_matches[3]/total_words*100))
        file.write("Povprečno odstopanje = {}\n".format(povprečno_odstopanje[3]/total_words))