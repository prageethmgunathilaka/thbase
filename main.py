from ai_agent import EchoAgent

def run_workflow():
    # Initialize the agent
    agent = EchoAgent()
    
    print("Welcome to Echo AI Workflow!")
    print("Type 'quit' to exit")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check if user wants to quit
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        # Get agent's response
        response = agent.respond(user_input)
        print(response)

if __name__ == "__main__":
    run_workflow() 