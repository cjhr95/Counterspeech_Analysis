import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import random
import json
import time

API_KEY = ''    # Add API key
OUTPUT_FILE = 'content.json'

def zero_shot(model, dataset):
    replies = {}
    for i in range(500): # 15 responses allowed per minute by Gemini
        try:
            if i % 15 == 0:
                time.sleep(55)
            response = model.generate_content(f"Respond to the following hate message with appropriate counterspeech in 1-2 sentences: {dataset[str(i)]['HATE_SPEECH']}",
                                            safety_settings={
                                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE})
            replies[str(i)] = response.text
        except:
            # Exceeded response limit
            time.sleep(60)
    return replies

def one_shot(model, dataset):
    replies = {}
    for i in range(301, 881): # 15 responses allowed per minute by Gemini
        try:
            if i % 15 == 0:
                time.sleep(55)
            response = model.generate_content(f"Respond to the following hate message with appropriate counterspeech in 1-2 sentences using a provided counterspeech example of [{dataset[str(i)]['COUNTER_NARRATIVE']}]: {dataset[str(i)]['HATE_SPEECH']}",
                                            safety_settings={
                                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE})
            replies[str(i)] = response.text
        except:
            # Exceeded response limit
            time.sleep(60)
    return replies

def two_shot(model, dataset):
    replies = {}
    rand_index = 0
    for i in range(881, 1501): # 15 responses allowed per minute by Gemini
        while True:
            rand_index = random.randint(881, 1500)
            try:
                if dataset[str(rand_index)]['TARGET'] == dataset[str(i)]['TARGET']:
                    break
                else:
                    continue
            except KeyError:
                continue
        try:
            if i % 15 == 0:
                time.sleep(55)
            response = model.generate_content(f"Respond to the following hate message with appropriate counterspeech in 1-2 sentences using the provided counterspeech examples [{dataset[str(i)]['COUNTER_NARRATIVE']}], [{dataset[str(rand_index)]['COUNTER_NARRATIVE']}]: {dataset[str(i)]['HATE_SPEECH']}",
                                            safety_settings={
                                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE})
            replies[str(i)] = response.text
        except:
            # Exceeded response limit
            time.sleep(60)
    return replies

def three_shot(model, dataset):
    replies = {}
    rand_index = 0
    rand_index_2 = 0
    for i in range(1501, 2001): # 15 responses allowed per minute by Gemini
        while True:
            rand_index = random.randint(1501, 2000)
            try:
                if dataset[str(rand_index)]['TARGET'] == dataset[str(i)]['TARGET']:
                    break
                else:
                    continue
            except KeyError:
                continue
        while True:
            rand_index_2 = random.randint(1501, 2000)
            try:
                if dataset[str(rand_index_2)]['TARGET'] == dataset[str(i)]['TARGET'] and rand_index != rand_index_2:
                    break
                else:
                    continue
            except KeyError:
                continue
        try:
            if i % 15 == 0:
                time.sleep(55)
            response = model.generate_content(f"Respond to the following hate message with appropriate counterspeech in 1-2 sentences using the provided counterspeech examples [{dataset[str(i)]['COUNTER_NARRATIVE']}], [{dataset[str(rand_index)]['COUNTER_NARRATIVE']}], [{dataset[str(rand_index_2)]['COUNTER_NARRATIVE']}]: {dataset[str(i)]['HATE_SPEECH']}",
                                            safety_settings={
                                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE})
            replies[str(i)] = response.text
        except:
            # exceeded response limit
            time.sleep(60)
    return replies

if __name__ == '__main__':
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    with open('Multitarget-CONAN.json') as f:
        dataset = json.load(f)
        zs_dict = zero_shot(model, dataset)
        print("Done with zero shot. Waiting...")
        time.sleep(60)

        os_dict = one_shot(model, dataset)
        print("Done with one shot. Waiting...")
        time.sleep(60)

        print("Starting two shot...")
        twos_dict = two_shot(model, dataset)
        print("Done with two shot. Waiting...")
        time.sleep(60)

        print("Starting three shot...")
        threes_dict = three_shot(model, dataset)
        print("Done with three shot.")
        print("Responses generated.")
    
    # Zero shot results
    with open('responses/zero_shot_responses.json', 'w', encoding='utf-8') as f:
        json.dump(zs_dict, f, ensure_ascii=False, indent=4)
    print(f"Copied responses to zero_shot_responses.json")

    # One shot results
    with open('responses/one_shot_responses.json', 'w', encoding='utf-8') as f:
        json.dump(os_dict, f, ensure_ascii=False, indent=4)
    print(f"Copied responses to one_shot_responses.json")

    # Two shot results
    with open('responses/two_shot_responses.json', 'w', encoding='utf-8') as f:
        json.dump(twos_dict, f, ensure_ascii=False, indent=4)
    print(f"Copied responses to two_shot_responses.json")

    # Three shot results
    with open('responses/three_shot_responses.json', 'w', encoding='utf-8') as f:
        json.dump(threes_dict, f, ensure_ascii=False, indent=4)
    print("Copied responses to three_shot_respones.json")