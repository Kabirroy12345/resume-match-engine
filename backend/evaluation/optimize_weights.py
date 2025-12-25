
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import spearmanr

def optimize():
    print("Starting Grid Search for Optimal Alpha/Beta...")
    
    # Load Data
    with open("dataset.json", "r") as f:
        data = json.load(f)
        
    ground_truth = [item['ground_truth_score'] for item in data]
    
    # Pre-calculate component scores to avoid re-running expensive inference
    # Component 1: Semantic (SBERT)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sbert_scores = []
    for item in data:
        e1 = model.encode(item['resume_text'], convert_to_tensor=True)
        e2 = model.encode(item['jd_text'], convert_to_tensor=True)
        sbert_scores.append(util.cos_sim(e1, e2).item())
        
    # Component 2: Keyword/Skill (Approximated by TF-IDF here for optimization)
    # In production, this is Jaccard of skills. For optimization, TF-IDF is a good proxy for "keyword overlap".
    vectorizer = TfidfVectorizer(stop_words='english')
    corpus_pairs = [(d['resume_text'], d['jd_text']) for d in data]
    tfidf_scores = []
    
    # We need to fit vectorizer on ALL text to get proper vocabulary
    all_text = [d['resume_text'] for d in data] + [d['jd_text'] for d in data]
    vectorizer.fit(all_text)
    
    from sklearn.metrics.pairwise import cosine_similarity
    for r, j in corpus_pairs:
        mat = vectorizer.transform([r, j])
        tfidf_scores.append(cosine_similarity(mat[0:1], mat[1:2])[0][0])
        
    # Grid Search
    # Formula: Score = alpha * Skill(TFIDF) + beta * Semantic(SBERT)
    # Constraint: alpha + beta = 1.0 (usually)
    
    best_corr = -1.0
    best_alpha = 0.0
    best_beta = 0.0
    
    results = []
    
    # Search alpha from 0.0 to 1.0 step 0.05
    for alpha in np.arange(0.0, 1.05, 0.05):
        beta = 1.0 - alpha
        
        # Calculate hybrid scores for this config
        hybrid_scores = [ (alpha * t) + (beta * s) for t, s in zip(tfidf_scores, sbert_scores) ]
        
        # Calculate metric (Spearman Correlation with Ground Truth)
        corr, _ = spearmanr(ground_truth, hybrid_scores)
        
        if corr > best_corr:
            best_corr = corr
            best_alpha = alpha
            best_beta = beta
            
        results.append((alpha, beta, corr))
        
    print(f"\nOptimization Complete.")
    print(f"Best Correlation: {best_corr:.4f}")
    print(f"Optimal Alpha (Keyword/Skill): {best_alpha:.2f}")
    print(f"Optimal Beta (Semantic):       {best_beta:.2f}")
    
    # Save optimized params
    params = {"alpha": round(best_alpha, 2), "beta": round(best_beta, 2), "correlation": round(best_corr, 4)}
    with open("optimized_params.json", "w") as f:
        json.dump(params, f, indent=4)
        
    print("Optimal parameters saved to 'optimized_params.json'")

if __name__ == "__main__":
    if not os.path.exists("dataset.json"):
        print("Please run data_generator.py first.")
    else:
        optimize()
