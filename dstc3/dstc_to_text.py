from dstc_utilities import *

# Data source and output paths
data_dir = os.path.join('dstc_data', 'json')
output_dir = os.path.join('dstc_data', 'text')

# If flag is set will only write utterances and not speaker or DA label
utterance_only_flag = False

# File holds all utterances and labels
full_set_file = 'full_set'
remove_file(output_dir, full_set_file, utterance_only_flag)

# Loop over each dataset
sets = ['train', 'test']
for dataset_name in sets:

    # Load JSON file
    data = load_json_data(os.path.join(data_dir, 'dstc3_' + dataset_name))

    # Remove old files if they exist, so we do not append to old data
    file_name = dataset_name + '_set'
    remove_file(output_dir, file_name, utterance_only_flag)

    print("Processing : " + data['dataset'] + " set of " + str(data['num_dialogues']) + " dialogues")

    for dialogue in data['dialogues']:

        # Append all utterances to sets file
        dialogue_to_file(os.path.join(output_dir, file_name), dialogue, utterance_only_flag, 'a+')

        # Append all utterances to full_set text file
        dialogue_to_file(os.path.join(output_dir, full_set_file), dialogue, utterance_only_flag, 'a+')

        # Create the sets directory if is doesn't exist yet
        set_dir = os.path.join(output_dir, dataset_name)

        # If only saving utterances use different directory
        if utterance_only_flag:
            set_dir = set_dir + "_utt/"
        else:
            set_dir = set_dir + "/"

        if not os.path.exists(set_dir):
            os.makedirs(set_dir)

        # Write individual dialogues to sets folder
        dialogue_to_file(os.path.join(set_dir, dialogue['dialogue_id']), dialogue, utterance_only_flag, 'w+')
