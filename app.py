from speech_processor import SpeechProcessor
import time

def handle_command(command):
    """Handle a detected command"""
    if not command:
        return
        
    print("\n--- COMMAND DETECTED ---")
    print(f"Type: {command['type']}")
    
    if command['type'] == 'create_agent':
        print(f"Creating agent named: {command['name']}")
        # Here you would call your AgentManager to actually create the agent
    
    elif command['type'] == 'define_scope':
        print(f"Setting scope for agent {command['agent_name']} to: {command['scope']}")
        # Here you would call your AgentManager to set the scope
    
    elif command['type'] == 'add_instruction':
        print(f"Adding instruction to agent {command['agent_name']}: {command['instruction']}")
        # Here you would call your AgentManager to add the instruction

def main():
    # Create the speech processor with our command handler
    processor = SpeechProcessor(command_callback=handle_command)
    
    try:
        # Start listening
        processor.start_listening()
        
        # Keep the program running
        print("Say commands like 'create an agent named assistant'")
        print("Press Ctrl+C to exit")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        processor.stop_listening()

if __name__ == "__main__":
    main() 