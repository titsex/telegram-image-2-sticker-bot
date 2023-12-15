from importlib import import_module
from os import listdir
from aiogram import types

name = "help"
description = "the command that displays the capabilities of the bot"
is_fsm = False

async def help(message: types.Message):
    command_list = dict()
    
    commands = listdir('commands')

    for command in commands:
        command_filename = command.replace('.py', '')
        if command_filename == "__pycache__":
            continue
        
        command_module = import_module("commands.{}".format(command_filename), package="commands")
        command_name = getattr(command_module, 'name', None)
        command_description = getattr(command_module, 'description', None)
        
        if command_name and command_description:
            command_list[command_name] = command_description
            
    answer = "List of bot commands:\n\n"
    
    for name in command_list:
        answer += "/{} - {}\n".format(name, command_list[name])
    
    await message.reply(answer)