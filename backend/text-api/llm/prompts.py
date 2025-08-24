from typing import Any, Tuple

from langchain import PromptTemplate

class PromptsFactory:
    @staticmethod
    def create_prompt(name: str, input: str) -> Tuple[str, Any]:
        prompt_text = """
        Analyze and extract required technical skills, soft skills, company, and role title from the following job description: {job_description}
        """

        response_json_schema = {
            "type": "object",
            "properties": {
                "company": {
                    "type": "string"
                },
                "role": {
                    "type": "string"
                },
                "skills": {
                  "type": "object",
                  "properties": {
                    "technical": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    },
                    "soft": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "technical",
                    "soft"
                  ]
                },
                "education": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
            },
            "required": [
                "company",
                "role",
                "skills"
              ]
        }

        template = PromptTemplate(
            input_variables=["job_description"],
            template=prompt_text,
        )

        return template.format(job_description=input), response_json_schema