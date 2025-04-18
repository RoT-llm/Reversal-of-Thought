from transformers import pipeline
from xarray.tutorial import base_url

from utils.llm_utils import *
from utils.prompt import *
import numpy as np
import json
import argparse
import os
import datetime
from utils.utils import extract, load_jsonl, save_jsonl

parser = argparse.ArgumentParser()
parser.add_argument('--task_name', type=str, default='gameof24',
                    choices=['gameof24', 'checkmate', 'wordsorting', 'gs', 'multi_step', 'sonnet', 'mgsm', 'p3_test'])
parser.add_argument('--dataset', type=str, default=None,help='Dataset filename (Jsonl)')
parser.add_argument('--api', default=None, type=str, help='input baseApi here')
parser.add_argument('--api_key', default=None, type=str, help='input your api key here')
parser.add_argument('--model_id', type=str, default='gpt-4',
                    help='Input model id here, if use local model, input the path to the local model')
parser.add_argument('--top_one', default=10, type=int, help='Input the number of reversal candidate sets here')
parser.add_argument('--candidate_temperature', default=0.7, type=float,
                    help='Sampling temperature for candidates generation (higher values = more random)')
parser.add_argument('--instantiation_temperature', default=0.1, type=float,
                    help='Sampling temperature for reasoning (higher values = more random)')

if __name__ == '__main__':
    args = parser.parse_args()
    task = args.task_name
    dataset = args.dataset
    api_key = args.api_key
    model_id = args.model_id
    top_one = args.top_one
    candidate_temperature = args.candidate_temperature
    instantiation_temperature = args.instantiation_temperature
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d-%H:%M:%S")
    output_dir = 'test_results'

    pipeline = Pipeline(
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        prob=True,
        candidate_temperature=candidate_temperature,
        instantiation_temperature=instantiation_temperature
    )
    # user_prompt=benchmark_input[task]
    # demos=user_prompt.split("###Example###")[1].split("###Input###")[0]
    # user_instruction=user_prompt.split("###Example###")[0]
    demos = "Input:1, 5, 5, 5; Output:5× (5 − 1 ÷ 5) = 24"

    ##Preference-Guided Reverse Reasoning Demo Version
    llm_taste = rot_pipeline(pipeline, reversal_of_thought, demos=demos, warmup=top_one)
    print(llm_taste)
    '''
    llm_def=extract_defination(llm_taste)

    #Knowlege Boundary for known /unknown Demo Version
    is_known=pipeline.compute_similarity(llm_def,user_instruction)
    cpm= None
    if is_known>0.7:
        cpm_p=infor_agg
    else:
        cpm_p=cog_prefer
    llm_taste = pipeline.get_respond(cpm_p,
                               f"LLM-Taste Prompt:{llm_taste}\nBenchmark Prompt:{user_instruction}\n")
    '''
    instantiation = instantiation_prompt.format(llm_taste=llm_taste)


    if dataset:
        data=load_jsonl(dataset)
        for d in data:
            response = pipeline.get_respond(instantiation, d["input"], Switch="instantiation")
            answer = extract(response, d)
            print(answer)
            test_outputs=f'test_results/{model_id}_{task}_{timestamp_str}.jsonl'
            save_jsonl(test_outputs,answer,True)

    else:
        #demo
        data = {"input": "2, 5, 8, 11"}
        response = pipeline.get_respond(instantiation, data["input"], Switch="instantiation")
        answer = extract(response, data)
        print(answer)
