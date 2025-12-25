
import json
import sys
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from sentence_transformers import SentenceTransformer, util
from scipy.stats import spearmanr

# Ensure we can import modules if needed, but we'll implement logic directly to be standalone
# This script compares TF-IDF vs SBERT vs Hybrid against Ground Truth

def load_dataset(path="dataset.json"):
    with open(path, "r") as f:
        return json.load(f)

def run_tfidf_benchmark(data):
    """Calculates TF-IDF similarity for each pair."""
    vectorizer = TfidfVectorizer(stop_words='english')
    scores = []
    
    print(f"Running TF-IDF Benchmark on {len(data)} pairs...")
    for item in data:
        corpus = [item['resume_text'], item['jd_text']]
        tfidf_matrix = vectorizer.fit_transform(corpus)
        # Cosine sim between row 0 and row 1
        score = sklearn_cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        scores.append(score)
    return scores

def run_sbert_benchmark(data):
    """Calculates SBERT similarity for each pair."""
    print("Running SBERT Benchmark (Loading Model)...")
    # Load model (this will download if not present, but we should have it)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    scores = []
    
    for item in data:
        emb1 = model.encode(item['resume_text'], convert_to_tensor=True)
        emb2 = model.encode(item['jd_text'], convert_to_tensor=True)
        score = util.cos_sim(emb1, emb2).item()
        scores.append(score)
    return scores

def calculate_metrics(ground_truth, predictions, model_name):
    """Calculates evaluation metrics."""
    # Spearman Correlation
    corr, _ = spearmanr(ground_truth, predictions)
    
    # Mean Squared Error
    mse = np.mean((np.array(ground_truth) - np.array(predictions)) ** 2)
    
    print(f"--- {model_name} Results ---")
    print(f"Spearman Correlation: {corr:.4f}")
    print(f"Mean Squared Error:   {mse:.4f}")
    print("-" * 30)
    
    with open("benchmark_results.txt", "a") as f:
        f.write(f"--- {model_name} Results ---\n")
        f.write(f"Spearman Correlation: {corr:.4f}\n")
        f.write(f"Mean Squared Error:   {mse:.4f}\n")
        f.write("-" * 30 + "\n")
    
    return corr, mse

def main():
    if not os.path.exists("dataset.json"):
        print("Error: dataset.json not found. Run data_generator.py first.")
        return

    data = load_dataset()
    ground_truth = [item['ground_truth_score'] for item in data]
    
    # 1. TF-IDF Baseline
    tfidf_scores = run_tfidf_benchmark(data)
    calculate_metrics(ground_truth, tfidf_scores, "TF-IDF (Baseline)")
    
    # 2. SBERT (Our System)
    sbert_scores = run_sbert_benchmark(data)
    calculate_metrics(ground_truth, sbert_scores, "SBERT (Our Model)")
    
    # 3. Hybrid (Example with fixed weights)
    # Hybrid = 0.7 * TF-IDFish (Skill) + 0.3 * SBERT
    # Note: Our paper actually defines S_skills as Jaccard. 
    # For this synthetic benchmark, we'll approximate 'Skill Score' with TF-IDF for simplicity 
    # OR we can just show SBERT dominance. Let's do a simple weighted mix of the two above.
    alpha = 0.3
    beta = 0.7
    hybrid_scores = [ (alpha * t) + (beta * s) for t, s in zip(tfidf_scores, sbert_scores) ]
    calculate_metrics(ground_truth, hybrid_scores, f"Hybrid (a={alpha}, b={beta})")

if __name__ == "__main__":
    main()
