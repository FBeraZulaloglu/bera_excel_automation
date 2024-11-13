import pandas as pd
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz
import re
import fuzzy
from sklearn.metrics.pairwise import cosine_similarity

# Load the model for semantic similarity
model = SentenceTransformer('all-mpnet-base-v2')

soundex = fuzzy.Soundex(4)

def preprocess_name(name):
    name = re.sub(r'\b(inc|co|ltd|corp|llc)\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[^a-zA-Z0-9]', ' ', name)
    return name.strip().lower()

def is_similar_name(name1, name2, char_threshold=70, semantic_threshold=0.75):
    # Preprocess the brand names
    name1, name2 = preprocess_name(name1), preprocess_name(name2)
    
    # Character similarity check
    char_similarity = fuzz.ratio(name1, name2)
    if char_similarity >= char_threshold:
        return True
    
    # Phonetic similarity check (optional)
    if soundex(name1) == soundex(name2):
        return True
    
    # Semantic similarity check
    embedding1 = model.encode(name1)
    embedding2 = model.encode(name2)
    semantic_similarity = util.cos_sim(embedding1, embedding2).item()
    
    return semantic_similarity >= semantic_threshold

def get_sentence_similarity_score(brand1,brand2,semantic_threshold=0.74):
    model_name = "bert-base-nli-mean-tokens"
    model = SentenceTransformer(model_name)
    
    embedding = model.encode([brand1,brand2])
    similarity = cosine_similarity([embedding[0]],embedding[1:])
    #print(similarity[0][0])
    return similarity >= semantic_threshold

# Load Excel file
input_file = "/Users/farukbera/Desktop/bera_excel_automation/liste.xlsx"  # Replace with your input file path
df = pd.read_excel(input_file)

# Get the first two rows to compare brands (Assuming brand names are in 'Brand1' and 'Brand2' columns)
# Adjust 'Brand1' and 'Brand2' to your column names as needed
rows_to_compare = df[['İzlenecek Kelime', 'Marka Adı']]

# Initialize a list to store similar brand pairs
similar_brands = []

# Compare the brands in the specified rows
for index, row in rows_to_compare.iterrows():
    print("INDEX", index)
    brand1 = row['İzlenecek Kelime']
    brand2 = row['Marka Adı']
    
    if get_sentence_similarity_score(brand1, brand2):
        similar_brands.append({'İzlenecek Kelime': brand1, 'Marka Adı': brand2, 'Benzer': 'Evet'})
    else:
        similar_brands.append({'İzlenecek Kelime': brand1, 'Marka Adı': brand2, 'Similarity': 'Hayır'})

similar_df = pd.DataFrame(similar_brands)

output_file = "similar_brands.xlsx"
similar_df.to_excel(output_file, index=False)

print(f"Similarity check complete. Results saved to {output_file}")
