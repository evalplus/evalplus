import logging
import math
import re
import time
from datetime import datetime

import ollama

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def make_request(
    model: str,
    prompt: str,
    max_tokens: int = -1,
    temperature: float = 1,
    num_ctx: int = None,
    n: int = 1,
    stream: bool = True,  # Default to streaming
    timeout: float = 180.0,  # 3 minutes default timeout
    **kwargs,
) -> ollama.ChatResponse:
    start_time = time.time()
    logger.debug(f"[{datetime.now()}] Starting Ollama request for model {model}")
    logger.debug(f"[{datetime.now()}] Prompt length: {len(prompt)} characters")

    options = {
        "temperature": temperature,
        "num_predict": max_tokens,  # based on llama.cpp: -1 is infinite , -2 until context is filled
    }
    if num_ctx is not None:
        options[
            "num_ctx"
        ] = num_ctx  # Add Context length, if provided. should be a multiple of 8 and never larger than the trained context length (see ollama show modelname)

    ollama_chat = ollama.Client(timeout=timeout)
    try:
        response = ollama_chat.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options=options,
            stream=stream,
        )
        return response
    except Exception as e:
        logger.error(f"[{datetime.now()}] Error in Ollama request: {str(e)}")
        raise


def unique_word_ratio(text):
    # Remove noise characters, normalize whitespace
    text = re.sub(r"[-_#~|─┼\r\n]", " ", text)  # remove styling garbage
    text = re.sub(r"\s+", " ", text).strip()  # collapse whitespace
    tokens = text.split(" ")  # split by space (or tab if needed)
    if not tokens:
        return 0.0
    else:
        unique_words = set(tokens)
        logger.debug(
            f"[{datetime.now()}] unique_word_ratio-testing with {len(text)} characters text, which has {len(tokens)} words(tokens), and {len(unique_words)} unique words"
        )
        return len(unique_words) / len(tokens)


def make_auto_request(*args, **kwargs) -> ollama.ChatResponse:
    ret = None
    chunk_buffer = ""  # Buffer for checking repetitions without newlines

    model = kwargs.get("model")
    timeout = kwargs.get("timeout", 180)
    while ret is None:
        request_start_time = time.time()
        try:
            response = make_request(*args, **kwargs)
            if kwargs.get("stream", True):
                full_response = {"message": {"content": ""}}
                min_buffer_size = 6000  # Minimum characters to start checking
                request_returns_characters = 0  # will be reset in intervals and will be used to calculate the average response speed
                repeating_loop_penalty_counter = 0
                last_stat_time = time.time()
                last_chunk_time = time.time()
                logger.debug(
                    f"[{datetime.now()}] elapsed time between make_request and now: {last_stat_time - request_start_time} seconds"
                )
                for chunk in response:
                    current_time = time.time()
                    elapsed_time = current_time - last_chunk_time
                    if elapsed_time > 10:
                        logger.debug(
                            f"[{datetime.now()}] inside for-chunk-loop: elapsed_time over 10 seconds: {elapsed_time:.2f} seconds"
                        )
                    if elapsed_time > timeout:
                        logger.error(
                            f"[{datetime.now()}] inside for-chunk-loop: Request timeout after {elapsed_time:.2f} seconds"
                        )
                        raise TimeoutError(
                            f"Ollama request timeout after {timeout} seconds"
                        )

                    if "message" in chunk:
                        chunk_content = chunk["message"]["content"]
                        full_response["message"]["content"] += chunk_content
                        chunk_buffer += chunk_content
                        request_returns_characters += len(chunk_buffer.encode("utf-8"))
                        last_chunk_time = time.time()

                        if len(chunk_buffer) >= min_buffer_size:
                            logger.debug(
                                f"[{datetime.now()}] Received {len(chunk_buffer)} characters (total: {request_returns_characters})"
                            )
                            logger.debug(f"{chunk_buffer}")

                            # Check for repetitions using unique word ratio when buffer is large enough
                            penalty_counter = 2  # default penalty counter
                            ratio = unique_word_ratio(
                                chunk_buffer
                            )  # calulation of the ratio of unique words in the buffer
                            if (
                                ratio < 0.15
                            ):  # You can adjust this threshold, but 0.15 is a throughly tested threshold
                                repeating_loop_penalty_counter += 1
                                logger.warning(
                                    f"[{datetime.now()}] Detected low uniqueness (ratio: {ratio:.3f}) in recent response. Penalty counter: {repeating_loop_penalty_counter} of {penalty_counter}"
                                )

                                if repeating_loop_penalty_counter >= penalty_counter:
                                    logger.warning(
                                        f"[{datetime.now()}] Canceling request streaming due to excessive repetition (uniqueness ratio: {ratio:.3f})"
                                    )
                                    ret = full_response
                                    logger.debug(
                                        f"[{datetime.now()}] Size of ret content: {len(ret['message']['content'])}"
                                    )
                                    return ret
                            else:
                                repeating_loop_penalty_counter = 0  # Reset the penalty counter because the ratio going higher again.
                            chunk_buffer = ""  # Reset the buffer

                    # Every 60 seconds, display the statistics block and reset the request_returns_characters counter
                    if time.time() - last_stat_time >= 60:
                        logger.debug(
                            f"[{datetime.now()}] 60 seconds Statistics histogram: After {(time.time() - last_stat_time):.2f} seconds, {request_returns_characters} characters, {request_returns_characters / (time.time() - last_stat_time):.2f} char/s, {request_returns_characters / (time.time() - last_stat_time) * 60:.2f} char/min."
                        )
                        request_returns_characters = (
                            0  # reset measured message response chunk
                        )
                        last_stat_time = time.time()  # reset timer

                # Optionally, handle any leftover incomplete row
                if len(chunk_buffer) > 0:
                    # logger.debug(f"[{datetime.now()}] final chunk_buffer: '{chunk_buffer}'")
                    logger.debug(
                        f"[{datetime.now()}] elapsed time between make_request and finaly returning the response: {time.time() - request_start_time} seconds"
                    )
                    ret = full_response
            else:
                # If stream is False, return the response immediately
                ret = response

        except ollama.ResponseError as e:
            if e.status_code == 404:
                logger.error(
                    f"[{datetime.now()}] Model '{model}' not found. Please check if the model is available."
                )
                raise Exception(f"Fatal error: {e.status_code}")
            elif e.status_code == 500:
                logger.error(
                    f"[{datetime.now()}] Ollama is having a problem with Model '{model}' . Please check if the model is compatible with the current version of Ollama."
                )
                raise Exception(f"Fatal error: {e.status_code}")
            else:
                logger.error(
                    f"[{datetime.now()}] Ollama API Error: {e.error}, Code: {e.status_code}"
                )
                time.sleep(5)

        except ConnectionError:
            logger.warning(
                f"[{datetime.now()}] Warning: Unable to connect to Ollama. Retrying..."
            )
            time.sleep(5)

        except TimeoutError:
            logger.warning(
                f"[{datetime.now()}] Warning: Request timed out. Retrying..."
            )
            time.sleep(5)

        except ValueError as ve:
            logger.error(f"[{datetime.now()}] Error: Invalid input - {ve}")

        except Exception as e:
            logger.error(f"[{datetime.now()}] Unexpected error: {e}")
            time.sleep(5)
    logger.debug(
        f"[{datetime.now()}] Size of ret content: {len(ret['message']['content'])}"
    )
    logger.debug(f"[{datetime.now()}] Exiting with response due to ret is not None")
    return ret
