import time
from huggingface_hub import InferenceClient

# Declare global history
history = []

def sanitize_input(text):
    # Remove any potentially problematic characters
    problematic_chars = ['<', '>', '\\']
    for char in problematic_chars:
        text = text.replace(char, '')
    return text

def format_prompt(message):
    prompt = "<s>"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

def generate_response(client, prompt, temperature=0.9, max_new_tokens=256, 
                     top_p=0.95, repetition_penalty=1.2):
    
    temperature = max(float(temperature), 1e-2)
    
    generate_kwargs = {
        'temperature': temperature,
        'max_new_tokens': max_new_tokens,
        'top_p': float(top_p),
        'repetition_penalty': repetition_penalty,
        'do_sample': True,
        'seed': 42
    }

    max_retries = 3
    accumulated_output = ""
    
    for attempt in range(max_retries):
        try:
            # Only print newline and "Mistral:" for first attempt
            if attempt == 0:
                print("\nMistral: ", end='', flush=True)
            
            # Modify the prompt based on history
            continuation_prompt = format_prompt(prompt)
            
            stream = client.text_generation(
                continuation_prompt,
                **generate_kwargs,
                stream=True,
                details=True,
                return_full_text=False
            )
            
            current_attempt_output = ""
            for response in stream:
                token_text = response.token.text
                
                if '<unk>' in token_text:
                    if current_attempt_output:
                        accumulated_output += current_attempt_output
                        break
                    raise Exception("Unknown token detected")
                
                current_attempt_output += token_text
            
            # If we completed without <unk>, add the current attempt and return
            if '<unk>' not in current_attempt_output:
                accumulated_output += current_attempt_output
                print()  # Add newline at end
                return accumulated_output
                
        except Exception as e:
            if attempt < max_retries - 1:
                # Don't print retry message, just silently retry
                client = reset_client(client)
                time.sleep(0.5)
            else:
                if accumulated_output:
                    print()  # Add newline
                    return accumulated_output
                else:
                    print("\nI apologize, but I'm having trouble generating a response. Please try rephrasing your question.")
                    return ""

    return accumulated_output if accumulated_output else ""

def reset_client(client):
    try:
        return InferenceClient(
            "mistralai/Mistral-7B-Instruct-v0.3", 
            token="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"
        )
    except Exception as e:
        print(f"Error reinitializing client: {e}")
        return client  # Return the original client if reset fails

def check_length(user_input, params):
    user_input = user_input.lower()
    user_len = len(user_input)
    tokens = 50
    
    # Adjust max_new_tokens based on user input
    if user_len > 50 and user_len <= 100:
        tokens += 45
    elif user_len > 100 and user_len <= 200:
        tokens += 75
    elif user_len > 200 and user_len <= 300:
        tokens += 90
    elif user_len > 300 and user_len <= 400:
        tokens += 105
    elif user_len > 400 and user_len <= 500:
        tokens += 125
    elif user_len > 500 and user_len <= 600:
        tokens += 150
    elif user_len > 600 and user_len <= 700:
        tokens += 175
    elif user_len > 700 and user_len <= 800:
        tokens += 200
    elif user_len > 800 and user_len <= 900:
        tokens += 225
    elif user_len > 900 and user_len <= 1000:
        tokens += 250

    if "explain" in user_input and "detail" in user_input:
        tokens += 115
    elif "explain" in user_input and "difference between" in user_input:
        tokens += 215
    elif "explain" in user_input or "discuss" in user_input:
        tokens += 75
    elif "explain" in user_input and "detail" in user_input:
        tokens
    elif "if" in user_input:
        tokens += 80
    elif "list" in user_input or "provide" in user_input:
        tokens += 100
    elif "summarize" in user_input:
        tokens += 75
    elif "describe" in user_input or "propose" in user_input:
        tokens += 75
    elif "what were" in user_input or "what was" in user_input:
        tokens += 120
    elif "what is" in user_input or "who is" in user_input:
        tokens += 50
    elif "short story" in user_input or "story" in user_input:
        tokens += 305
    elif "long story" in user_input:
        tokens += 605
    elif "create" in user_input and "recipe" in user_input:
        tokens += 800
    elif "create" in user_input:
        tokens += 100
    elif "poem" in user_input:
        tokens += 200

    # Cap the maximum tokens
    params['max_new_tokens'] = min(tokens, 1024)

    # Inform user about token adjustment
    #print(f"Response length adjusted to {params['max_new_tokens']} tokens based on your request.")

def clean_response(response):
    # Clean up incomplete bullet points or numbered lists
    lines = response.split('\n')
    if lines:
        last_line = lines[-1].strip()
        # Check if the last line starts with a bullet point or number but isn't complete
        if (last_line.startswith('- ') or last_line.startswith('* ') or 
            (last_line[0].isdigit() and '. ' in last_line)) and len(last_line) < 10:
            lines = lines[:-1]
    
    # Clean up incomplete sentences
    response = '\n'.join(lines)
    for punct in ['.', '!', '?']:
        if response.rfind(punct) != -1:
            last_punct_index = response.rfind(punct)
            if last_punct_index < len(response) - 1:
                next_char = response[last_punct_index + 1:]
                if not any(next_char.rstrip().endswith(p) for p in ['.', '!', '?']):
                    response = response[:last_punct_index + 1]
    
    return response.strip()

def generate(user_input):
    # Initialize the client
    client = InferenceClient(
        "mistralai/Mistral-7B-Instruct-v0.3", 
        token="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"
    )
    
    # Default parameters
    params = {
        'temperature': 0.5,
        'max_new_tokens': 50,
        'top_p': 0.8,
        'repetition_penalty': 1.1
    }
    
    run = True
    while run is True:
        try:
            # Prompt user for input
            user_input = sanitize_input(user_input.strip())
            
            # Append the user input to the history
            history.append((user_input, ''))  # Add an empty bot response placeholder
            
            check_length(user_input, params)

            response = generate_response(client, user_input, **params)
            #print(response)
            
            # Store the bot's response in history
            if response:
                history[-1] = (user_input, response)  # Update the last entry with the bot's response
            
            return response.replace('</s>', '')
        
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Resetting client and history...\n")
            client = reset_client(client)
            history.clear()  # Clear history if an error occurs
            iteration_count = 0
