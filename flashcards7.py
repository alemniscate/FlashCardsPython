import random
import os
import sys

log = []

def logout(msg):
    print(msg)
    log.append(msg)

def loginput():
    data = input()
    log.append(data)
    return data

def loginput_term(cards):
    while(True):
        term = loginput()
        if term not in cards:
            return term
        logout(f'The card "{term}" already exists. Try again:')

def loginput_definition(cards):
    while(True):
        definition = loginput()
        if not is_definition_exist(definition, cards):
            return definition
        logout(f'The definition "{definition}" already exists. Try again:')

def get_key(target_definition, cards):
    for key, value in cards.items():
        definition, mistakes = value
        if definition == target_definition:
            return key

def is_definition_exist(target_definition, cards):
    for value in cards.values():
        definition, mistakes = value
        if definition == target_definition:
            return True
    return False

def check_answer(answer, value, cards):
    definition, mistakes = value
    if answer == definition:
        logout("Correct!")
        return

    value[1] = mistakes + 1
    if is_definition_exist(definition, cards):
        term = get_key(answer, cards)
        logout(f'Wrong. The right answer is "{definition}", but your definition is correct for "{term}".')
    else:
        logout(f'Wrong. The right answer is "{definition}".')

def ask_card(cards):
    logout("How many times to ask?")
    n = int(loginput())

    for i in range(n):
        term = random.choice(list(cards.keys()))
        value = cards[term]
        logout(f'Print the definition of "{term}":')
        answer = loginput()
        check_answer(answer, value, cards)

def add_card(cards):
    logout("The card:")
    term = loginput_term(cards)
    logout("The definition of the card:")
    definition = loginput_definition(cards)
    cards[term] = [definition, 0]
    logout(f'The pair ("{term}":"{definition}") has been added.')

def import_card(cards, filename=None):
    if not filename:
        logout("File name:")
        filename = loginput()

    if not os.path.exists(filename):
        logout("File not found.")
        return

    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        term, definition, mistakes = line.strip("\n").split("\t")
        cards[term] = [definition, int(mistakes)]

    logout(f"{len(lines)} cards have been loaded.")

def remove_card(cards):
    logout("Which card?")
    term = loginput()
    if term in cards: 
        del cards[term]
        logout("The card has been removed.")
    else:
        logout(f'Can\'t remove "{term}": there is no such card.')

def export_card(cards, filename=None):
    if not filename:
        logout("File name:")
        filename = loginput()

    text = ""
    for term, value in cards.items():
        definition, mistakes = value
        text += f"{term}\t{definition}\t{mistakes}\n"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    
    logout(f"{len(cards)} cards have been saved.")

def log_card():
    logout("File name:")
    filename = loginput()

    text = ""
    for line in log:
        text += line + "\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    logout("The log has been saved.")    

def hardest_card(cards):
    mistake_list = [value[1] for value in cards.values()]
    if len(mistake_list) == 0:
        logout("There are no cards with errors.")
        return

    max_mistakes = max(mistake_list)
    if max_mistakes == 0:
        logout("There are no cards with errors.")
        return

    hardest_list = ['"' + term + '"' for term, value in cards.items() if value[1] == max_mistakes]
    if len(hardest_list) == 1:
        term = hardest_list[0]
        logout(f'The hardest card is {term}. You have {max_mistakes} errors answering it')
    else:
        terms = ",".join(hardest_list)
        logout(f'The hardest card are {terms}. You have {max_mistakes} errors answering it')

def reset_stats(cards):
    for value in cards.values():
        value[1] = 0

    logout("Card statistics have been reset.")

def get_arg():
    if len(sys.argv) == 1:
        return None, None
    elif len(sys.argv) == 2:
        arg1 = sys.argv[1].split("=")
        if arg1[0] == "--import_from":
            return arg1[1], None
        else:
            return None, arg1[1]
    elif len(sys.argv) == 3:
        arg1 = sys.argv[1].split("=")
        arg2 = sys.argv[2].split("=")
        if arg1[0] == "--import_from":
            return arg1[1], arg2[1]
        else:
            return arg2[1], arg1[1]

            
if __name__ == "__main__":
    infile, outfile = get_arg()
    cards = {}
    if infile:
        import_card(cards, infile)

    while(True):
        logout("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        action = loginput()
        if action == "add":
            add_card(cards)
        elif action == "remove":
            remove_card(cards)
        elif action == "import":
            import_card(cards)
        elif action == "export":
            export_card(cards)
        elif action == "ask":
            ask_card(cards)
        elif action == "log":
            log_card()
        elif action == "hardest card":
            hardest_card(cards)
        elif action == "reset stats":
            reset_stats(cards)    
        elif action == "exit":
            logout("Bye bye!")
            if outfile:
                export_card(cards, outfile)
            break
        logout("")