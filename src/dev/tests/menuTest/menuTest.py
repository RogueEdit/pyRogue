from colorama import Fore, Style, init
import functions as rogue
import re

init()
version = 'v0.3'
title = f'pyRogue <{version}>'

def strip_color_codes(text):
    """
    Strips ANSI color codes from the text for accurate length calculations.
    """
    ansi_escape = re.compile(r'\x1b\[.*?m')
    return ansi_escape.sub('', text)

def line_fill(line, helper_text='', length=55, fill_char=' ', truncate=False):
    """
    Formats the line to a fixed length by adding fill characters at the end and including optional helper text.
    If the combined length of line and helper_text exceeds the length, it truncates the line and keeps the helper text intact.
    """
    stripped_line = strip_color_codes(line)
    stripped_helper_text = strip_color_codes(helper_text)
    
    total_length = len(stripped_line) + len(stripped_helper_text)
    
    if truncate and total_length > length:
        truncated_length = length - len(stripped_helper_text) - 3  # 3 characters for "..."
        line = line[:truncated_length] + '...'
        stripped_line = strip_color_codes(line)
        total_length = len(stripped_line) + len(stripped_helper_text)

    fill_length = length - total_length
    fill = fill_char * fill_length
    return f"{Style.RESET_ALL}{line}{fill}{helper_text}"

def center_text(text, length=55, fill_char=' '):
    """
    Centers the text within the given length, filling with the specified character.
    """
    stripped_text = strip_color_codes(text)
    total_length = len(stripped_text)
    if total_length >= length:
        return text[:length]
    
    fill_length = length - total_length
    front_fill = fill_char * (fill_length // 2)
    back_fill = fill_char * (fill_length - (fill_length // 2))
    if fill_char == '>':
        back_fill = '<' * (fill_length - (fill_length // 2))
    
    
    return f"{front_fill}{text}{back_fill}"

def initialize_menu(term):
    """
    Initializes and prints the menu based on the provided term list.
    Returns a list of tuples containing valid numbered choices and their associated functions.
    """
    valid_choices = []
    actual_idx = 1
    for item in term:
        if isinstance(item, tuple):
            if item[1] == 'helper':
                print(Fore.GREEN + '* ' + center_text(f' {item[0]} ', 55, '-') + f' {Fore.GREEN}*' + Style.RESET_ALL)
            elif item[1] == 'title':
                print(Fore.GREEN + '* ' + center_text(f' {item[0]} ', 55, '*') + f' {Fore.GREEN}*' + Style.RESET_ALL)
            elif item[1] == 'category':
                print(Fore.LIGHTYELLOW_EX + '* ' + center_text(f' {item[0]} ', 55, '>') + f' {Fore.GREEN}*' + Style.RESET_ALL)
            else:
                text, func = item
                line = f'{actual_idx}: {text[0]}'
                formatted_line = line_fill(line, text[1], 55, ' ', True)
                print(Fore.GREEN + '* ' + formatted_line + f' {Fore.GREEN}*' + Style.RESET_ALL)
                valid_choices.append((actual_idx, func))
                actual_idx += 1
        else:
            print(Fore.YELLOW + '* ' + center_text(item, 55, '*') + ' *' + Style.RESET_ALL)
    
    return valid_choices

def main():
    useWhenDone = f'{Fore.LIGHTYELLOW_EX}(Use when Done)'
    term = [
        (title, 'title'),
        ('Account Actions', 'category'),
        (('Create a backup', ''), rogue.create_backup),
        (('Recover your backup', ''), rogue.restore_backup),
        (('Load Game-Data from server', ''), rogue.get_trainer_data),
        (('Load SaveSlot-Data from server', ''), rogue.get_gamesave_data),
        (('Edit account stats', ''), rogue.edit_account_stats),

        ('Trainer Data Actions', 'category'),
        (('Edit a starter', ''), rogue.edit_starter_separate),
        (('Edit your egg-tickets', ''), rogue.add_ticket),
        (('Edit candies on a starter', ''), rogue.add_candies),
        (('Edit Egg-hatch durations', ''), rogue.edit_hatchWaves),
        (('Generate eggs', ''), rogue.generate_eggs),
        (('Unlock all vouchers', ''), rogue.edit_vouchers),
        (('Unlock all starters', ''), rogue.unlock_all_starters),
        (('Unlock all achievements', ''), rogue.unlock_all_achievements),
        (('Unlock all gamemodes', ''), rogue.unlock_all_gamemodes),
        (('Unlock Everything', ''), rogue.unlock_all_features),

        ('Session Data Actions', 'category'),
        (('Edit CURRENT Pokemon Party', ''), rogue.edit_pokemon_party),
        (('Edit money amount', ''), rogue.edit_money),
        (('Edit pokeballs amount', ''), rogue.edit_pokeballs),
        (('Edit current biome', ''), rogue.edit_biome),

        ('Print game information', 'category'),
        (('Show all Pokemon ID', ''), rogue.print_pokedex),
        (('Show all Biome IDs', ''), rogue.print_biomes),
        (('Show all Move IDs', ''), rogue.print_moves),
        (('Show all Vouchers IDs', ''), rogue.print_vouchers),
        (('Show all Natures IDs', ''), rogue.print_natures),
        (('Show all NaturesSlot IDs', ''), rogue.print_natureSlot),

        ('You can always edit your JSON manually aswell!', 'helper'),
        (('Save data and upload to the Server', useWhenDone), rogue.update_all),
        (('Print help and program information', ''), rogue.print_help),
        (('Logout', ''), rogue.logout),
        (title, 'title'),
    ]

    try:
        while True:
            print('')
            valid_choices = initialize_menu(term)
            user_input = input("Command: ").strip().lower()
            if user_input == 'exit':
                raise KeyboardInterrupt  # Raise KeyboardInterrupt to exit the program
            
            # Handle user input
            if user_input.isdigit():
                choice_index = int(user_input)
                for idx, func in valid_choices:
                    if idx == choice_index:
                        func()  # Call the associated function
                        break
                    elif idx == 'exit':
                        KeyboardInterrupt()
                else:
                    print("Invalid selection. Please choose a valid menu option.")
            else:
                print("Invalid input. Please enter a number.")

    except KeyboardInterrupt:
        print("Program interrupted by user.")

if __name__ == '__main__':
    main()
