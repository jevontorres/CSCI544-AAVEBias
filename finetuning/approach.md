prompt base LLM with SAE texts

use `extract_match.py` to get SAE scores out, match SAE with AAVE lines

now you have a csv with SAE text, SAE scores, AAVE text

_optionally use_ *_`extract_refusals.py`_* _to extract just refused lines_

_now you have a csv with DIALECT text and zereod scores. can then run_ *`extract_csvrow.py`* _on input row, to get a txt of just refused texts_

use `indiv_pretune.py` to create counterfactual dataset

now you have a json with AAVE text, SAE scores, in finetuning format

use `traintestsplitter.py` to create train and test split

now you have train and test jsons. train json will be the input for finetuning

**FINETUNE/TRAIN on [Python Notebook](https://colab.research.google.com/drive/15xson1nZWYYFTGnxLM5jzrKGaEkGxvzh?usp=sharing), download model output as gguf or upload to hugging face**

create Modelfile, with FROM /path to model on local machine  

if have text file of just dialect texts, set only_dialect = True in `modelrunner.py`. if have a text file of dialect text and prompt (output from traintestsplit),use `extract_jsonfield.py` to take just the dialect texts from a instruction json (test split from `traintestsplitter.py`).

use `modelrunner.py` to run the local finetuned model on txt file of dialect texts using ollama

now you have a txt file with results from finetuned model

use `extractor.py` to extract scores from finetuned model output