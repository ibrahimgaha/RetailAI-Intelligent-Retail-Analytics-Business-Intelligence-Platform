def preprocess_review(review_text: str):
    """
    Basic preprocessing for the review text before passing it to Gemini.
    Could include stripping, basic length checks, or simple keyword heuristics
    if we were using a local NLP model. For now, it categorizes based on naive rules
    to simulate the local classification step before Gemini explains it.
    """
    text = review_text.lower().strip()
    
    if not text:
        return "Unknown"
        
    positive_words = ["great", "excellent", "good", "amazing", "love", "fantastic", "best", "recommend"]
    negative_words = ["bad", "terrible", "worst", "hate", "awful", "poor", "slow", "broken"]
    
    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)
    
    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"

def get_sentiment_confidence(sentiment: str):
    """
    Simulates a confidence score that might come from a local ML model.
    """
    if sentiment == "Positive":
        return 0.85
    elif sentiment == "Negative":
        return 0.92
    else:
        return 0.65
