import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OUTPUT_FILEPATH = "var_ending_test/resources/test_samples.json"

client = openai.OpenAI(api_key=OPENAI_API_KEY)

MODELS = ["gpt-4o", "gpt-4o-mini"]
STYLES = ["0shot", "4shot"]


def completions(query: str, model: str = "gpt-4o") -> str:
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user",
             "content": query
             }
        ]
    )
    content = completion.choices[0].message.content
    content = content.replace("json", "")
    content = content.replace("```", "")
    print(content)
    return completion.choices[0].message.content



def generation_prompt(sample, part="precontext"):
    if part == "precontext":
        part_description = "premises that preceed this sentence"
    else:
        part_description = "endings that follow this story"
    prompt = f"""
        The sentence "{sample["sentence"]}" is part of a to-be-constructed story. 
        "{sample["word"]}" has two meanings: "{sample["meaning1"]} and {sample["meaning2"]}. 
        Your task: Give me three story {part_description}. The first one should have one sentence, the second one two sentences, the third one three sentences.
        Keep the sentences short and the language simple.
        Keep in mind that both meanings of the word should be at least somewhat plausible in all cases. 
        Please refrain from referencing the meanings through synonyms or paraphrases. Don't use the word {sample["word"]} either, but you can introduce other new information. The three texts should be fairly distinct from another. Regarding the meanings of the word, keep it implicit and a bit vague.
        Return it in a json format with the three keys "1", "2" and "3", each key having one of the {part_description} as value. Do not return anything else or any other formatting so the answer can be loaded with python json.
    """
    return prompt

if __name__ == "__main__":
    with open("var_ending_test/resources/homonyms.json", "r") as f:
        homonyms = json.load(f)

    output = {}

    for i in homonyms:
        output[i] = {"word": homonyms[i]["word"], "meaning1": homonyms[i]["meaning1"], "meaning2": homonyms[i]["meaning2"],
                     "focus_meaning": homonyms[i]["meaning1"], "precontexts": [], "endings": []}
        precontext_prompt = generation_prompt(homonyms[i])
        ending_prompt = generation_prompt(homonyms[i], part="ending")
        precontext = json.loads(completions(precontext_prompt))
        ending = json.loads(completions(ending_prompt))
        for ind in ["1", "2", "3"]:
            output[i]["precontexts"].append(precontext[ind])
            output[i]["endings"].append(ending[ind])

    with open(OUTPUT_FILEPATH, "w") as f:
        json.dump(output, f, indent=4)
