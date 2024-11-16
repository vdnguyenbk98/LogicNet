# Challenge for Synthetic Request
import openai
import random
from logicnet.protocol import LogicSynapse
import bittensor as bt
from .human_noise import get_condition
from .math_generator.topics import TOPICS as topics
import mathgenerator


class LogicChallenger:
    def __init__(self, base_url: str, api_key: str, model: str):
        bt.logging.info(
            f"Logic Challenger initialized with model: {model}, base_url: {base_url}"
        )
        self.model = model
        self.openai_client = openai.OpenAI(base_url=base_url, api_key=api_key)

    def __call__(self, synapse: LogicSynapse) -> LogicSynapse:
        self.get_challenge(synapse)
        return synapse

    def get_challenge(self, synapse: LogicSynapse):
        logic_problem = self.get_atom_math_problem(synapse)
        conditions: dict = get_condition()
        revised_logic_question: str = self.get_revised_math_question(
            logic_problem, conditions
        )
        synapse.logic_question = revised_logic_question

    def get_atom_math_problem(self, synapse: LogicSynapse) -> str:
        selected_topic = random.choice(topics)
        subtopic = selected_topic["subtopic"]
        topic = selected_topic["topic"]
        bt.logging.debug(f"Using {mathgenerator.__name__} to generate math problem")
        atom_problem, atom_answer = eval(f"mathgenerator.{topic}.{subtopic}()")
        subtopic = subtopic.replace("_", " ").capitalize()
        topic = topic.replace("_", " ").capitalize()
        atom_problem = atom_problem.replace("$", "").strip()
        atom_problem = f"Find the solution of this math problem:\n---\nTopic: {topic}, Subtopic: {subtopic}.\n{atom_problem}\n---\n"
        bt.logging.debug(f"Generated atom math problem: {atom_problem}")
        synapse.raw_logic_question = atom_problem

        synapse.ground_truth_answer = str(atom_answer).replace("$", "").strip()

        bt.logging.debug(f"Generated atom math answer: {atom_answer}")

        return atom_problem

    def get_revised_math_question(self, math_problem: str, conditions: dict) -> str:
        # prompt = "Please paraphrase by adding word or expression to this question as if you were a {profile} who is {mood} and write in a {tone} tone. You can use incorrect grammar, typo or add more context! Don't add your solution! Just say the revised version, you don't need to be polite.".format(
        #     **conditions
        # )
        
        prompt = (
            "As a {profile} who is feeling {mood}, please rephrase the following math problem "
            "in a {tone} tone. Write it as you would naturally ask the question. "
            "Do not include the solution or add unnecessary context."
        ).format(**conditions)
        
        bt.logging.debug(f"Revising prompt: {prompt}")
        
        # messages = [
        #     {
        #         "role": "user",
        #         "content": "Generate a math problem that required logic to solve.",
        #     },
        #     {"role": "assistant", "content": math_problem},
        #     {
        #         "role": "user",
        #         "content": prompt,
        #     },
        # ]
        
        messages = [
            {
                "role": "system",
                "content": (
                    "You are simulating various human personas asking math problems. "
                    "Rephrase the following math problem as the specified persona, "
                    "ensuring the question sounds natural and appropriate for that individual."
                ),
            },
            {"role": "assistant", "content": math_problem},
            {"role": "user", "content": prompt},
        ]

        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=256,
            temperature=0.7,
        )
        
        response = response.choices[0].message.content.strip()
        bt.logging.debug(f"Generated revised math question: {response}")
        return response
    