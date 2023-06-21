from haystack.nodes import PromptTemplate

LFQA_PROMPT = """Synthesize a comprehensive answer from the following text for the given question.
Provide a clear and concise response that summarizes the key points and information
presented in the text. Your answers must be in your own words. Always use Related
text before your knowledge base. If you don't find anything in the related text,
kindly mention what the course is about and that the question goes outside of the
scope of the video course.
\n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:"""


lfqa = PromptTemplate(
    name="lfqa",
    prompt_text=LFQA_PROMPT,
)
