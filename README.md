<h1 align="center"> Reversal of Thought: Enhancing Large Language Models with Preference-Guided Reverse Reasoning Warm-up </h1>
<p align="center"> <strong>💌 Contact us:</strong> <a href="mailto:reversalofthought@163.com">reversalofthought@163.com</a> </p>

RoT improves reasoning accuracy and efficiency while minimizing computational costs, leveraging **Preference-Guided Reverse Reasoning** and a **Cognitive Preference Manager** to optimally explore LLM reasoning with cognitive preferences.

## 📚 Dataset
- [24-Game](https://huggingface.co/datasets/nlile/24-game);
- [BIG-Bench](https://github.com/google/BIG-bench);
- [PythonProgrammingPuzzles](https://github.com/microsoft/PythonProgrammingPuzzles);
- [MGSM](https://github.com/google-research/url-nlp/tree/main/mgsm);
- SonnetWriting( [1](https://huggingface.co/datasets/turingmachine/meta-prompting/viewer/default/SonnetWriting), [2](https://github.com/iljones00/Shakespearean-Sonnets-GPT) )
## 🧩 Model Architecture
<img src="./asset/Reversal_Of_Thought.png">

## 🚀 Demo for _Preference-Guided Reverse Reasoning_
🎉🎉🎉 Run `reversal_demo.py` to see the framework in action:
```python
from utils.llm_utils import *
from utils.prompt import *
pipeline=Pipeline(model_id=model_id, base_url=base_url, api_key=api_key, prob=True)
demos = "Input:... Output:..." #Suggest 2-shot Demos
llm_taste=rot_pipeline( pipeline, reversal_of_thought, demos=demos, warmup=5)
```
## 💡 What might `reversal_demo.py` be used for?
- **Enhance LLM-Preferred Prompts for Task Solutions**  
  Refines prompts to align with LLM-preferred strategies, optimizing task-solving efficiency.

- **Potential for Creating Diverse QA Datasets**  
  Generates varied question-answer pairs to improve dataset diversity.

## 📬 Contact Us
We'd love to hear from you! Whether you have ideas, potential applications, or simply want to chat about this project, feel free to get in touch:
💌 **Email**: [reversalofthought@163.com](mailto:reversalofthought@163.com)

## 📖 Citation
If you find our work useful for your research, please kindly cite our paper as follows:
```bibtex
@article{yuan2024reversal,
  title={Reversal of Thought: Enhancing Large Language Models with Preference-Guided Reverse Reasoning Warm-up},
  author={Yuan, Jiahao and Du, Dehui and Zhang, Hao and Di, Zixiang and Naseem, Usman},
  journal={arXiv preprint arXiv:2410.12323},
  year={2024}
}
```
