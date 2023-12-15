import settings, asyncio, logging

from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, Router
from importlib import import_module
from os import listdir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    datefmt="%d-%m-%Y, %H:%M:%S",
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler()
    ]
)

bot = Bot(token=str(settings.TOKEN))

dp = Dispatcher()
router = Router()

async def load_commands():
    commands = listdir('commands')

    for command in commands:
        command_filename = command.replace('.py', '')
        if command_filename == "__pycache__":
            continue
        
        command_module = import_module("commands.{}".format(command_filename), package="commands")
        
        command_name = getattr(command_module, 'name', None)
        if not command_name:
            raise Exception(f"Specify the 'name' variable in commands/{command_filename}.py")
        
        command_function = getattr(command_module, command_name, None)
        if not command_function:
            continue
        
        is_command_fsm = getattr(command_module, 'is_fsm', None)
        if is_command_fsm:
            form = getattr(command_module, 'Form', None)
            if form:
                form_states = list(form.__dict__["__states__"])
                
                for form_state in form_states:
                    form_state_name = form_state._state
                    
                    form_state_function = getattr(command_module, form_state_name, None)
                    if not form_state_function:
                        raise Exception(f"Implement the '{form_state_name}' function in commands/{command_filename}.py")
                    
                    print(form_state)
                    router.message.register(form_state_function, form_state)
                
                router.message.register(command_function, Command(command_name))
        else:
            dp.message.register(command_function, Command(command_name))
            
        logging.info("command {} was successfully loaded".format(command_name))

async def main():
    await load_commands()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())