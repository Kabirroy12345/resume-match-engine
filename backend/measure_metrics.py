import time
import os
from app.main import get_similarity, get_sbert_model

def measure_performance():
    print("--- PERFORMANCE BENCHMARK ---")
    
    # 1. Cold Boot / Model Load Time
    start_load = time.time()
    model = get_sbert_model()
    end_load = time.time()
    load_time = end_load - start_load
    print(f"Model Load Time: {load_time:.4f} seconds")

    # 2. Inference Time (Similarity)
    text1 = "Experienced Python developer with Flask and AWS skills."
    text2 = "Looking for a Software Engineer with Python and Cloud experience."
    
    # Warmup
    get_similarity(text1, text2)
    
    # Measure
    start_inf = time.time()
    for _ in range(50):
        get_similarity(text1, text2)
    end_inf = time.time()
    avg_inf = (end_inf - start_inf) / 50
    print(f"Avg Inference Time (50 runs): {avg_inf:.4f} seconds")

if __name__ == "__main__":
    measure_performance()
