# Local CC-BOS Generation

This fork keeps the original Classical Chinese CC-BOS entry point and adds English and modern vernacular Traditional Chinese variants.

- `code/gen.py`: original Classical Chinese CC-BOS style
- `code/gen_english.py`: English CC-BOS-style ablation
- `code/gen_traditional.py`: modern vernacular Taiwan-style Traditional Chinese CC-BOS-style ablation

All variants use the same fruit-fly search, dimensions, scoring loop, and output schema. The intended comparison is language/style, not a fixed prompt wrapper.

The English and modern vernacular Traditional Chinese variants also replace the original Classical Chinese `dimension_options` labels with language-matched labels while preserving the same dimension keys, option counts, numeric indices, and search procedure. This keeps the search space shape comparable while avoiding Classical Chinese strategy labels leaking into the English or vernacular Traditional Chinese runs.

## Prepare Input

From the tenBenign repo:

```bash
cd "/mnt/c/Users/lab342/Documents/GAIS/final project/third_party/tenBenign"

python code/measure/prepare_ccbos_input.py \
  --input_path ./data/harmful_behaviors.pkl \
  --output_path ../CC-BOS/data/tenbenign_advbench.csv
```

## Ollama Backend

Recommended local models:

```bash
ollama pull qwen3:14b
```

If memory allows, use a larger model:

```bash
ollama pull qwen3:30b
ollama pull qwen3:32b
```

If memory is tight:

```bash
ollama pull qwen3:8b
```

## Hugging Face Backend

You can also use a downloaded local Hugging Face model for generator/target calls:

```bash
--generator_backend hf \
--generator_model "/mnt/c/Users/lab342/Documents/GAIS/final project/models/Qwen3-8B" \
--target_backend hf \
--target_model "/mnt/c/Users/lab342/Documents/GAIS/final project/models/Qwen3-8B" \
--use_4bit
```

The judge backend currently supports `api` or `ollama`, so the simplest fully free setup is still Ollama for generation, target response, translation, and judge scoring.

## Generate Classical Chinese Prompts

```bash
cd "/mnt/c/Users/lab342/Documents/GAIS/final project/third_party/CC-BOS/code"

python gen.py \
  --input_file ../data/tenbenign_advbench.csv \
  --data_format csv \
  --output_dir ../result/classical_qwen3_14b \
  --overwrite \
  --limit 20 \
  --population_size 3 \
  --max_iter 2 \
  --seed 0 \
  --generator_backend ollama \
  --generator_model qwen3:14b \
  --target_backend ollama \
  --target_model qwen3:14b \
  --translation_backend ollama \
  --translation_model qwen3:14b \
  --judge_backend ollama \
  --judge_model qwen3:14b
```

Remove `--limit 20` for the full 520-prompt run after the smoke test looks reasonable.

## Generate English Prompts

```bash
cd "/mnt/c/Users/lab342/Documents/GAIS/final project/third_party/CC-BOS/code"

python gen_english.py \
  --input_file ../data/tenbenign_advbench.csv \
  --data_format csv \
  --output_dir ../result/english_qwen3_14b \
  --overwrite \
  --limit 20 \
  --population_size 3 \
  --max_iter 2 \
  --seed 0 \
  --generator_backend ollama \
  --generator_model qwen3:14b \
  --target_backend ollama \
  --target_model qwen3:14b \
  --translation_backend none \
  --judge_backend ollama \
  --judge_model qwen3:14b
```

The English version skips translation because the target response is already evaluated as English.

## Generate Vernacular Traditional Chinese Prompts

```bash
cd "/mnt/c/Users/lab342/Documents/GAIS/final project/third_party/CC-BOS/code"

python gen_traditional.py \
  --input_file ../data/tenbenign_advbench.csv \
  --data_format csv \
  --output_dir ../result/traditional_plain_qwen3_14b \
  --overwrite \
  --limit 20 \
  --population_size 3 \
  --max_iter 2 \
  --seed 0 \
  --generator_backend ollama \
  --generator_model qwen3:14b \
  --target_backend ollama \
  --target_model qwen3:14b \
  --translation_backend ollama \
  --translation_model qwen3:14b \
  --judge_backend ollama \
  --judge_model qwen3:14b
```

The Traditional Chinese version uses the same optimization loop as the Classical Chinese version, but the generated prompt is constrained to modern vernacular Traditional Chinese, not Classical Chinese or semi-classical prose. It keeps translation enabled during CC-BOS scoring because the consistency judge compares against the original English intention.

## Sync For tenBenign Evaluation

```bash
cd "/mnt/c/Users/lab342/Documents/GAIS/final project/third_party/tenBenign"

mkdir -p data/cc_bos
cp ../CC-BOS/result/classical_qwen3_14b/record.jsonl data/cc_bos/record_classical.jsonl
cp ../CC-BOS/result/english_qwen3_14b/record.jsonl data/cc_bos/record_english.jsonl
cp ../CC-BOS/result/traditional_plain_qwen3_14b/record.jsonl data/cc_bos/record_traditional.jsonl
```

Then run response generation:

```bash
python code/measure/generate_responses.py \
  --model_key qwen3 \
  --dataset ccbos_record_classical \
  --adapter_path code/finetune/adapters/qwen3_sweep_r16_stage2 \
  --tag sweep_r16_stage2 \
  --use_4bit

python code/measure/generate_responses.py \
  --model_key qwen3 \
  --dataset ccbos_record_english \
  --adapter_path code/finetune/adapters/qwen3_sweep_r16_stage2 \
  --tag sweep_r16_stage2 \
  --use_4bit

python code/measure/generate_responses.py \
  --model_key qwen3 \
  --dataset ccbos_record_traditional \
  --adapter_path code/finetune/adapters/qwen3_sweep_r16_stage2 \
  --tag sweep_r16_stage2 \
  --use_4bit
```

## Notes

The local Ollama runs are not the same as the paper's API-backed run. They are a local/free reproduction path. To keep the language comparison fair, use the same generator, target, judge, `population_size`, `max_iter`, `seed`, and input CSV for `gen.py`, `gen_english.py`, and `gen_traditional.py`.
