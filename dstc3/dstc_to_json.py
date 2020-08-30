import zipfile
import tempfile
from spacy.lang.en import English
from dstc_utilities import *

nlp = English()
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)

# DSTC3 archive directory
archive_dir = 'dstc_archive'

# Processed data directory
data_dir = os.path.join('dstc_data', 'json')

remove_words = ['sil', 'unitelligible', 'unintelligible', 'background', 'noise', 'nosie', 'cough', 'coughing',
                'laughing', 'breathing', 'click', 'clicking', 'knock', 'knocking', 'system', 'dog', 'barking',
                'whisper', 'throat', 'clear', 'clearing', 'throatnoise', 'whisperingunintelligible']
sets = ['train', 'test']
# Create a temporary directory and unzip the archived data
with tempfile.TemporaryDirectory(dir=archive_dir) as tmp_dir:

    # Load into temp directory
    zip_file = zipfile.ZipFile(os.path.join(archive_dir, 'dstc3_archive.zip'), 'r')
    zip_file.extractall(tmp_dir)
    zip_file.close()

    for dataset_name in sets:
        # Get a list of all the dialogues
        set_list = os.listdir(os.path.join(tmp_dir, dataset_name))

        dialogue_data = dict()
        dialogues = []
        num_dialogues = 0
        # For each dialogue
        for folder in set_list:

            # Read JSON files
            sys_data = load_json_data(os.path.join(tmp_dir, dataset_name, folder , "log"))
            usr_data = load_json_data(os.path.join(tmp_dir, dataset_name, folder, "label"))

            dialogue = dict()
            utterances = []
            num_utterances = 0
            # For each turn in the dialogue
            for turn in range(len(usr_data['turns'])):

                # Get the user and system turns
                sys_turn = sys_data['turns'][turn]
                usr_turn = usr_data['turns'][turn]

                # Split the system and user utterances into sentences
                sys_utts = nlp(sys_turn['output']['transcript'])
                usr_utts = nlp(usr_turn['transcription'])

                # Convert system utterances to dictionary
                for sent in sys_utts.sents:
                    utterance = dict()

                    # Set speaker
                    utterance['speaker'] = "SYS"

                    # Set the utterance text
                    utterance['text'] = sent.text

                    # Set ap labels to empty and da label
                    utterance['ap_label'] = ""
                    utterance['da_label'] = sys_turn['output']['dialog-acts'][0]['act']

                    # Get the slot values from the previous user turn
                    slots = dict()
                    if turn > 0:
                        prev_usr_turn = usr_data['turns'][turn - 1]['semantics']['json']
                        for json_slots in prev_usr_turn:
                            # Check there are slot values
                            if json_slots['slots']:
                                slots[json_slots['slots'][0][0]] = json_slots['slots'][0][1]

                    # Set slots data
                    utterance['slots'] = slots

                    # Add to utterances
                    num_utterances += 1
                    utterances.append(utterance)

                # Convert system utterances to dictionary
                for sent in usr_utts.sents:
                    utterance = dict()

                    # Do not keep silence, background noise etc in utterances, else keep all text
                    if any(token.text in remove_words for token in sent):
                        # Replace with <unk> token
                        text = [token.text if not token.text in remove_words else '<unk>' for token in sent]

                        # Ignore if only <unk> tokens left
                        if all(token == '<unk>' for token in text):
                            text = None
                        else:
                            text = " ".join(text)
                    else:
                        text = sent.text

                    # If there is no text (because it was removed) don't make an utterance, else set speaker, text etc
                    if not text:
                        continue
                    else:
                        # Set speaker
                        utterance['speaker'] = "USR"

                        # Set utterance text
                        utterance['text'] = text

                        # Set ap labels to empty and da label if it exists
                        utterance['ap_label'] = ""

                        if usr_turn['semantics']['json']:
                            utterance['da_label'] = usr_turn['semantics']['json'][0]['act']
                        else:
                            utterance['da_label'] = "null"

                        # Add to utterances
                        num_utterances += 1
                        utterances.append(utterance)

            # Create dialogue
            dialogue['dialogue_id'] = dataset_name + '_' + str(num_dialogues + 1)
            dialogue['num_utterances'] = num_utterances
            dialogue['utterances'] = utterances

            # Create the scenario
            scenario = dict()
            scenario['db_id'] = usr_data['session-id']
            scenario['db_type'] = "find restaurant"
            scenario['task'] = usr_data['task-information']['goal']['text']
            scenario['items'] = []
            dialogue['scenario'] = scenario

            # Add to dialogues
            num_dialogues += 1
            dialogues.append(dialogue)

        # Add dataset metadata
        dialogue_data['dataset'] = dataset_name
        dialogue_data['num_dialogues'] = num_dialogues
        dialogue_data['dialogues'] = dialogues

        # Save to JSON file
        save_json_data(os.path.join(data_dir, "dstc3_" + dataset_name), dialogue_data)