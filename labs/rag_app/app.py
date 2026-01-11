import gradio as gr
from dotenv import load_dotenv
from answer import answer_question

load_dotenv(override=True)


def format_context(context):
    result = "<h2 style='color: #ff7800;'>Relevant Context</h2>\n\n"
    for doc in context:
        result += f"<span style='color: #ff7800;'>Source: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result


def chat(history):
    """
    Process a chat message and generate a response.
    Args:
        history: List of message dicts from Gradio chatbot component.
                Each dict has "role" ("user" or "assistant") and "content" keys.
                This comes from the chatbot component which maintains conversation state.
    """
    last_message = history[-1]["content"]  # Get the most recent user message
    prior = history[:-1]  # Get all previous messages for context
    answer, context = answer_question(last_message, prior)
    history.append({"role": "assistant", "content": answer})
    return history, format_context(context)


def main():
    def put_message_in_chatbot(message, history):
        """
        Add user message to chat history.
        Args:
            message: The user's message text
            history: Current chat history from chatbot component.
                    On first call, this will be [] (empty list).
                    On subsequent calls, it contains previous messages.
        Returns:
            Empty string (to clear input) and updated history with new user message
        """
        return "", history + [{"role": "user", "content": message}]

    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title="Insurellm Expert Assistant", theme=theme) as ui:
        gr.Markdown("# 🏢 Insurellm Expert Assistant\nAsk me anything about Insurellm!")

        with gr.Row():
            with gr.Column(scale=1):
                # Chatbot component initializes with history=[] (empty list) by default
                # When value parameter is not provided, Gradio defaults to None, which becomes []
                chatbot = gr.Chatbot(
                    label="💬 Conversation", height=600, type="messages", show_copy_button=True
                    # value=None (default) → Gradio converts to history=[]
                )
                message = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask anything about Insurellm...",
                    show_label=False,
                )

            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    label="📚 Retrieved Context",
                    value="*Retrieved context will appear here*",
                    container=True,
                    height=600,
                )

        message.submit(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])

    ui.launch(inbrowser=True)


if __name__ == "__main__":
    main()
