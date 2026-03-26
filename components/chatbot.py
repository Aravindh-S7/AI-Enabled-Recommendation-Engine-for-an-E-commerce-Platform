import reflex as rx
import os

class ChatState(rx.State):
    is_open: bool = False
    messages: list[dict[str, str]] = [
        {"role": "assistant", "content": "Hi! I am powered by Groq Llama 3. How can I help you find the perfect product today?"}
    ]
    current_input: str = ""
    
    def toggle_chat(self):
        self.is_open = not self.is_open
        
    def send_message(self):
        if not self.current_input.strip():
            return
            
        self.messages.append({"role": "user", "content": self.current_input})
        self.current_input = ""
        yield
        
        target_key = os.getenv("GROQ_API_KEY", "")
        if not target_key:
            self.messages.append({"role": "assistant", "content": "Please provide your GROQ_API_KEY in the .env file and restart the server!"})
            return
            
        try:
            import groq
            client = groq.Groq(api_key=target_key)
            
            api_messages = [{"role": "system", "content": "You are a concise AI assistant for an e-commerce store."}] + self.messages
            
            chat_completion = client.chat.completions.create(
                messages=api_messages,
                model="llama-3.1-8b-instant",
            )
            bot_response = chat_completion.choices[0].message.content
            self.messages.append({"role": "assistant", "content": bot_response})
            
        except Exception as e:
            self.messages.append({"role": "assistant", "content": f"API Error: {str(e)}"})

def chatbot() -> rx.Component:
    """Floating AI assistant for the E-commerce app."""
    return rx.box(
        # The Chat Window
        rx.cond(
            ChatState.is_open,
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="bot", color="blue"),
                        rx.heading("AI Assistant", size="4"),
                        rx.spacer(),
                        rx.button(rx.icon("x"), size="1", variant="ghost", on_click=ChatState.toggle_chat),
                        width="100%",
                        border_bottom="1px solid #eaeaea",
                        padding_bottom="0.5rem"
                    ),
                    rx.vstack(
                        rx.foreach(
                            ChatState.messages,
                            lambda m: rx.box(
                                rx.text(m["content"], size="2"),
                                background_color=rx.cond(m["role"] == "user", "blue.100", "gray.100"),
                                color=rx.cond(m["role"] == "user", "blue.900", "black"),
                                padding="0.75rem",
                                border_radius="lg",
                                align_self=rx.cond(m["role"] == "user", "flex-end", "flex-start"),
                                max_width="85%"
                            )
                        ),
                        width="100%",
                        height="350px",
                        overflow_y="auto",
                        padding_y="1rem",
                        align_items="stretch"
                    ),
                    rx.hstack(
                        rx.input(placeholder="Type a message...", value=ChatState.current_input, on_change=ChatState.set_current_input, width="100%"),
                        rx.button(rx.icon("send"), on_click=ChatState.send_message, color_scheme="blue"),
                        width="100%"
                    ),
                    width="100%",
                    height="100%"
                ),
                position="fixed",
                bottom="5rem",
                right="2rem",
                width="350px",
                shadow="2xl",
                border_radius="lg",
                z_index="2000",
                background_color="white"
            )
        ),
        
        # The Floating Action Button
        rx.button(
            rx.icon(tag="message-circle", size=24),
            position="fixed",
            bottom="2rem",
            right="2rem",
            size="4",
            border_radius="full",
            color_scheme="indigo",
            shadow="xl",
            on_click=ChatState.toggle_chat,
            z_index="2000"
        )
    )
