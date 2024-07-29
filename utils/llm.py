from openai import OpenAI

def call_llm(
    conversation,
    temperature=1.0,
    max_tokens=None,
    user=None,
    stream=False,
    seed=None,
    response_format="text",
    model="gpt-3.5-turbo"
):

    client = OpenAI(api_key=os.environ.get("NextGenKey"),)

    # Define conversation with JSON system message
    if isinstance(conversation, str) and response_format == 'text':
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": conversation}
        ]
    elif isinstance(conversation, str) and response_format == 'json_object':
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": conversation}
        ]
    elif isinstance(conversation, list):
        messages = conversation
    else:
        print("Incorrect Conversation/Message format.")

    # Create chat completion
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        user=user,
        stream=stream,
        seed=seed,
        response_format={"type" : response_format}
    )

    # Print or return the generated poem
    response_generated = completion.choices[0].message
    finish_reason = completion.choices[0].finish_reason
    token_usage = completion.usage

    llm_output = {
        "response_generated": response_generated,
        "finish_reason": finish_reason,
        "token_usage": dict(token_usage)
    }

    return llm_output
