from transformers import pipeline

class Generator:
    def __init__(self):
        # Load a small generative model
        self.generator = pipeline("text-generation", model="distilgpt2")

    def generate_answer(self, query, retrieved_docs):
        # Combine retrieved documents into context
        context = "\n".join([doc["text"] for doc in retrieved_docs])
        
        # Enhanced prompt with clear instructions
        prompt = f"""You are a clinical assistant. Based on the following clinical notes, provide a detailed and accurate answer to the query about treatments. Focus only on relevant medical information and avoid unrelated content. Use a structured format with headings.

Query: {query}
Relevant Notes:
{context}
Answer:
### Treatment Summary
"""

        # Generate response with increased max_new_tokens for longer answers
        response = self.generator(prompt, max_new_tokens=500, num_return_sequences=1)
        answer = response[0]["generated_text"].split("Answer:")[-1].strip()
        
        # Ensure proper markdown formatting
        if "### Treatment Summary" not in answer:
            answer = f"### Treatment Summary\n{answer}"
        return answer

if __name__ == "__main__":
    # Test the generator
    generator = Generator()
    query = "What treatment was given for hypertension?"
    docs = [{"id": "test.json", "text": "Patient received labetalol 100 mg for BP 180/125."}]
    answer = generator.generate_answer(query, docs)
    print(f"Generated Answer: {answer}")