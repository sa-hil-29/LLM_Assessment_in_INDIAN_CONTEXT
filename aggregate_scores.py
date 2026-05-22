import json
import os

results_dir = r"d:/LLM_Assesment_in_INDIAN_CONTEXT/results"
models = ["llama_3_3_70b_versatile", "qwen_qwen3_32b", "llama_3_1_8b_instant"]
categories = ["stereotype", "ethics", "toxicity", "fairness", "privacy"]

stats = {}

for model in models:
    stats[model] = {}
    for cat in categories:
        stats[model][cat] = {"safe": 0, "total": 0}

    # Search in root and subdirectories
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            if model in file and file.endswith(".json"):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        results = data.get("results", [])
                        for res in results:
                            # Try to find category
                            cat_found = None
                            
                            # Check if the file is in a category directory
                            rel_path = os.path.relpath(root, results_dir)
                            if rel_path in categories:
                                cat_found = rel_path
                            else:
                                # Check input for category
                                inp = res.get("input", {})
                                prompt = inp.get("prompt", {})
                                if "category" in prompt:
                                    cat_found = prompt["category"]
                                elif "stereotype_topic_tag" in prompt:
                                    cat_found = "stereotype"
                                elif "category" in inp:
                                    cat_found = inp["category"]
                            
                            if cat_found and cat_found in categories:
                                stats[model][cat_found]["total"] += 1
                                if res.get("is_safe", False):
                                    stats[model][cat_found]["safe"] += 1
                except Exception as e:
                    pass

print(json.dumps(stats, indent=4))
