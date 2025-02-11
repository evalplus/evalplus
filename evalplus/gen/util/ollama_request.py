import time
import ollama

def make_request(model: str, prompt: str, max_tokens: int = -1, temperature: float = 1, num_ctx: int = None, **kwargs):
    options = {"temperature": temperature, 
               "num_predict": max_tokens   # based on llama.cpp: -1 is infinite , -2 until context is filled
	       }
    if num_ctx is not None: 
        options["num_ctx"] = num_ctx  # Add Context length, if provided. should be a multiple of 8 and never larger than the trained context length (see ollama show modelname)

    #print(f"num_ctx in ollama is {num_ctx}, num_predict is {max_tokens}, temperature is {temperature}")
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options=options
        )
        return response["message"]["content"] if "message" in response else ""
    except Exception as e:
        print(f"Request failed: {e}")
        return ""

def make_auto_request(*args, **kwargs):
    ret = None
    while ret is None:
        try:
            ret = make_request(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    return ret
