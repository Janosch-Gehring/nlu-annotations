import json

INPUT_FILEPATH = "ambiguity_task/resources/pilot_study.json"
OUTPUT_FILEPATH = "ambiguity_task/resources/pilot_samples_manual_filtering.json"

MANUAL_FILTERING = True

def main():
    with open(INPUT_FILEPATH, "r") as f:
        data = json.loads(f.read())
    
    output = {}

    sample_index = 1
    for key in data:
        if key == "metadata":
            continue
        word = data[key]["word"]
        meaning1 = data[key]["meaning1"]
        meaning2 = data[key]["meaning2"]

        filter_ok = not MANUAL_FILTERING
        if MANUAL_FILTERING:
            print(f"\n\n\n-----\n\n\nThe next word is {word}, meaning either '{meaning1}' or '{meaning2}'")
            print("The generated sentences are...")
            for sentence in data[key]:
                if sentence.count(word) != 1:
                    continue
                formatted_sentence = sentence.replace(word, "[" + word + "]")
                for meaning_index in ["1", "2"]:
                    for context in data[key][sentence][meaning_index]["contexts"]:
                        print(sentence, context)
            user_input = input("Are these examples high quality? Y/n")
            if "y" in user_input.lower():
                filter_ok = True

        if not filter_ok:
            continue
        for sentence in data[key]:
            if sentence.count(word) != 1:
                continue  # word must only be used once, otherwise sample is noisy
            formatted_sentence = sentence.replace(word, "[" + word + "]")
                    
            output[sample_index] = {
                "sentence": formatted_sentence,
                "word": word,
                "meaning1": meaning1,
                "meaning2": meaning2,
                "grouping": sample_index % 8  # 7 samples per sentence
                }
            sample_index += 1

            sentence_data = data[key][sentence]
            for meaning_index in ["1", "2"]:
                for context in sentence_data[meaning_index]["contexts"]:
                    output[sample_index] = {
                    "sentence": formatted_sentence + " " + context,
                    "word": word,
                    "meaning1": meaning1,
                    "meaning2": meaning2,
                    "grouping": sample_index % 8  # 7 samples per sentence
                    }
                    sample_index += 1
        with open(OUTPUT_FILEPATH, "w") as f:
            json.dump(output, f, indent=4)




if __name__ == "__main__":
    main()