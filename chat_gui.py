import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import messagebox, simpledialog

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.7)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def submit_question(event=None):
    user_input = user_question.get().strip()

    if user_input.lower() == 'quit':
        root.destroy()
        return

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "Bot: " + answer + "\n")
        chat_history.config(state=tk.DISABLED)
        chat_history.see(tk.END)
    else:
        response = messagebox.askquestion("Bot", "I don't know the answer, would you like to teach me?")
        if response == 'yes':
            new_answer = simpledialog.askstring("Bot", "Type the answer:")
            if new_answer:
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                chat_history.config(state=tk.NORMAL)
                chat_history.insert(tk.END, "Bot: Thank you! I have learned a new response.\n")
                chat_history.config(state=tk.DISABLED)
                chat_history.see(tk.END)

    user_question.delete(0, tk.END)  # Clear the entry field

def clear_conversation():
    chat_history.config(state=tk.NORMAL)
    chat_history.delete(1.0, tk.END)
    chat_history.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Chat Bot")

knowledge_base = load_knowledge_base('knowledge_base.json')

chat_history = tk.Text(root, width=50, height=20, state=tk.DISABLED)
chat_history.pack(padx=10, pady=10)

user_question_label = tk.Label(root, text="You:")
user_question_label.pack()
user_question = tk.Entry(root, width=50)
user_question.pack()

submit_button = tk.Button(root, text="Submit", command=submit_question)
submit_button.pack()

clear_button = tk.Button(root, text="Clear", command=clear_conversation)
clear_button.pack()

root.bind('<Return>', submit_question)  # Bind the Enter key to submit_question

root.mainloop()
