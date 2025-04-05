import time
import ollama
import math


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
                full_response = {"message": {"content": ""}}
                row_stats = {}  # key: row_hash, value: [counter, row_length]
                recent_rows = []  # list to track ALL recent rows (including duplicates)
                current_row = ""
                request_start_time = time.time()    # Time when the request was sent
                request_returns_characters = 0      # Number of characters returned from the so far
                last_stat_time = time.time()
                
                for chunk in response:
                    if "message" in chunk:
                        chunk_content = chunk["message"]["content"]                        
                        request_returns_characters += len(chunk_content) ## add a statitics on how many new characters were returned in the last 60 seconds

                        full_response["message"]["content"] += chunk_content
                        current_row += chunk_content
                        
                        while "\n" in current_row:
                            row, current_row = current_row.split("\n", 1)
                            row_length = len(row)
                            if row_length > 1:
                                row_hash = hash(row)
                                
                                # Track this row in recent_rows regardless of uniqueness
                                recent_rows.append(row_hash)
                                if len(recent_rows) > 100:
                                    # Remove oldest row
                                    oldest_hash = recent_rows.pop(0)
                                    # Decrease counter for the removed hash
                                    if oldest_hash in row_stats:
                                        row_stats[oldest_hash][0] -= 1
                                        # If counter reaches 0, remove from stats
                                        if row_stats[oldest_hash][0] <= 0:
                                            del row_stats[oldest_hash]
                                
                                # Update stats for current row
                                if row_hash in row_stats:
                                    row_stats[row_hash][0] += 1
                                else:
                                    row_stats[row_hash] = [1, row_length]
                                
                                # Check for repetition threshold
                                if (sum(row_stats[k][0] * math.log(row_stats[k][0]) for k in row_stats) / (len(recent_rows))) >= 1.6:
                                    print(f"#### Breaking due to row being repeated {row_stats[row_hash][0]} times / high Entropy-Based Repetition Score.")
                                    print(f"total unique rows {len(row_stats)}, recent row count: {len(recent_rows)}")
                                    print("# Last known Statistics histogram:", end="")
                                    print_histogram(row_stats)
                                    entropy_based_repetition_density_score = sum(row_stats[k][0] * math.log(row_stats[k][0]) for k in row_stats) / (len(recent_rows))
                                    print(f"#_# Entropy-Based Repetition Density Score: {entropy_based_repetition_density_score:.4f}")


                                    ret = full_response
                                    return ret
                            
                            print(f"Completed row: '{row}'")
                
                    # Every 60 seconds, display the statistics block
                    if time.time() - last_stat_time >= 60:
                        print(f"#_# 60 seconds Statistics histogram: {request_returns_characters} characters, {request_returns_characters / (time.time() - last_stat_time):.2f} char/s, {request_returns_characters / (time.time() - last_stat_time) * 60:.2f} char/min.")
                        request_returns_characters = 0 # reset measured message response chunk 

                        print_histogram(row_stats)
                        #Build a Entropy-Based Repetition Density Score for row_stats
                        entropy_based_repetition_density_score = sum(row_stats[k][0] * math.log(row_stats[k][0]) for k in row_stats) / (len(recent_rows))

                        print(f"#_# Entropy-Based Repetition Density Score: {entropy_based_repetition_density_score:.4f}")
                        
                        last_stat_time = time.time()  # reset timer

                # Optionally, handle any leftover incomplete row
                if current_row:
                    print(f"final row: '{current_row}'")

                print("### Final Statistics histogram:", end="")
                print_histogram(row_stats)
                print(f"### total unique rows {len(row_stats)}, recent row count: {len(recent_rows)}")
                #Build a Entropy-Based Repetition Density Score for row_stats
                entropy_based_repetition_density_score = sum(row_stats[k][0] * math.log(row_stats[k][0]) for k in row_stats) / (len(recent_rows))
                print(f"### Entropy-Based Repetition Density Score: {entropy_based_repetition_density_score:.4f}")

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
