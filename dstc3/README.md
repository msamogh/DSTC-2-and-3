# DSTC3-Corpus
Utilities for Processing the [Dialogue State Tracking Challenge 3 (DSTC 3) Corpus](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/write_up.pdf)
available [here](http://camdial.org/~mh521/dstc/).
The DSTC is a research challenge focused on improving the state of the art in tracking the state of spoken dialog systems.
The corpus contains dialogues in the restaurant and tourist information domains.
The utilities process the original transcripts into plain text or json formats.

## Scripts
dstc_to_json.py script processes the dialogues from the original format into .json files using the format
outlined below. Each dialogue set (train and test) is output as a separate .json file.
This format is intended to facilitate annotation of the dialogue using the 
[Conversation Analysis Modelling Schema](https://nathanduran.github.io/Conversation-Analysis-Modelling-Schema/).

dstc_to_text.py processes the dialogues from the .json format into plain text files,
with one line per-utterance, using the format outlined below.
Setting the *utterance_only* flag to true will remove the speaker label from the output text files.

dstc_utilities.py script contains various helper functions for loading/saving and processing the data.

## Data Format
The original dialogues have had all 'noise' utterances removed e.g. 'sil', 'throat clear', 'background noise', etc.
Where no dialogue act is present it is replaces with 'null'.
By default utterances are written one per line in the format *Speaker* | *Utterance Text* | *Dialogue Act Tag*.
This can be changed to only output the utterance text by setting the utterance_only_flag = True.

### Example Text Format
SYS|How may I help you?|welcomemsg

USR|pub food cherry hinton|inform

SYS|Are you looking for a pub or a restaurant?|select

USR|pub|inform

SYS|Let me confirm.|expl-conf

### Example JSON Format
The following is an example of the JSON format for the DSTC3 corpus.

```json
    {
        "dataset": "dataset_name",
        "num_dialogues": 1,
        "dialogues": [
            {
                "dialogue_id": "dataset_name_1",
                "num_utterances": 2,
                "utterances": [
                    {
                        "speaker": "A",
                        "text": "Utterance 1 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label"
                    },
                    {
                        "speaker": "B",
                        "text": "Utterance 2 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label",
                        "slots": { //Optional
                            "slot_name": "slot_value"
                        }
                    }
                ],
                "scenario": { //Optional
                    "db_id": "1",
                    "db_type": "i.e booking",
                    "task": "i.e book",
                    "items": []
                }
            }
        ]
    }
```
## Licensing and Attribution
The original papaer for the DSTC3: Henderson, M., Thomson, B. and Williams, J.D. (2014) [The Third Dialog State Tracking Challenge](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/write_up.pdf).

The code within this repository is distributed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).