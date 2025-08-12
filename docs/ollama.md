# Ollama backend quirks

Using [Ollama](https://www.ollama.com/) as your LLM backend may need more care than relying on commercial llm as a service backends.
Here are a few hints and best practices

## Ollama daemon parameters

To ensure that ollama is properly tuned, consult the [ollama sourcecode](https://github.com/ollama/ollama/blob/main/envconfig/config.go). Since the code is well documented, it is much better than relying on blog posts or other data sources. Also consult [llama.cpp sourcecode](https://github.com/ggml-org/llama.cpp), on which ollama is based on. It is also helpful to understand some concepts behind ollama parameters.

OLLAMA_MAX_LOADED_MODELS defines how many models can be loaded into memory simultaneously. This parameter helps prevent out-of-memory issues by limiting the number of concurrent models that Ollama will keep loaded. Setting this value too high may cause system instability, while setting it too low may cause more frequent model loading/unloading operations.

OLLAMA_NUM_PARALLEL defines the number of concurrent requests that Ollama can process simultaneously, which directly impacts the system's ability to handle multiple API calls at once. Setting this value too high may lead to resource contention and degraded performance, while setting it too low may result in request queuing and increased response times. The default value is typically set to 1 or 2 for stability, but can be increased based on your system's available resources and workload requirements.

OLLAMA_KEEP_ALIVE specifies how long Ollama will keep a model loaded in memory after its last use before unloading it. This parameter helps balance memory usage by automatically freeing up resources from inactive models while avoiding the overhead of frequently reloading commonly used models. The default value is typically 5 minutes, but can be adjusted based on your usage patterns and available system memory.

OLLAMA_CONTEXT_LENGTH defines the default length num_ctx, which ollama uses as a default, when in the modelfile does not include a num_ctx or num_ctx is not sent from the client as a parameter. This parameter controls the maximum number of tokens that can be processed in a single request, affecting both the model's memory usage and its ability to handle longer sequences of text. Setting this value appropriately is crucial for balancing between the model's context understanding capabilities and system resource consumption.

OLLAMA_NUM_PARALLEL defines the maximum number of concurrent requests that can be processed simultaneously. This parameter directly impacts system performance and resource utilization, with higher values potentially leading to increased memory usage and CPU load. The default value is typically set to 1 or 2 for stability, but can be adjusted based on your system's capabilities. Since you are just running this evaluation, keep it at 1 to ensure best usage of GPU memory, especially when you are using multiple GPUs.

OLLAMA_LOAD_TIMEOUT specifies the maximum time allowed for loading a model before timing out. This parameter helps prevent system hangs when loading large models or when system resources are constrained. The default timeout is usually set to 15 minutes, but can be adjusted based on your model sizes and system performance. If you are mostly using CPU memory or very slow gpu connections, the loading time can be quite significant on large models. Keep an eye on the ollama debug output.

OLLAMA_DEBUG enables detailed logging and debugging information for troubleshooting Ollama operations. When enabled, it provides extensive information about model loading, request processing, and system state that can be valuable for diagnosing issues. This parameter should typically be disabled in production environments unless actively debugging an issue.

OLLAMA_HOST defines the network interface and port that Ollama will listen on for incoming requests. For local development and testing, using 127.0.0.1:11434 is recommended as it only allows connections from the same machine. Setting this to 0.0.0.0:11434 will make Ollama accessible from any network interface on the computer, which could pose security risks if your machine is accessible from other networks.

Here is an example of
/etc/systemd/system/ollama.service
```shell
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
Environment="OLLAMA_NUM_PARALLEL=2"
Environment="OLLAMA_MAX_LOADED_MODELS=2"
Environment="OLLAMA_KEEP_ALIVE=30m"
Environment="OLLAMA_LOAD_TIMEOUT=15m0s"
Environment="OLLAMA_DEBUG=1"
Environment="OLLAMA_ORIGINS=*"

[Install]
WantedBy=default.target
```


> [!Tip]
> Inside evalplus/gen/util/ollama_request.py, you could probably fine tune:
> connection (receive-) timeouts:
> If your system is extremly slow, it could help to add longer timeouts. However the default timing is tested and proofed working quite well on several systems.
> Repetion-Detection:
> The detection for repeating texts based on a simple sliding window check of normalized repeating words in comparison with the overall amount of words. This method shown to be very effective of ollama models.
> There are two ways to fine-tune the repetition detection: The size ( min_buffer_size ) of the sliding window (content_buffer) and
