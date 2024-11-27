from llm_interface import LLM_Interface

if __name__ == "__main__":
    model_path = "_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf"  # Replace with actual path
    llm_interface = LLM_Interface(model_path)

    # Initialize context
    context = "The following is a conversation between a user and an AI."

    # User input
    user_input = "What is the meaning of simulation theory?"

    # Build prompt
    prompt = llm_interface.build_prompt(context, user_input, template_type="reasoning")  # Use the "reasoning" template

    # Generate text using ollama run
    generated_text = llm_interface.generate_text(prompt)

    # Parse the response
    response = llm_interface.parse_response(generated_text)

    # Manage context to fit within the context window
    updated_context = llm_interface.manage_context(context, f"User: {user_input}\nAI: {response}")

    print("Updated Context:", updated_context)