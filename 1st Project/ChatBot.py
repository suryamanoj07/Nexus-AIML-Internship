import json
from difflib import get_close_matches

# Load the data from the json file
def load_data(file_path: str) -> dict:
    with open(file_path) as file:
        data = json.load(file)
    return data

def save_data(file_path: str, data: dict):
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, indent=2)
        
def find_best_match(user_question: str, question: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base['questions']:
        if q['question'] == question:
            return q['answer']
        
        
# Main Script

def chat_bot():
    knowledge_base = load_data("knowledge_base.json")
    
    while True:
        user_input: str = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        best_match: str | None = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])
        if best_match:
            answer: str = get_answer(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: Sorry, I dont know the answer to that question. Please teach me.")
            print("Type the answer or 'skip' to skip.")
            new_answer:str = input("You: ")
            if new_answer.lower() != 'skip':
                knowledge_base['questions'].append({'question': user_input, 'answer': new_answer})
                save_data("knowledge_base.json", knowledge_base)
                print("Bot: Thanks, I learned something new!")
            
            if new_answer.lower() == 'skip':
                print("Bot: Ok, I will skip this question.")
                knowledge_base['questions'].append({'question': user_input, 'answer': 'I dont know the answer to that question.'})
            
if __name__ == "__main__":
    chat_bot()