import os
import json


def load_json_data(path):
    with open(path + ".json") as file:
        data = json.load(file)
    return data


def save_json_data(path, data):
    with open(path + '.json', 'w+') as file:
        json.dump(data, file, sort_keys=False, indent=4, separators=(',', ': '))


def dialogue_to_file(path, dialogue, utterance_only, write_type):
    if utterance_only:
        path = path + "_utt"
    with open(path + ".txt", write_type) as file:
        for utterance in dialogue['utterances']:
            if utterance_only:
                file.write(utterance['text'].strip() + "\n")
            elif utterance['ap_label']:
                file.write(utterance['speaker'] + "|" +
                           utterance['text'].strip() + "|" +
                           utterance['ap_label'] + "|" +
                           utterance['da_label'] + "\n")
            else:
                file.write(utterance['speaker'] + "|" +
                           utterance['text'].strip() + "|" +
                           utterance['da_label'] + "\n")


def remove_file(data_dir, file, utterance_only):
    # Remove either text or full versions
    if utterance_only:
        if os.path.exists(os.path.join(data_dir, file + '_utt.txt')):
            os.remove(os.path.join(data_dir, file + '_utt.txt'))
    else:
        if os.path.exists(os.path.join(data_dir, file + '.txt')):
            os.remove(os.path.join(data_dir, file + '.txt'))