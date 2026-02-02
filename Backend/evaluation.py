keyword_map = {
    "What is supervised learning?": ["labeled data", "input", "output", "predict"],
    "What is unsupervised learning?": ["unlabeled data", "patterns", "clusters"],
    "What is classification?": ["category", "class", "label"],
    "What is regression?": ["number", "continuous value", "predict"],
    "What is cross-validation and why is it important?": ["splitting data", "avoids overfitting"],
    "What is the purpose of feature scaling?": ["normalization", "standardization", "similar scale"],
    "What is a decision tree?": ["flowchart", "splits data", "decision"],
    "What is k-means clustering?": ["k clusters", "centroid", "similarity"],
    "What is the bias-variance tradeoff?": ["bias", "variance", "overfitting", "underfitting"],
    "How do you handle imbalanced datasets?": ["oversampling", "undersampling", "f1-score", "precision", "recall"]
}

def length_score(answer):
  words=answer.split()
  if len(words)<10:
    return "Weak"
  elif len(words)<30:
    return "Average"
  else:
    return "Good"



def keyword_score(answer,keyword):
  found =0
  for kw in keyword:
    if kw.lower()in answer.lower():
      found+=1
  return found



def missing_keywords(answer, keywords):
    missing = []
    for kw in keywords:
        if kw.lower() not in answer.lower():
            missing.append(kw)
    return missing



def has_example(answer):
  example_word=["example","for example","such as"]
  for word in example_word:
    if word in answer.lower():
      return True
  return False


def final_score(answer, keywords):
    score = 0
   # 1. Length check
    if length_score(answer) != "Weak":
        score += 1  # point if not very short

    # 2. Keyword check (realistic threshold)
    found_keywords = keyword_score(answer, keywords)
    required_keywords = max(2, len(keywords)//2)  # Strong answer needs enough keywords
    if found_keywords >= required_keywords:
        score += 1

    # 3. Example check (optional bonus)
    if has_example(answer):
        score += 1
    return score


def get_quality(score):
  if score<=1:
    return "weak"
  elif score==2:
    return "Average"
  else:
    return "Good"



def feedback(answer, keywords):
    reasons = []
    if length_score(answer) == "Weak":
        reasons.append("Answer too short")
    missing = missing_keywords(answer, keywords)
    if missing:
        reasons.append(f"Missing keywords: {', '.join(missing)}")
    if not has_example(answer):
        reasons.append("No example provided (optional)")
    return reasons