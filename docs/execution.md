# Program Execution

LLM solutions are regarded as **failed** on timeout and OOM etc.

## Time Limits

We set the timeout $T=\max(T_{base}, T_{gt}\times k)$ where:

- $T_{base}$ is the minimal timeout (configurable by `--min-time-limit`; default to 4s);
- $T_{gt}$ is the runtime of the ground-truth solutions (achieved via profiling);
- $k$ is a configurable factor `--gt-time-limit-factor` (default to 4);

If your machine is too slow and you are getting high-variance results, try to use larger $k$ and $T_{base}$.

## Memory Limits

- **Default behavior**: The default memory limit per process is `min(4GB, system_maximum)`.
- Environment variable `EVALPLUS_MAX_MEMORY_BYTES`:
  - `-1` means no limit.
  - Otherwise, the limit is set to the specified value in bytes.

Related discussion threads:

- https://github.com/evalplus/evalplus/pull/225

## Parallelism

You are **NOT** encouraged to make your test-bed over stressed while running evaluation.
For example, using `--parallel 64` on a 4-core machine or doing something else during evaluation are bad ideas...

## Tips for Fast Evaluation

If you do greedy decoding where there is only one sample for each task, the evaluation should take just a few seconds.
When running 200 samples x 164 tasks x ~700+ tests, it can take around 2-10 minutes by using `--parallel 64` and `--test-details`.
Here are some tips to speed up the evaluation:

- Use `--parallel $(nproc)`
- Do **NOT** use `--test-details` if you just want to quickly get pass@k as `--test-details` will run all tests (700+ on average for each task), while without `--test-details` the testing for a sample stops immediately when it fails the first test.
- Use our pre-evaluated results (see [LLM-generated code](#-LLM-generated-code))
- Use HumanEval+ Mini

</div>
</details>

> [!Tip]
>
> 🚀 **Try out `HumanEvalPlus-Mini`!** which selects a _minimal_ set of additional tests with the highest quality, achieving almost the same effectiveness of the full version. Just add a **`--mini`** flag, it can run 23+% faster! (even faster if you evaluate all tests without fail-stop with `--test-details`).
>
> ```bash
> docker run -v $(pwd):/app ganler/evalplus:latest --dataset humaneval --samples samples.jsonl --mini
> # ...Or locally ⚠️
> # evalplus.evaluate --dataset humaneval --samples samples.jsonl --mini
> ```
