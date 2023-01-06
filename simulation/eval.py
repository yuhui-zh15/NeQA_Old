# Code adapted from https://huggingface.co/docs/transformers/v4.25.1/en/tasks/language_modeling#language-modeling

# - Evaluation:
#     - Task 1: sentiment classification. For test set, evaluate accuracy of “this is _”.
#     - Task 2: negation understanding. For test set, evaluate accuracy of “this is not _”.
# - Plot:
#     - Matrix: x-axis: model size; y-axis: X%; cell: task 1/2 accuracy


prompt = "Somatic hypermutation allows the immune system to"
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
inputs = tokenizer(prompt, return_tensors="pt").input_ids
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("my_awesome_eli5_clm-model2")
outputs = model.generate(
    inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95
)
print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
