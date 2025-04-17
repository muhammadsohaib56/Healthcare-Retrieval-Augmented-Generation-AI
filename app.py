import gradio as gr
from retriever import Retriever
from generator import Generator
from gradio.themes import Base

# Initialize components
retriever = Retriever()
generator = Generator()

# Custom Light Theme
class LightHealthcareTheme(Base):
    def __init__(self):
        super().__init__()
        self.primary_hue = "#4CAF50"  # Pastel green
        self.secondary_hue = "#81C784"  # Light green accent
        self.background_fill_primary = "#F5F5F5"  # Soft white
        self.background_fill_secondary = "#E0E0E0"  # Light gray
        self.text_color = "#333333"  # Dark gray for readability
        self.button_primary_background_fill = "#4CAF50"
        self.button_primary_text_color = "#FFFFFF"
        self.block_background_fill = "#E8F5E9"  # Very light green

custom_theme = LightHealthcareTheme()

def get_answer(query):
    # Retrieve relevant documents
    retrieved_docs = retriever.retrieve(query, top_k=3)
    
    # Generate answer
    answer = generator.generate_answer(query, retrieved_docs)
    
    # Format retrieved documents for display
    docs_output = ""
    for i, doc in enumerate(retrieved_docs):
        docs_output += f"**Document {i+1}: {doc['id']}**\n{doc['text']}\n\n"
    
    return docs_output, answer

# Gradio Interface with Professional Light Theme
with gr.Blocks(theme=custom_theme, title="Clinical Query System") as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=200):
            # Sidebar
            gr.Markdown("### 🩺 Navigation")
            gr.Markdown("**Features:**\n- Submit Queries\n- View Documents\n- Get Answers")
            gr.Markdown("**Powered by xAI**")
        
        with gr.Column(scale=4):
            # Header
            gr.Markdown("# 🩺 Clinical Query Assistant")
            gr.Markdown("AI-powered insights from MIMIC-IV-Ext data.")

            # Query Input
            query_input = gr.Textbox(
                label="Enter Your Clinical Query",
                placeholder="e.g., What treatment was given for hypertension?",
                lines=2
            )

            submit_btn = gr.Button("Get Answer", variant="primary")

            # Output Sections
            with gr.Tab("Results"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("## 📋 Retrieved Documents")
                        docs_output = gr.Markdown()
                    with gr.Column():
                        gr.Markdown("## ✅ Generated Answer")
                        answer_output = gr.Markdown()

            # Event Handling
            submit_btn.click(
                fn=get_answer,
                inputs=query_input,
                outputs=[docs_output, answer_output]
            )

            # Footer
            gr.Markdown("---")
            gr.Markdown("Developed with ❤️ using Gradio, FAISS, and DistilGPT-2 | Data: MIMIC-IV-Ext")

# Launch the app
demo.launch()