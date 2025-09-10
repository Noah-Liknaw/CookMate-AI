from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class LocalLLM:
    def __init__(self, model_name="google/flan-t5-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate(self, prompt: str, max_new_tokens=800):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,             
            do_sample=True,
            top_p=0.9,
            temperature=0.7
        )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
