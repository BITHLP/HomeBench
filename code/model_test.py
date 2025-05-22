import torch
import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0,1"
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import time

def calculate_similarity(query_vector, vector_list, threshold):
    query_vector = query_vector / query_vector.norm(p=2)
    vector_list = vector_list / vector_list.norm(p=2, dim=1, keepdim=True)

    # Calculate cosine similarity
    similarities = torch.matmul(vector_list, query_vector)

    # Find indices where similarity exceeds the threshold
    indices = (similarities > threshold).nonzero(as_tuple=True)[0]

    return indices.tolist()

def calculate_topk_similarity(query_vector, vector_list, topk):

    # Ensure the input tensors are normalized for cosine similarity
    query_vector = query_vector / query_vector.norm(p=2)
    vector_list = vector_list / vector_list.norm(p=2, dim=1, keepdim=True)

    # Calculate cosine similarity
    similarities = torch.matmul(vector_list, query_vector)

    # Get the indices of the top-k most similar vectors
    topk_indices = torch.topk(similarities, topk).indices

    return topk_indices.tolist()

def rag_dataset(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name,device_map="auto",output_hidden_states=True)
    # tokenizer.pad_token = tokenizer.eos_token
    # tokenizer.pad_token_id = tokenizer.eos_token_id
    f = open("/home/slli/home_assistant/our_dataset/raw_data/test_data.jsonl", "r")
    lines = f.readlines()
    f.close()
    f_home = open("/home/slli/home_assistant/our_dataset/raw_data/new_home_status_method.jsonl", "r")
    lines_home = f_home.readlines()
    home_status = {}
    for line in lines_home:
        data = json.loads(line)
        home_status[data["home_id"]] = {"home_status": data["home_status"], "method": data["method"]}
    f_home.close()
    examples = open("/home/slli/home_assistant/our_dataset/raw_data/example1.txt", "r").read()
    system = open("/home/slli/home_assistant/our_dataset/raw_data/system.txt", "r").read()
    data = []
    for i in range(len(lines)):
        case = lines[i]
        case = json.loads(case) 
        state_str, method_str = chang_json2strchunk(home_status[case["home_id"]]["home_status"], home_status[case["home_id"]]["method"])
        state_str_list = state_str.split("<chunk>")[0:-1]
        method_str_list = method_str.split("<chunk>")
        prompt = "After thinking step by step, summry this sentence: {input}: " 
        state_str_list1 = [prompt.format(input=state) for state in state_str_list]
        method_str_list1 = [prompt.format(input=method) for method in method_str_list]
        state_tokens = tokenizer(state_str_list1, return_tensors="pt",padding=True)
        method_tokens = tokenizer(method_str_list1, return_tensors="pt",padding=True)
        query_tokens = tokenizer([case["input"]], return_tensors="pt",padding=True)
        with torch.no_grad():
            state_embeddings = model(**state_tokens,return_dict=True).hidden_states
            state_embeddings = state_embeddings[-1][:,-1,:]
            method_embeddings = model(**method_tokens,return_dict=True).hidden_states
            method_embeddings = method_embeddings[-1][:,-1,:]
            query_embeddings = model(**query_tokens,return_dict=True).hidden_states
            query_embeddings = query_embeddings[-1][:,-1,:][0]

        state_index = calculate_similarity(query_embeddings, state_embeddings, 0.5)
        if len(state_index) == 0:
            state_index = calculate_topk_similarity(query_embeddings, state_embeddings, 3)
        method_index = calculate_similarity(query_embeddings, method_embeddings, 0.5)
        if len(method_index) == 0:
            method_index = calculate_topk_similarity(query_embeddings, method_embeddings, 3)
        new_state_str = ""
        new_method_str = ""
        for index in state_index:
            new_state_str += state_str_list[index]
        for index in method_index:
            new_method_str += method_str_list[index]
        
        case_input = "-------------------------------\n" + "Here are the user instructions you need to reply to.\n" + "<User instructions:> \n" + case["input"] + "\n" + "<Machine instructions:>"
        home_status_case = "<home_state>\n  The following provides the status of all devices in the room of the current household, the adjustable attributes of each device, and the threshold values for adjustable attributes:"+ new_state_str + "\n" + "</home_state>\n"
        device_method_case = "<device_method>\n     The following provides the methods to control each device in the current household:"+ new_method_str + "\n" + "</device_method>\n"
        input = system + home_status_case + device_method_case + examples + case_input
        output = case["output"]
        print("input:",input)

        data.append({"input": input, "output": output})
    
    f = open("/home/slli/home_assistant/our_dataset/raw_data/qwen_rag_test_data.json", "w")
    f.write(json.dumps(data))

class rag_home_assistant_dataset(Dataset):
    def __init__(self,tokenizer):
        self.tokenizer= tokenizer
        f = open("/home/slli/home_assistant/our_dataset/raw_data/qwen_rag_test_data.json", "r")
        self.data = json.load(f)
        f.close()

    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        item = self.data[idx]
        input_text = [
            {"role":"system","content":item["input"]}
        ]
        output_text = item["output"]
        inputs_id = self.tokenizer.apply_chat_template(input_text,add_generation_prompt=True,tokenize=False)

        return inputs_id, output_text

class no_few_shot_home_assistant_dataset(Dataset):
    def __init__(self,tokenizer,use_rag=False):
        self.tokenizer= tokenizer
        if use_rag:
            f = open("/home/slli/home_assistant/our_dataset/raw_data/rag_test_data.json", "r")
            self.data = json.loads(f.read())
            f.close()
        else:
            f = open("/home/slli/home_assistant/our_dataset/raw_data/test_data.jsonl", "r")
            lines = f.readlines()
            f.close()
            f_home = open("/home/slli/home_assistant/our_dataset/raw_data/new_home_status_method.jsonl", "r")
            lines_home = f_home.readlines()
            home_status = {}
            for line in lines_home:
                data = json.loads(line)
                home_status[data["home_id"]] = {"home_status": data["home_status"], "method": data["method"]}
            f_home.close()
            system = open("/home/slli/home_assistant/our_dataset/raw_data/system.txt", "r").read()
            self.data = []
            for i in range(len(lines)):
                case = lines[i]
                case = json.loads(case) 
                state_str, method_str = chang_json2str(home_status[case["home_id"]]["home_status"], home_status[case["home_id"]]["method"])
                case_input = "-------------------------------\n" + "Here are the user instructions you need to reply to.\n" + "<User instructions:> \n" + case["input"] + "\n" + "<Machine instructions:>"
                home_status_case = "<home_state>\n  The following provides the status of all devices in each room of the current household, the adjustable attributes of each device, and the threshold values for adjustable attributes:"+ state_str + "\n" + "</home_state>\n"
                device_method_case = "<device_method>\n     The following provides the methods to control each device in the current household:"+ method_str + "\n" + "</device_method>\n"
                input = system + home_status_case + device_method_case  + case_input
                output = case["output"]
                self.data.append({"input": input, "output": output})

    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        item = self.data[idx]
        input_text = [
            {"role":"system","content":item["input"]}
        ]
        output_text = item["output"]
        inputs_id = self.tokenizer.apply_chat_template(input_text,add_generation_prompt=True,tokenize=False)
        
        return inputs_id, output_text

class home_assistant_dataset(Dataset):
    def __init__(self,tokenizer,use_rag=False):
        self.tokenizer= tokenizer
        if use_rag:
            f = open("/home/slli/home_assistant/our_dataset/raw_data/rag_test_data.json", "r")
            self.data = json.loads(f.read())
            f.close()
        else:
            f = open("/home/slli/home_assistant/our_dataset/raw_data/test_data.jsonl", "r")
            lines = f.readlines()
            f.close()
            f_home = open("/home/slli/home_assistant/our_dataset/raw_data/new_home_status_method.jsonl", "r")
            lines_home = f_home.readlines()
            home_status = {}
            for line in lines_home:
                data = json.loads(line)
                home_status[data["home_id"]] = {"home_status": data["home_status"], "method": data["method"]}
            f_home.close()
            examples = open("/home/slli/home_assistant/our_dataset/raw_data/example1.txt", "r").read()
            system = open("/home/slli/home_assistant/our_dataset/raw_data/system.txt", "r").read()
            self.data = []
            for i in range(len(lines)):
                case = lines[i]
                case = json.loads(case) 
                state_str, method_str = chang_json2str(home_status[case["home_id"]]["home_status"], home_status[case["home_id"]]["method"])
                case_input = "-------------------------------\n" + "Here are the user instructions you need to reply to.\n" + "<User instructions:> \n" + case["input"] + "\n" + "<Machine instructions:>"
                home_status_case = "<home_state>\n  The following provides the status of all devices in each room of the current household, the adjustable attributes of each device, and the threshold values for adjustable attributes:"+ state_str + "\n" + "</home_state>\n"
                device_method_case = "<device_method>\n     The following provides the methods to control each device in the current household:"+ method_str + "\n" + "</device_method>\n"
                input = system + home_status_case + device_method_case + examples + case_input
                output = case["output"]
                self.data.append({"input": input, "output": output})

    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        item = self.data[idx]
        input_text = [
            {"role":"user","content":item["input"]}
        ]
        output_text = item["output"]
        inputs_id = self.tokenizer.apply_chat_template(input_text,add_generation_prompt=True,tokenize=False)
        
        return inputs_id, output_text

def chang_json2strchunk(state,methods):
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
        state_str += "<chunk>"

    method_str = ""
    tmp_room_name = methods[0]["room_name"]
    for method in methods:
        if method["room_name"] != tmp_room_name:
            method_str += "<chunk>"
            tmp_room_name = method["room_name"]
        if method["room_name"] == "None":
            method_str += method["device_name"] + "." + method["operation"] + "("
        else:
            method_str += method["room_name"] + "." + method["device_name"] + "." + method["operation"] + "("
        if len(method["parameters"]) > 0:
            for parameter in method["parameters"]:
                method_str += parameter["name"] + ":" + parameter["type"] + ","
            method_str = method_str[:-1]
        method_str += "),"
    return state_str, method_str

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

def compute_accuracy(generated_texts, expected_texts):
    macro_num_correct = 0
    micro_num_correct = 0
    micro_num_total = 0
    for generated_text, expected_text in zip(generated_texts, expected_texts):
        generated_text = generated_text.replace("<Machine instructions:>", "")
        generated_text = generated_text.replace(" ", "")
        generated_text = generated_text.replace("\n", "")
        
        ## 匹配{}中的内容
        # generated_text= generated_text.replace("{","")
        # generated_text = generated_text.replace("}","")
        # generated_text = generated_text.replace("<","")
        # generated_text = generated_text.replace(">","")
        generated_text = re.findall(r'\{(.*?)\}', generated_text)
        if len(generated_text) > 1:
            print("generated_text:",generated_text)
        else:
            generated_text = generated_text[0]



        ## 匹配‘''' '''中的内容
        expected_text = expected_text.replace("'''", "")
        expected_text = expected_text.replace(" ","")
        expected_text = expected_text.replace("\n","")
        generated_text = generated_text.split(",")
        expected_text = expected_text.split(",")

        generated_text = [x for x in generated_text if x != ""]
        expected_text = [x for x in expected_text if x != ""]
        generated_text = set(generated_text)
        expected_text = set(expected_text)
        print("generated_text:",generated_text)
        print("expected_text:",expected_text)

        if generated_text == expected_text:
            macro_num_correct += 1
        if len(expected_text) == 0 and len(generated_text) == 0:
            micro_num_correct += 1
            micro_num_total += 1
        elif len(expected_text) == 0:
            micro_num_total += 1
        else:
            micro_num_correct += len(generated_text & expected_text)
            micro_num_total += len(expected_text)
    return macro_num_correct / len(generated_texts), micro_num_correct / micro_num_total

def model_test(model_name,use_rag=False,use_few_shot=False,test_type=None):
    if model_name == "llama":
        model_id = '/home/slli/home_assistant/model/llama3-8b-Instruct'
    elif model_name == "qwen":
        model_id = '/home/slli/home_assistant/model/Qwen2.5-7B-Instruct'
    elif model_name == "mistral":
        model_id = '/home/slli/home_assistant/model/Mistral-7B-Instruct-v0.3'
    elif model_name == "gemma":
        model_id = '/home/slli/home_assistant/model/Gemma-7B-Instruct-v0.3'

    print(torch.cuda.is_available())
    tokenizer = AutoTokenizer.from_pretrained(model_id,padding_side='left')
    model = AutoModelForCausalLM.from_pretrained(model_id,torch_dtype=torch.bfloat16,device_map="auto")
    if use_rag:
        test_dataset = rag_home_assistant_dataset(tokenizer)
    elif use_few_shot:
        test_dataset = home_assistant_dataset(tokenizer)
    else:
        test_dataset = no_few_shot_home_assistant_dataset(tokenizer)
        print("test_dataset:",len(test_dataset))
    test_loader = DataLoader(test_dataset, batch_size=1)
    res = []
    start_time = time.time()
    for inputs_id, output_text in tqdm(test_loader):
        if model_name == "llama" or model_name == "mistral":
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.pad_token_id = tokenizer.eos_token_id

        inputs = tokenizer(list(inputs_id), return_tensors="pt",padding=True).to(model.device)
        if model_name == "llama":
            terminator = [
                tokenizer.eos_token_id,
                tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]
            logits = model.generate(**inputs,max_new_tokens=1024,eos_token_id=terminator,do_sample=True,temperature=1.0,top_p=0.9,pad_token_id=tokenizer.eos_token_id)
        else:
            logits = model.generate(**inputs,max_new_tokens=1024,do_sample=True,temperature=1.0,top_p=0.9)
        response = logits[:, len(inputs['input_ids'][0]):]
        generated_texts = tokenizer.batch_decode(response, skip_special_tokens=True)


        for i in range(len(generated_texts)):
            res.append({"generated": generated_texts[i], "expected": output_text[i]})
    end_time = time.time()
    print("time:",end_time-start_time)
    f = open("/home/slli/home_assistant/our_dataset/raw_data/" + model_name + "_" + test_type + "_test_result.json", "w")
    f.write(json.dumps(res))

def llama_test():
    model_id = '/home/slli/home_assistant/model/llama3-8b-Instruct'
    print(torch.cuda.is_available())
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model = AutoModelForCausalLM.from_pretrained(model_id,torch_dtype=torch.bfloat16,device_map="auto")
    test_dataset = home_assistant_dataset()
    test_loader = DataLoader(test_dataset, batch_size=2)
    res = []
    terminator = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    print(terminator)
    print(tokenizer.pad_token,tokenizer.pad_token_id)
    # Define PAD Token = BOS Token
    tokenizer.pad_token = tokenizer.bos_token
    model.config.pad_token_id = model.config.bos_token_id

    for inputs_id, output_text in test_loader:
        inputs = tokenizer(list(inputs_id), return_tensors="pt",padding=True).to(model.device)
        logits = model.generate(**inputs,max_new_tokens=1024,eos_token_id=terminator,do_sample=True,temperature=1.0,top_p=0.9)
        response = logits[:, len(inputs['input_ids'][0]):]
        generated_texts = tokenizer.batch_decode(response, skip_special_tokens=True)
        res.append({"generated": generated_texts, "expected": output_text})
        print("Generated: ", generated_texts)

    f = open("/home/slli/home_assistant/our_dataset/raw_data/llama_test_result.json", "w")
    f.write(json.dumps(res))

def qwen_test():
    model_id = '/home/slli/home_assistant/model/Qwen2.5-7B-Instruct'
    print(torch.cuda.is_available())
    tokenizer = AutoTokenizer.from_pretrained(model_id,padding_side='left')
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype="auto",
        device_map="auto"
    )
    test_dataset = home_assistant_dataset(tokenizer)
    test_loader = DataLoader(test_dataset, batch_size=2)
    res = []
    for inputs_id, output_text in test_loader:
        inputs = tokenizer(list(inputs_id), return_tensors="pt",padding=True).to(model.device)
        logits = model.generate(**inputs,max_new_tokens=1024,do_sample=True,temperature=1.0,top_p=0.9)
        response = logits[:, len(inputs['input_ids'][0]):]
        generated_texts = tokenizer.batch_decode(response, skip_special_tokens=True)
        for i in range(len(generated_texts)):
            res.append({"generated": generated_texts[i], "expected": output_text[i]})

    f = open("/home/slli/home_assistant/our_dataset/raw_data/qwen_test_result.json", "w")
    f.write(json.dumps(res))


if __name__ == "__main__":
    # llama_test()
    model_test("mistral",use_rag=False,use_few_shot=True,test_type="error_input")
    # rag_dataset('/home/slli/home_assistant/model/Qwen2.5-7B-Instruct')
    # f = open("/home/slli/home_assistant/our_dataset/raw_data/llama_test_result.json", "r")
    # res = json.loads(f.read())
    # f.close()
    # generated_texts = []
    # expected_texts = []
    # for item in res:
    #     generated_texts.append(item["generated"])
    #     expected_texts.append(item["expected"][0])
    # print(compute_accuracy(generated_texts, expected_texts))
