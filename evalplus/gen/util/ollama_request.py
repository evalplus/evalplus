import time
import ollama

def print_histogram(row_stats: dict) -> None:
    # Build histogram for lines repeated more than twice
    histogram = {
        "under_2": 0,
        "2_4": 0,
        "5_9": 0
    }
    # Add additional buckets from 10 to 199 in 10-number intervals
    for lower in range(10, 200, 10):
        bucket_label = f"{lower}_{lower+9}"
        histogram[bucket_label] = 0
    histogram["over_200"] = 0

    # Create a mapping of internal keys to display labels
    display_labels = {
        "under_2": "under 2",
        "2_4": "2-4",
        "5_9": "5-9",
        "over_200": "over 200"
    }
    # Add display labels for the 10-number interval buckets
    for lower in range(10, 200, 10):
        bucket_key = f"{lower}_{lower+9}"
        display_labels[bucket_key] = f"{lower}-{lower+9}"
    
    for row_hash, data in row_stats.items():
        count = data[0]
        if count <= 1:
            histogram["under_2"] += 1
        elif count <= 4:
            histogram["2_4"] += 1
        elif count <= 9:
            histogram["5_9"] += 1
        elif count <= 200:
            # Determine the appropriate 10-number bucket
            lower = (count // 10) * 10
            bucket_label = f"{lower}_{lower+9}"
            histogram[bucket_label] += 1
        else:
            histogram["over_200"] += 1

    labels = {}
    for bucket in histogram.keys():
        # Use display label if it exists, otherwise use the bucket as is
        labels[bucket] = display_labels.get(bucket, bucket)
    
    non_zero = [f"{labels[k]}: {v}" for k, v in histogram.items() if v > 0]
    print("# Amount of repeated rows: " + ", ".join(non_zero))


def make_request(
    model: str,
    prompt: str,
    max_tokens: int = -1,
    temperature: float = 1,
    num_ctx: int = None,
    n: int = 1,
    stream: bool = True,  # Default to streaming
    **kwargs
) -> ollama.ChatResponse:
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
        options=options,
        stream=stream
    )

def make_auto_request(*args, **kwargs) -> ollama.ChatResponse:
    ret = None
    model = kwargs.get("model")
    while ret is None:
        try:
            response = make_request(*args, **kwargs)
            if kwargs.get("stream", True):
                # Handle streaming response
                full_response = {"message": {"content": ""}}
                # Initialize an empty dictionary for row statistics
                row_stats = {}  # key: row_hash, value: [counter, row_length]
                current_row = ""
                last_stat_time = time.time()    # start timer for statistics
                for chunk in response:
                    if "message" in chunk:
                        chunk_content = chunk["message"]["content"]
                        full_response["message"]["content"] += chunk_content
                        current_row += chunk_content
                        # Process each complete row when a newline is found
                        while "\n" in current_row:
                            # Extract one complete row
                            row, current_row = current_row.split("\n", 1)
                            row_length = len(row)
                            if row_length > 1:
                                row_hash = hash(row)
                                # Update the statistics dictionary
                                if row_hash in row_stats:
                                    row_stats[row_hash][0] += 1
                                    # Check if this row has been repeated 200 or more times
                                    if row_stats[row_hash][0] >= 200:
                                        print(f"Breaking due to row being repeated {row_stats[row_hash][0]} times")
                                        ret = full_response
                                        return ret  # Exit the entire function immediately
                                else:
                                    row_stats[row_hash] = [1, row_length]
                            # Print out details for the completed row
                            print(f"Completed row: '{row}'")

                
                    # Every 60 seconds, display the statistics block
                    if time.time() - last_stat_time >= 60:
                        print("# 60 seconds Statistics histogram:", end="")
                        print_histogram(row_stats)
                        last_stat_time = time.time()  # reset timer

                # Optionally, handle any leftover incomplete row
                if current_row:
                    print(f"Incomplete row: '{current_row}'")

                print("### Final Statistics histogram:", end="")
                print_histogram(row_stats)

                ret = full_response
            else:
                ret = response

        except ollama.ResponseError as e:
            if e.status_code == 404:
                print(f"Error: Model '{model}' not found. Please check if the model is available.")
                raise Exception(f"Fatal error: {e.status_code}")
                time.sleep(5)
            elif e.status_code == 500:
                print(f"Error: Ollama is having a problem with Model '{model}' . Please check if the model is compatible with the current version of Ollama.")
                raise Exception(f"Fatal error: {e.status_code}")
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
