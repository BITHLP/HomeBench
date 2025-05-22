import json
import re
from collections import Counter

def compute_accuracy(generated_texts, expected_texts):
    print("nums"   , len(generated_texts))
    correct_num = 0
    tp = 0
    all_pre = 0
    all_gold = 0
    res11 = []
    for generated_text, expected_text in zip(generated_texts, expected_texts):
        res = {}
        # generated_text = generated_text.split("</think>\n\n")[1]
        generated_text = generated_text.replace(" ", "")
        generated_text = generated_text.replace("\n", "")
        test11 = generated_text
        generated_text = re.findall(r'\{(.*?)\}', generated_text)

        if len(generated_text) > 1:
            # print("generated_text:",generated_text)
            generated_text = ",".join(generated_text)
        elif len(generated_text) == 0:
            generated_text = ""
        else:
            generated_text = generated_text[0]

        
        expected_text = expected_text.replace("'''", "")
        expected_text = expected_text.replace(" ","")
        expected_text = expected_text.replace("\n","")
        expected_text = expected_text.split(",")
        expected_text = [x for x in expected_text if x != ""]

        generated_text = generated_text.split(",")
        generated_text = [x for x in generated_text if x != ""]
        # print("generated_text:",generated_text)
        # print("expected_text:",expected_text)
        generated_counter = Counter(generated_text)
        expected_counter = Counter(expected_text)
        if generated_counter == expected_counter:
            correct_num += 1
        else:
            res11.append({"generated":generated_text, "expected":expected_text})
        intersection = generated_counter & expected_counter

        tp += len(list(intersection.elements()))
        all_pre += len(generated_text)
        all_gold += len(expected_text)

    print("em:", correct_num / len(generated_texts))
    print("Precision:", tp / all_pre)
    print("Recall:", tp / all_gold)
    precision = tp / all_pre
    recall = tp / all_gold
    if precision + recall == 0:
        print("F1:", 0)
    else:
        print("F1:", 2 * precision * recall / (precision + recall))

    return res11


def dif_type(test_data):
    f = open("/home/slli/home_assistant/our_dataset/raw_data/test_data.jsonl","r")
    data = f.readlines()
    f.close()
    normal_single = {"expected": [], "generated": []}
    unexist_single = {"expected": [], "generated": []}
    unexist_attribute_single = {"expected": [], "generated": []}
    unexist_device_single = {"expected": [], "generated": []}
    normal_multi = {"expected": [], "generated": []}
    mix_multi = {"expected": [], "generated": []}
    error_multi = {"expected": [], "generated": []}
    all = {"expected": [], "generated": []}
    print("test_data",len(test_data))
    print("data",len(data))
    # assert len(data) == len(test_data)
    for i in range(len(test_data)):
        item = json.loads(data[i])
        item2 = test_data[i]
        assert item["output"] == item2["gold_output"]
        all["expected"].append(item["output2"])
        all["generated"].append(item2["generated_output"])
        if item["type"] == "normal":
            normal_single["expected"].append(item["output2"])
            normal_single["generated"].append(item2["generated_output"])
        elif item["type"] == "unexist_device":
            unexist_device_single["expected"].append(item["output2"])
            unexist_device_single["generated"].append(item2["generated_output"])
            unexist_single["expected"].append(item["output2"])
            unexist_single["generated"].append(item2["generated_output"])
        elif item["type"] == "unexist_attribute":
            unexist_attribute_single["expected"].append(item["output2"])
            unexist_attribute_single["generated"].append(item2["generated_output"])
            unexist_single["expected"].append(item["output2"])
            unexist_single["generated"].append(item2["generated_output"])
        else:
            tmp = item["type"].split("_")[1]
            if tmp == "mix":
                mix_multi["expected"].append(item["output2"])
                mix_multi["generated"].append(item2["generated_output"])
            elif tmp == "normal":
                normal_multi["expected"].append(item["output2"])
                normal_multi["generated"].append(item2["generated_output"])
            else:
                error_multi["expected"].append(item["output2"])
                error_multi["generated"].append(item2["generated_output"])
    print("all")
    compute_accuracy(all["generated"], all["expected"])
    print("normal_single")
    compute_accuracy(normal_single["generated"], normal_single["expected"])
    print("unexist_single")
    ffff = open("/home/slli/home_assistant/our_dataset/raw_data/unexist_single.json","w")
    for i in range(len(unexist_single["generated"])):
        res = {}
        res["gpt"] = unexist_single["generated"][i]
        res["g"] = unexist_single["expected"][i]
        ffff.write(json.dumps(res)+"\n")
    
    compute_accuracy(unexist_single["generated"], unexist_single["expected"])
    # print("unexist_device_single")
    # compute_accuracy(unexist_device_single["generated"], unexist_device_single["expected"])
    # print("unexist_attribute_single")
    # compute_accuracy(unexist_attribute_single["generated"], unexist_attribute_single["expected"])
    print("normal_multi")

    nm_error = compute_accuracy(normal_multi["generated"], normal_multi["expected"])
    ffff = open("/home/slli/home_assistant/our_dataset/raw_data/normal_multi.json","w")
    for i in range(len(nm_error)):
        res = {}
        res["generated"] = nm_error[i]["generated"]
        res["expected"] = nm_error[i]["expected"]
        ffff.write(json.dumps(res)+"\n")

    print("mix_multi")
    mm_error=compute_accuracy(mix_multi["generated"], mix_multi["expected"])
    ffff = open("/home/slli/home_assistant/our_dataset/raw_data/mix_multi.json","w")
    for i in range(len(mm_error)):
        res = {}
        res["generated"] = mm_error[i]["generated"]
        res["expected"] = mm_error[i]["expected"]
        ffff.write(json.dumps(res)+"\n")
    print("error_multi")
    x = compute_accuracy(error_multi["generated"], error_multi["expected"])
    ffff = open("/home/slli/home_assistant/our_dataset/raw_data/error_multi.json","w")
    for i in range(len(x)):
        res = {}
        res["generated"] = x[i]["generated"]
        res["expected"] = x[i]["expected"]
        ffff.write(json.dumps(res)+"\n")



    return None



f = open("/home/slli/home_assistant/our_dataset/raw_data/deepseek_r1_no_fewshot2.json", "r")
data = f.readlines()
# data = json.load(f)
test_data = []
generated_output = []
excepted_output = []
for item in data:
    item = json.loads(item)
    generated_output.append(item["generated"])
    excepted_output.append(item["expected"])
    test_data.append({"generated_output": item["generated"], "gold_output": item["expected"]})
    # generated_output.append(item["gpt_output"])
    # excepted_output.append(item["golden_output"])
    # test_data.append({"generated_output": item["gpt_output"], "gold_output": item["golden_output"]})


dif_type(test_data)
