import time
import ollama


def print_histogram(row_stats: dict, header: str = "# Statistics histogram (ignoring counts of 2 or below):") -> None:
    histogram = {
        "over_100": 0,
        "90_99": 0,
        "80_89": 0,
        "70_79": 0,
        "60_69": 0,
        "50_59": 0,
        "40_49": 0,
        "30_39": 0,
        "20_29": 0,
        "10_19": 0,
        "5_9": 0,
        "under_5": 0,
    }
    for row_hash, data in row_stats.items():
        count = data[0]
        if count > 2:  # Only consider rows with more than 2 counts
            if count > 100:
                histogram["over_100"] += 1
            elif 90 <= count <= 99:
                histogram["90_99"] += 1
            elif 80 <= count <= 89:
                histogram["80_89"] += 1
            elif 70 <= count <= 79:
                histogram["70_79"] += 1
            elif 60 <= count <= 69:
                histogram["60_69"] += 1
            elif 50 <= count <= 59:
                histogram["50_59"] += 1
            elif 40 <= count <= 49:
                histogram["40_49"] += 1
            elif 30 <= count <= 39:
                histogram["30_39"] += 1
            elif 20 <= count <= 29:
                histogram["20_29"] += 1
            elif 10 <= count <= 19:
                histogram["10_19"] += 1
            elif 5 <= count <= 9:
                histogram["5_9"] += 1
            else:
                histogram["under_5"] += 1

    print(header)
    print(f"# Unique hashes with count over 100: {histogram['over_100']}")
    print(f"# Unique hashes with count between 90-99: {histogram['90_99']}")
    print(f"# Unique hashes with count between 80-89: {histogram['80_89']}")
    print(f"# Unique hashes with count between 70-79: {histogram['70_79']}")
    print(f"# Unique hashes with count between 60-69: {histogram['60_69']}")
    print(f"# Unique hashes with count between 50-59: {histogram['50_59']}")
    print(f"# Unique hashes with count between 40-49: {histogram['40_49']}")
    print(f"# Unique hashes with count between 30-39: {histogram['30_39']}")
    print(f"# Unique hashes with count between 20-29: {histogram['20_29']}")
    print(f"# Unique hashes with count between 10-19: {histogram['10_19']}")
    print(f"# Unique hashes with count between 5-9: {histogram['5_9']}")
    print(f"# Unique hashes with count under 5: {histogram['under_5']}")


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
                                else:
                                    row_stats[row_hash] = [1, row_length]
                            # Print out details for the completed row
                            # print(f"Completed row: '{row}'")
                     
                            # Print only the hash when row_length > 1 and count > 2
                            #if row_length > 1 and row_stats[row_hash][0] > 2:
                            #    print(f"Seen this row {row_stats[row_hash][0]} times,  Row hash: {row_hash}")

                    # Every 120 seconds, display the statistics block
                    if time.time() - last_stat_time >= 120:
                        print_histogram(row_stats, header="# Periodic Statistics histogram (ignoring counts of 2 or below):")
                        last_stat_time = time.time()  # reset timer

                # Optionally, handle any leftover incomplete row
                #if current_row:
                #    print(f"Incomplete row: '{current_row}'")

                # Final histogram block after processing all chunks
                print_histogram(row_stats, header="# Final Statistics histogram (ignoring counts of 2 or below):")

                ret = full_response
            else:
                ret = response

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
