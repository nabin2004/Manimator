import requests
import json

def query_model(context, system_prompt, user_prompt, model="gemma3:270m", api_url="http://127.0.0.1:11434/api/generate"):
    """
    Calls the local Ollama API to generate a model response.

    Args:
        context (str): Conversation or background context.
        system_prompt (str): Instructions for the system.
        user_prompt (str): User input or query.
        model (str): Model name (default gemma3:270m).
        api_url (str): API endpoint (default local Ollama URL).

    Returns:
        str: Generated model response.
    """
    payload = {
        "model": model,
        "prompt": f"{context} ;; {system_prompt} ;; {user_prompt}"
    }

    try:
        resp = requests.post(api_url, json=payload, stream=True)
        resp.raise_for_status()  # Raise error for bad responses
    except requests.RequestException as e:
        return f"Request failed: {e}"

    response_text = ""
    for line in resp.iter_lines():
        if line:
            try:
                response_text += json.loads(line.decode()).get("response", "")
            except json.JSONDecodeError:
                continue

    return response_text

if __name__ == "__main__":
    context = "You are an assistant that explains concepts simply."
    system_prompt = "Answer clearly and concisely."
    user_prompt = "Explain what overfitting is in machine learning."

    response = query_model(context, system_prompt, user_prompt)
    print("Model Response:\n", response)