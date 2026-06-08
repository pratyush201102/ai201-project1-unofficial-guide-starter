from __future__ import annotations

import gradio as gr

from src.rag_pipeline import ask


def handle_query(question: str, top_k: int):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question, top_k=int(top_k))
    sources_text = "\n".join(f"- {s}" for s in result["sources"]) if result["sources"] else "No sources retrieved"
    return result["answer"], sources_text


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("# The Unofficial Guide\nAsk questions over your student knowledge documents.")

    with gr.Row():
        question = gr.Textbox(label="Question", placeholder="Example: Is the housing lottery actually random?")
        top_k = gr.Slider(minimum=1, maximum=10, value=5, step=1, label="Top-k retrieval")

    ask_btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=6)

    ask_btn.click(handle_query, inputs=[question, top_k], outputs=[answer, sources])
    question.submit(handle_query, inputs=[question, top_k], outputs=[answer, sources])


demo.launch()
