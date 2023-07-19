import logging
import os
from typing import Text, Dict, Any

from ruamel.yaml import YAML

logger = logging.getLogger(__name__)

READ_MODE = "r"
ENCODING_UTF8 = "utf8"


def _read_yml(yml_file: str, mode: str = READ_MODE, encoding: str = ENCODING_UTF8):
    ruamel_yaml = YAML()
    ruamel_yaml.preserve_quotes = True
    ruamel_yaml.indent(mapping=2, sequence=4, offset=2)
    with open(yml_file, mode, encoding=encoding) as yml_file_content:
        content_ = ruamel_yaml.load(yml_file_content)

    return content_


def _load_prompts():
    prompts = _read_yml(yml_file=os.path.join("actions", "llm_prompts.yml"))
    logger.info(f"Prompts were loaded successfully.")
    return prompts


# load prompts when actions
# server is initialized
PROMPTS: Dict[Text, Any] = _load_prompts()


def _construct_prompt_from_template(
    template: Text, placeholders: Dict[Text, Text]
) -> Text:
    for placeholder, value in placeholders.items():
        template = template.replace("{{" + str(placeholder) + "}}", value)
        template = template.replace("\\n", "\n")
    return template


def _inject_personality(personality: Text, prompt: Text) -> Text:
    if not personality:
        return prompt

    return f"""{personality}
    
    
    {prompt}
    """


class OpenAIPrompts:
    # best practices:
    # https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api
    # playground:
    # https://platform.openai.com/playground

    response_generate_prompt_default = """
Given the following context and the user query, please generate a response in JSON format containing the answer. The response should be structured as:

{
"answer": "generated_answer"
}

Ensure that the generated answer directly addresses the user query and is based solely on the provided context. The response should only include the "answer" field with the generated answer and no additional information. Please avoid any form of hallucination or generating fictional content. Focus on providing a concise, accurate, and factual answer within the JSON response.

context: 
{{context}}

user_query: `{{query}}`
"""

    response_rephrase_prompt_default = """
Given the following response and the user query, please rephrase the response in a manner suitable to the user query. Ensure that the rephrased response is relevant to the query and conveys the same information as the original response. The rephrased response should be provided in JSON format, structured as:

{
"answer": "rephrased_response"
}

Focus on modifying the response to align it with the user query while maintaining the same meaning. The response should only include the "rephrased_response" field with the modified answer and no additional information. Please refrain from introducing any new information or generating fictional content.

response:
{{response}}

user_query: `{{query}}`
"""

    personality = PROMPTS.get("personality", None)
    custom_generate_prompts = {
        prompt.get("name"): prompt.get("prompt")
        for prompt in PROMPTS.get("generate", [])
    }
    custom_rephrase_prompts = {
        prompt.get("name"): prompt.get("prompt")
        for prompt in PROMPTS.get("rephrase", [])
    }
    custom_prompts = {
        prompt.get("name"): prompt.get("prompt") for prompt in PROMPTS.get("custom", [])
    }

    @staticmethod
    def get_generate_prompt(
        template: Text, query: Text, context: Text, configure_personality: bool = False
    ) -> Text:
        prompt_template = OpenAIPrompts.response_generate_prompt_default

        if template:
            if template in list(OpenAIPrompts.custom_generate_prompts.keys()):
                prompt_template = OpenAIPrompts.custom_generate_prompts.get(template)

        placeholders = {"query": query, "context": context}
        prompt = _construct_prompt_from_template(
            template=prompt_template, placeholders=placeholders
        )

        if configure_personality:
            prompt = _inject_personality(
                personality=OpenAIPrompts.personality, prompt=prompt
            )

        return prompt

    @staticmethod
    def get_rephrase_prompt(
        template: Text, query: Text, response: Text, configure_personality: bool = False
    ) -> Text:
        prompt_template = OpenAIPrompts.response_rephrase_prompt_default

        if template:
            if template in list(OpenAIPrompts.custom_rephrase_prompts.keys()):
                prompt_template = OpenAIPrompts.custom_rephrase_prompts.get(template)

        placeholders = {"query": query, "response": response}
        prompt = _construct_prompt_from_template(
            template=prompt_template, placeholders=placeholders
        )

        if configure_personality:
            prompt = _inject_personality(
                personality=OpenAIPrompts.personality, prompt=prompt
            )

        return prompt

    @staticmethod
    def get_custom_prompt(
        template_name: Text,
        placeholders: Dict[Text, Text] = None,
        configure_personality: bool = False,
    ) -> Text:
        if not template_name:
            return ""

        prompt_template = OpenAIPrompts.custom_prompts.get(template_name, None)
        if not prompt_template:
            return ""

        prompt = prompt_template
        if placeholders:
            prompt = _construct_prompt_from_template(
                template=prompt_template, placeholders=placeholders
            )

        if configure_personality:
            prompt = _inject_personality(
                personality=OpenAIPrompts.personality, prompt=prompt
            )

        return prompt
