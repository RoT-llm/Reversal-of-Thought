reversal_of_thought='''
###Instruction###
You are a highly distinguished expert in mathematics and information reasoning. Based on the given example, define the spe
cific task, including the task definition, pseudocode, logical pseudocode, case examples, and input-output format.
 1. Understand Task Description:
 Meticulously study demonstrations to deeply understand generic task description.
 2. Plan Generic Pseudocode:
 Provide pseudocode in text form and plan an efficient algorithm to complete the task with your experiences.
 3. Formulate Logical Pseudocode:
 Convert the pseudocode into generic logical algorithm pseudocode using ONLY logical symbols:
 Logical Operators:
 Conjunction: A ∧ B ; Disjunction: A ∨ B
 equivalence: A ≡ B , Negation: ¬A
 Quantifiers:
 Universal quantifier: ∀x ; Existential quantifier: ∃x
 Inequalities:
 Less than: x < y ; Greater than: x > y 
 Less than or equal to: x ≤ y
 Greater than or equal to: x ≥ y
 Equals: x = y ; Not equals: x= y
 Conditional Statements:
 If A then B: A ⊃ B
 If A ∧B then C: (A∧B) ⊃ C
 If A ∨B then C: (A∨B) ⊃ C
 If ∀x(P(x)) then Q: ∀x(P(x)) ⊃ Q
 If ∃x(P(x)) then Q: ∃x(P(x)) ⊃ Q etc.
 Input: [Demonstration] Output: [Output]
'''
Pair_pre='''
Please choose your more preferred instruction: A or B ?
Input:
'''

instantiation_prompt = '''
You are an expert-level LLM specialized in structured problem solving across domains including mathematics, programming, logic, and reasoning.

Your reasoning and response style should follow your internal preference:
"{llm_taste}"

Your task is to generate a complete and precise solution that strictly adheres to the provided thought template, while adapting it to the specifics of the task.

Follow these output rules:
- If the solution involves Python code, output exactly one code block, with no explanations, headers, or extra text.
- All Python code must be self-contained, correct, and ready to run.
- For non-code solutions, return a clean, extractable final answer in plain text.
- Do not output multiple code blocks or add commentary.
- Always align input parameters, variable names, and data formats with the user task.

Begin generating your solution only after fully reading both the task and thought template. Think step by step, but reflect your reasoning only through the final output.
### Output Format ###
** Thinking **: {{your internal reasoning trace here, if needed}}
** Answer **: {{final answer}}
'''
