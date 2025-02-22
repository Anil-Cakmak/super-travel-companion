from my_agent.agent import graph

def chat(user_input: str, thread: str) -> str:

    if not user_input.strip():
        return "Error: Empty input"
        
    try:
        config = {"configurable": {"thread_id": thread}}
        response_message = ""

        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config
        ):
            for value in event.values():
                if "messages" in value:
                    response_message = f"{value['messages'][-1].content}"
    
        return response_message
    except Exception as e:
        return f"Chat Error: {e} \n\n Please try again or start a new session."
