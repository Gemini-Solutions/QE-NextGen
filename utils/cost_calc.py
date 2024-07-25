def calculate_cost(usage, model="gpt-3.5-turbo-1106"):
    # Token rates for different models
    token_rates = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-3.5-turbo-1106": {"prompt": 0.0010, "completion": 0.0020},
        "gpt-3.5-turbo-instruct": {"prompt": 0.0015, "completion": 0.0020},
        "ada v2": {"prompt": 0.0001, "completion": 0.0001},
        "gpt-4o": {"prompt": 0.0010, "completion": 0.015}
    }

    # Extracting token counts from the usage dictionary
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)

    # Selecting the appropriate model's token rates
    rates = token_rates.get(model, token_rates["gpt-3.5-turbo-1106"])

    # Special handling for the "ada v2" model
    if model == "text-embedding-ada-002":
        rates = token_rates["ada v2"]

    # Calculating the cost based on the token counts and rates
    prompt_cost = prompt_tokens * rates["prompt"]
    completion_cost = completion_tokens * rates["completion"]
    total_cost = prompt_cost + completion_cost

    return {
        "prompt_cost": prompt_cost/1000,
        "completion_cost": completion_cost/1000,
        "total_cost": total_cost/1000,
    }