#
# class GenerateText:
#     def __init__(self, provider_name: str):
#         self.provider_name = provider_name
#
#     def generate(self, prompt: str, response_format: dict, model_name: str) -> dict:
#         if self.provider_name == "openai":
#             from langchain import OpenAI
#             from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
#             from langchain.chains import LLMChain
#             from langchain.output_parsers import PydanticOutputParser
#
#             llm = OpenAI(model_name=model_name, temperature=0)
#
#             parser = PydanticOutputParser(pydantic_object=response_format)
#
#             system_template = "You are a helpful assistant that helps people find information."
#             human_template = prompt + "\n{format_instructions}"
#             prompt = ChatPromptTemplate.from_messages([
#                 SystemMessagePromptTemplate.from_template(system_template),
#                 HumanMessagePromptTemplate.from_template(human_template)
#             ])
#             prompt_with_format = prompt.partial(format_instructions=parser.get_format_instructions())
#
#             chain = LLMChain(llm=llm, prompt=prompt_with_format, output_parser=parser, verbose=True)
#             response = chain.run()
#
#             return response
#         else:
#             raise ValueError(f"Provider {self.provider_name} not supported.")