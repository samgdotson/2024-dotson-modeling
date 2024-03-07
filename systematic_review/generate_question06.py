import os
import traceback

os.environ['PYB_CONFIG_FILE'] = "./pybliometrics.cfg"

from pybliometrics.scopus import ScopusSearch, AbstractRetrieval
import json
from tqdm import tqdm
import yaml
import pandas as pd
import numpy as np
import itertools as it
import sys
import glob

# NOTE: config file for pybliometrics is stored in $HOME/.config/pybliometrics.cfg

exclude_terms = ['building']

def combine_terms(term_list, how='and'):

    if how == 'and':
        joiner = " AND "
    elif how == 'or':
        joiner = " OR "

    terms = []
    for term in term_list:
        if term:
            if " " in term:
                terms.append(f"'{term}'")
            else:
                terms.append(f"{term}")
        else:
            continue
    terms = joiner.join(terms)

    return terms


if __name__ == "__main__":

    with open('keywords.yml', 'r') as file:
        data = yaml.load(file, yaml.SafeLoader)
    
    include = data['Include']
    exclude = data['Exclude']
    subjects = data['incl_subjects']

    excluded_terms = combine_terms(exclude, how='or')
    subjects = combine_terms(subjects, how='or')
    
    keys_q6 = ["Location", 
            "Energy justice", 
            "Planning processes", 
            "Energy modelling"]

    combinations = list(it.product(*[v for k, v in include.items() if k in keys_q6]))
    

    current_path = os.getcwd()
    folder_path = os.path.join(current_path, "output", "question_06")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    frames = []
    for combo in tqdm(combinations):

        combined_terms = combine_terms(combo)
        q6 = (f"TITLE-ABS-KEY({combined_terms}) " + 
              f"AND NOT TITLE-ABS-KEY({excluded_terms}) " +
              f"AND SUBJAREA({subjects})")

        x = ScopusSearch(query=q6, view='COMPLETE')

        if x.results:
            print(f"Query: {combined_terms} , Results count: {len(x.results)}", end='\n', flush=True)
            results = pd.DataFrame([doc._asdict() for doc in x.results])
            frames.append(results)

            # store the results and add the ref_docs key to store each reference
            for doc in tqdm(x.results, file=sys.stdout):
                try:
                    # store each result in a file labeled by its Scopus EID
                    doc_dict = doc._asdict()
                    eid = doc_dict["eid"]
                    file_path = os.path.join(folder_path, f"{eid}.json")
                    if not os.path.exists(file_path):
                        # Look up the references / citations for that document
                        document = AbstractRetrieval(eid, view="REF")
                        refs = []
                        # Store the references
                        for ref in document.references:
                            ref_doc = {"doi": ref.doi, "title": ref.title,
                                    "id": ref.id,
                                    "sourcetitle": ref.sourcetitle}
                            refs.append(ref_doc)
                        doc_dict["ref_docs"] = refs
                        # Dump the dictionary to the JSON file
                        with open(file_path, "w") as json_file:
                            json.dump(doc_dict, json_file)
                    else:
                        # print("SKIP (File already exists)", end='\r', flush=True)
                        pass

                # we're not going to try too hard to fix any of the rare errors
                except Exception as e:
                    pass
        else:
            print(f"Query: {combined_terms} , Results count: {x.results}", end='\n', flush=True)

    df = pd.concat(frames, axis=0)
    df.to_csv(os.path.join(folder_path, "data_question_06.csv"))
