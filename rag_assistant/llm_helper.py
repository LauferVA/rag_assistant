import logging
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch

logger = logging.getLogger(__name__)

model_name = "mistralai/Mistral-7B-Instruct"
try:
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    device = 0 if torch.cuda.is_available() else -1
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)
except Exception as e:
    logger.error("Error initializing LLM: %s", e)
    raise e

def generate_completion(prompt, max_length=200, num_return_sequences=1):
    """
    Generate text completion from the given prompt.
    
    :param prompt: The prompt string that includes context and instructions.
    :param max_length: Maximum length of the generated text.
    :param num_return_sequences: Number of completions to generate.
    :return: The generated completion text.
    """
    logger.info("Generating completion with prompt of length %d", len(prompt))
    try:
        outputs = generator(prompt, max_length=max_length, num_return_sequences=num_return_sequences)
        generated_text = outputs[0]['generated_text']
        # Remove the prompt from the generated text (if desired)
        completion = generated_text[len(prompt):].strip()
        logger.debug("Generated completion: %s", completion)
        return completion
    except Exception as e:
        logger.error("Error during text generation: %s", e)
        return "Error generating completion."
