import torch
import os
os.environ['CUDA_VISIBLE_DEVICES'] = "1"
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from peft import LoraConfig, get_peft_model, PeftConfig, PeftModel
from transformers import TrainingArguments, Trainer
import string
import numpy as np
from datasets import Dataset as hf_Dataset
from collections import Counter
from trl import SFTConfig, SFTTrainer, DataCollatorForCompletionOnlyLM
import functools

class train_home_assistant_dataset(Dataset):
    def __init__(self,tokenizer,use_rag=False,dataset_type="train"):
        self.tokenizer= tokenizer
        self._data = []
        if use_rag:
            f = open("/home/slli/home_assistant/our_dataset/raw_data/rag_test_data.json", "r")
            self._data = json.loads(f.read())
            f.close()
        else:
            if dataset_type == "test":
                f = open("/home/slli/home_assistant/raw_data/new_test_data.jsonl", "r")
            elif dataset_type == "train":
                f = open("/home/slli/home_assistant/raw_data/new_train_data.jsonl", "r")
            elif dataset_type == "val":
                f = open("/home/slli/home_assistant/raw_data/new_valid_data.jsonl", "r")
            elif dataset_type == "sample":
                f = open("/home/slli/home_assistant/raw_data/single_normal.jsonl", "r")
            lines = f.readlines()
            f.close()
            f_home = open("/home/slli/home_assistant/raw_data/new_home_status_method.jsonl", "r")
            lines_home = f_home.readlines()
            home_status = {}
            for line in lines_home:
                data = json.loads(line)
                home_status[data["home_id"]] = {"home_status": data["home_status"], "method": data["method"]}
            f_home.close()
            examples = open("/home/slli/home_assistant/raw_data/example.txt", "r").read()
            system = open("/home/slli/home_assistant/raw_data/system.txt", "r").read()
            for i in range(len(lines)):
                case = lines[i]
                case = json.loads(case) 
                state_str, method_str = chang_json2str(home_status[case["home_id"]]["home_status"], home_status[case["home_id"]]["method"])
                case_input = "-------------------------------\n" + "Here are the user instructions you need to reply to.\n" + "<User instructions:> \n" + case["input"] + "\n<Machine instructions:>\n"
                home_status_case = "<home_state>\n  The following provides the status of all devices in each room of the current household, the adjustable attributes of each device, and the threshold values for adjustable attributes:"+ state_str + "\n" + "</home_state>\n"
                device_method_case = "<device_method>\n     The following provides the methods to control each device in the current household:"+ method_str + "\n" + "</device_method>\n"
                input = system + home_status_case + device_method_case + examples + case_input
                output = case["output"]
                output = output.replace("\'\'\'", "")
                output = output.replace(" ", "")
                output = "{" + output + "}"
                self._data.append({"input": input, "output": output})

    def __len__(self):
        return len(self._data)
    def __getitem__(self, idx):
        item = self._data[idx]
        input_text = [
            {"role":"system","content":item["input"]}
        ]
        output_text = item["output"]
        inputs_id = self.tokenizer.apply_chat_template(input_text,add_generation_prompt=True,tokenize=False)
        inputs_id += output_text
        
        return {"text": inputs_id}


def chang_json2str(state,methods):
    state_str = ""
    for room in state.keys():
        state_str += room + ":\n"
        if room == "VacuumRobot":
            state_str += "  state: " + state[room]["state"] + "\n"
            for attribute in state[room]["attributes"].keys():
                state_str += "  " + attribute + ": " + str(state[room]["attributes"][attribute]["value"])
                if "options" in state[room]["attributes"][attribute].keys():
                    state_str += " (options" + str(state[room]["attributes"][attribute]["options"]) + ")\n"
                elif "lowest" in state[room]["attributes"][attribute].keys():
                    state_str += " (range: " + str(state[room]["attributes"][attribute]["lowest"]) + " - " + str(state[room]["attributes"][attribute]["highest"]) + ")\n"
                else:
                    state_str += "\n"
        else:
            for device in state[room].keys():
                if device == "room_name":
                    continue
                else:
                    state_str += "  " + device + "\n"
                    
                    state_str += "    state: " + state[room][device]["state"] + "\n"
                    for attribute in state[room][device]["attributes"].keys():
                        state_str += "    " + attribute + ": " + str(state[room][device]["attributes"][attribute]["value"])
                        if "options" in state[room][device]["attributes"][attribute].keys():
                            state_str += " (options" + str(state[room][device]["attributes"][attribute]["options"]) + ")\n"
                        elif "lowest" in state[room][device]["attributes"][attribute].keys():
                            state_str += " (range: " + str(state[room][device]["attributes"][attribute]["lowest"]) + " - " + str(state[room][device]["attributes"][attribute]["highest"]) + ")\n"
                        else:
                            state_str += "\n"

    method_str = ""
    for method in methods:
        if method["room_name"] == "None":
            method_str += method["device_name"] + "." + method["operation"] + "("
        else:
            method_str += method["room_name"] + "." + method["device_name"] + "." + method["operation"] + "("
        if len(method["parameters"]) > 0:
            for parameter in method["parameters"]:
                method_str += parameter["name"] + ":" + parameter["type"] + ","
            method_str = method_str[:-1]
        method_str += ");"
    return state_str, method_str


lora_config = LoraConfig(
 r=16,
 lora_alpha=32,
 target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
 lora_dropout=0.1,
 bias="none",
 task_type="CAUSAL_LM"
)

def compute_max_length(hf_train_dataset):
    max_length = 0
    tokenizer = AutoTokenizer.from_pretrained("/home/slli/models/llama3-8b-Instruct")
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id
    for i in range(len(hf_train_dataset)):
        input_text = hf_train_dataset[i]["input"]
        encoding = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        max_length = max(max_length, encoding["input_ids"].shape[1])
    return max_length

def preprocess_logits_for_metrics(logits, labels):
    """
    Original Trainer may have a memory leak. 
    This is a workaround to avoid storing too many tensors that are not needed.
    """
    pred_ids = torch.argmax(logits, dim=-1)
    return pred_ids, labels

def sft_model(model_name):
    if model_name == "llama":
        model_id =  "/home/slli/models/llama3-8b-Instruct"
    elif model_name == "qwen":
        model_id = "/home/slli/models/Qwen2.5-7B-Instruct"
    elif model_name == "mistral":
        model_id = "/home/slli/models/Mistral-7B-Instruct-v0.3"
    elif model_name == "gemma":
        model_id = "/home/slli/models/Gemma-7B-Instruct-v0.3"
    print(torch.cuda.is_available())
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if model_name == "llama":
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
        tokenizer.padding_side = "right"
    train_dataset = train_home_assistant_dataset(tokenizer,dataset_type="train")
    val_dataset = train_home_assistant_dataset(tokenizer,dataset_type="val")
    
    train_data_list = [train_dataset[i]for i in range(len(train_dataset))]
    hf_train_dataset = hf_Dataset.from_list(train_data_list)
    val_data_list = [val_dataset[i] for i in range(len(val_dataset))]
    hf_val_dataset = hf_Dataset.from_list(val_data_list)
    print(hf_train_dataset)
    print(hf_val_dataset)

    model = AutoModelForCausalLM.from_pretrained(model_id,torch_dtype=torch.bfloat16,device_map="auto")
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    batch_size = 1
    training_args = SFTConfig(
        output_dir = "./model_output7",
        # do_eval=True,
        remove_unused_columns=True,
        # eval_strategy="steps",
        save_strategy="steps",
        # eval_steps = 100,
        learning_rate=1e-5,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=256,
        # per_device_eval_batch_size=batch_size,
        fp16=True,
        num_train_epochs=2,
        logging_steps=10,
        report_to="tensorboard",
        max_seq_length=4000,
        save_steps=100,
    )
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=hf_train_dataset,
        # eval_dataset=hf_val_dataset,
        # compute_metrics=functools.partial(compute_metrics, tokenizer=tokenizer),
        preprocess_logits_for_metrics=preprocess_logits_for_metrics,
        data_collator=DataCollatorForCompletionOnlyLM(
            response_template="<Machine instructions:>\n<|im_end|>\n<|im_start|>assistant\n",
            tokenizer=tokenizer,    
        )
    )
    
    trainer.train()
    trainer.save_model()



if __name__ == "__main__":

    sft_model("qwen")
