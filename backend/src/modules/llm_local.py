from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextStreamer
import torch

model_id = "Qwen/Qwen2.5-1.5B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16, # или bfloat16 если карта RTX 30xx/40xx
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="cuda"
)
tokenizer = AutoTokenizer.from_pretrained(model_id)
print(f"Модель загружена на устройство: {model.device}")
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

while True:
    print('\n'+'_'*80)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    prompt = input()
    messages = [
    {"role": "system", "content": "Ты полезный ассистент."},
    {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    # --- ИСПРАВЛЕНИЕ: Передача **inputs (включая attention_mask) ---
    model.generate(
        **inputs,
        streamer=streamer,  # <--- ВОТ ЭТО ГЛАВНОЕ ИЗМЕНЕНИЕ
        max_new_tokens=512,
        pad_token_id=tokenizer.pad_token_id
    )
