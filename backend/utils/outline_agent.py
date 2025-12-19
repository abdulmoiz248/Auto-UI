from langchain_core.output_parsers.pydantic import PydanticOutputParser
from pydantic import BaseModel, Field, RootModel
from utils.call_ai import call_ai


class Section(BaseModel):
    sectionName: str = Field(...)
    description: str = Field(...)

class Outline(RootModel[list[Section]]):
    pass

parser = PydanticOutputParser(pydantic_object=Outline)

def generate_outline(topic):
    prompt = f"""
Create a detailed website outline for the topic: "{topic}"

Return ONLY valid JSON array.
Do not include extra text.

{parser.get_format_instructions()}
"""

    response = call_ai([{"content": prompt}])
    parsed = parser.parse(response)
    return parsed.model_dump()  # use model_dump() in Pydantic v2


if __name__ == "__main__":
    topic = "Health and Wellness Blog"
    outline = generate_outline(topic)
    print(outline)