from openai import OpenAI
import transformers
from safetensors import torch
from sentence_transformers import SentenceTransformer, util
from prompt import *
import numpy as np
import math
def evaluate_preference(A, B, pipeline):
    """
    Evaluate which response is better between A and B using the pipeline.

    Parameters:
    - A: First response.
    - B: Second response.
    - pipeline: The language model pipeline used for preference evaluation.

    Returns:
    - preference_score: The preference score (probability).
    """
    r, s = pipeline.get_respond(Pair_pre, F"A:{A}\nB:{B}", prob=True, max_tokens=1)
    print(r,s)
    if r == "B":
        s = 1 - s
    return s


def rot_pipeline(pipeline, reversal_of_thought, demos, warmup=3):
    """
    Perform Preference-Guided Reverse Reasoning (PGRR) on the given pipeline.
    https://arxiv.org/abs/2410.12323

    Parameters:
    - pipeline: The language model pipeline used for generating responses.
    - reversal_of_thought: The initial prompt or task definition for reasoning.
    - demos: A list of input-output demonstrations.
    - warmup: The number of warm iterations (default is 5).

    Returns:
    - P_opt: The optimal prompt based on reverse reasoning and pairwise preference.
    """
    responses = []
    P_res = []

    # Step 1: Reverse Reasoning Warm-up
    for i in range(warmup):
        R_i = pipeline.get_respond(reversal_of_thought, demos, prob=True,Switch="candidate")
        responses.append(R_i[0])
        P_res.append(R_i[1])
    P_pre = {}

    for i in range(warmup - 1):
        for j in range(i + 1, warmup):
            preference_score = evaluate_preference(responses[i], responses[j], pipeline)
            P_pre[(i, j)] = preference_score
            P_pre[(j, i)] = 1 - preference_score  # Add the reverse preference

    for i in range(warmup):
        for j in range(warmup):
            if i != j:
                for k in range(warmup):
                    if k != i and k != j:
                        P_pre[(i, k)] = max(P_pre.get((i, k), 0), P_pre[(i, j)] * P_pre.get((j, k), 0))

    P_pre_avg = []
    for i in range(warmup):
        avg_preference = sum([P_pre.get((i, j), 0) for j in range(warmup) if j != i]) / (warmup - 1)
        P_pre_avg.append(avg_preference)
    P_opt = max(range(warmup), key=lambda i: (P_res[i] + P_pre_avg[i]) / 2)
    return P_opt, responses[P_opt]

class Pipeline:
    def __init__(self, model_id, api_key=None,
                 base_url='https://api.openai.com/v1/',
                 prob=False,max_tokens=4096,
                 candidate_temperature=0.7,
                 instantiation_temperature=0.1):
        """
        Initialize the Pipeline class.

        Args:
        - model_id (str): Model identifier (either local model path or OpenAI model name).
        - api_key (str, optional): OpenAI API key. If None, local inference is used.
        - base_url (str): API base URL for OpenAI.
        - prob (bool): Whether to request token log probabilities.
        - max_tokens (int): Maximum number of tokens to generate.
        - candidate_temperature (float): Sampling temperature for candidate generation.
        - instantiation_temperature (float): Sampling temperature for instantiation generation.
        """
        self.api = False
        self.local = False
        self.base_url = base_url
        self.model_id = model_id
        self.max_tokens=max_tokens
        self.prob=prob
        self.cpm = SentenceTransformer("dunzhang/stella_en_1.5B_v5", trust_remote_code=True).cuda()
        self.candidate_temperature=candidate_temperature
        self.instantiation_temperature=instantiation_temperature
        if api_key is None:
            import torch
            self.local = True
            self.pipeline = transformers.pipeline(
                "text-generation",
                model=self.model_id,
                model_kwargs={"torch_dtype": torch.bfloat16},
                device_map='auto'
            )
            self.model = self.pipeline.model
            self.tokenizer = self.pipeline.tokenizer
        else:
            self.api = True
            self.api_key = api_key

    def compute_similarity(self,sentence1, sentence2):
        """
       Compute cosine similarity between two sentences using embeddings.

       Args:
       - sentence1 (str): First sentence.
       - sentence2 (str): Second sentence.

       Returns:
       - float: Cosine similarity score.
       """
        embedding1 = self.cpm.encode(sentence1, convert_to_tensor=True)
        embedding2 = self.cpm.encode(sentence2, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embedding1, embedding2)

        return similarity.item()
    def get_respond(self, meta_prompt, user_prompt, max_tokens=None, prob=False, Switch="candidate"):
        """
        Generate a response from the model, using either OpenAI API or local inference.

        Args:
        - meta_prompt (str): System prompt to guide the model.
        - user_prompt (str): User input prompt.
        - max_tokens (int, optional): Override the default max token limit.
        - prob (bool): Whether to return average token probability.
        - Switch (str): Mode of generation ('candidate' or 'instantiation').

        Returns:
        - str: The generated response.
        - float (optional): Average probability if `prob` is True.
        """
        global logprobs, completion, outputs
        self.prob=prob
        if max_tokens:
            self.max_tokens=max_tokens
        messages=[
            {"role": "system", "content": meta_prompt},
            {"role": "user", "content": user_prompt},
        ]
        if self.api:
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            temperature = self.candidate_temperature if Switch == "candidate" else self.instantiation_temperature
            completion = client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                max_tokens=self.max_tokens,
                logprobs=self.prob,
                temperature=temperature
            )

            print(completion)
            response = completion.choices[0].message.content
            if self.prob:
                logprobs = [token.logprob for token in completion.choices[0].logprobs.content]
                probs = [math.exp(logprob) for logprob in logprobs]
                probs=np.mean(probs)
                return response, probs


        else:

            prompt = self.tokenizer.apply_chat_template(
                messages=messages,
                tokenize=False,
                add_generation_prompt=True
            )

            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            terminators = [
                self.tokenizer.eos_token_id,
                self.tokenizer.convert_tokens_to_ids("<|eot|>")
            ]

            temperature = self.candidate_temperature if Switch == "candidate" else self.instantiation_temperature
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_tokens,
                    return_dict_in_generate=True,
                    output_scores=True,
                    do_sample=True,
                    temperature=temperature,
                    top_p=0.9,
                    eos_token_id=terminators
                )

            generated_ids = outputs.sequences[0][inputs["input_ids"].shape[-1]:]
            response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
            if self.prob:
                logprobs = []
                for i, score in enumerate(outputs.scores):
                    token_id = generated_ids[i]
                    logit = score[0]
                    prob = torch.nn.functional.log_softmax(logit, dim=0)[token_id]
                    logprobs.append(prob.item())
                tokens = self.tokenizer.convert_ids_to_tokens(generated_ids)
                avg_prob = np.mean([math.exp(lp) for lp in logprobs])
                return response, avg_prob

        return response


