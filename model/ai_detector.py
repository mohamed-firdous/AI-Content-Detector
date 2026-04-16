import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

# Globally deploy GPT2 to save memory mapping overhead on frequent calls
# Selects GPU if available otherwise defaults perfectly to CPU strings.
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    model_id = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
    tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
except Exception as e:
    print(f"Warning: Could not load GPT2 model. {e}")
    model = None
    tokenizer = None


def compute_perplexity(text):
    """
    Calculate the mathematical perplexity score by sampling standard text probabilities.
    Utilizes negative log-likelihood evaluations against standard language models (GPT-2).
    """
    # Create the tokenized mapping arrays
    encodings = tokenizer(text, return_tensors='pt')
    max_length = model.config.n_positions
    stride = 512
    seq_len = encodings.input_ids.size(1)

    nlls = []
    prev_end_loc = 0
    # Rolling evaluate text structure chunk by chunk to bypass standard GPT length limits natively
    for begin_loc in range(0, seq_len, stride):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc  # Check relative trajectory length
        
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            # Access embedded entropy logic
            neg_log_likelihood = outputs.loss

        nlls.append(neg_log_likelihood)
        prev_end_loc = end_loc
        if end_loc == seq_len:
            break

    # Guard rail against completely empty evaluations
    if not nlls:
        return float('inf')
        
    try:
        # Perform final mathematical conversion against aggregated loss calculations
        ppl = torch.exp(torch.stack(nlls).mean()).item()
        return ppl
    except Exception:
        return float('inf')


def compute_ai_probability(paragraph):
    """
    Predict AI generative involvement primarily analyzing standard normalized perplexity.
    
    Returns:
        float: Scaled probability indicator [0.0, 1.0].
    """
    if not paragraph.strip() or not model or not tokenizer:
        return 0.0
        
    try:
        perplexity = compute_perplexity(paragraph)
        
        if perplexity == float('inf'):
            return 0.0
            
        # Core Probability Normalization Formula
        # Baseline threshold analysis mapping perplexity to empirical percentages. 
        # Typically AI output < 30. Naturally derived human text roughly > 75. 
        min_ppl = 25.0
        max_ppl = 120.0
        
        # Lower perplexity -> closer to exactly matching statistical models -> Highest AI confidence
        if perplexity <= min_ppl:
            return 0.99
            
        if perplexity >= max_ppl:
            return 0.01
            
        # Invert scale so lowering numbers equal rising probability factors
        mapped_prob = 1.0 - ((perplexity - min_ppl) / (max_ppl - min_ppl))
        return round(mapped_prob, 2)
    except Exception as e:
        print(f"Error establishing perplexity thresholds: {e}")
        return 0.0
