import time
import ollama

def make_request(
    model: str,
    prompt: str,
    max_tokens: int = -1,
    temperature: float = 1,
    num_ctx: int = None,
    n: int = 1,
    **kwargs
) -> ollama.ChatResponse :
    options = {
    "temperature": temperature,
    "num_predict": max_tokens   # based on llama.cpp: -1 is infinite , -2 until context is filled
    }
    if num_ctx is not None: 
        options["num_ctx"] = num_ctx  # Add Context length, if provided. should be a multiple of 8 and never larger than the trained context length (see ollama show modelname)

    #print(f"num_ctx in ollama is {num_ctx}, num_predict is {max_tokens}, temperature is {temperature}")
    return ollama.chat(
           model=model,
           messages=[{"role": "user", "content": prompt}],
           options=options
           )

def make_auto_request(*args, **kwargs) -> ollama.ChatResponse:
    ret = None
    model = kwargs.get("model")
    while ret is None:
        try:
            ret = make_request(*args, **kwargs)
        except ollama.ResponseError as e:
            if e.status_code == 404:
                print(f"Error: Model '{model}' not found. Please check if the model is available.")
                time.sleep(5)
            else:
                print(f"Ollama API Error: {e.error}, Code: {e.status_code}")
                time.sleep(5)

        except ConnectionError:
            print("Error: Unable to connect to Ollama. Retrying...")
            time.sleep(5)

        except TimeoutError:
            print("Error: Request timed out. Retrying...")
            time.sleep(5)

        except ValueError as ve:
            print(f"Error: Invalid input - {ve}")

        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)

    return ret
