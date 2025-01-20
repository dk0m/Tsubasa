from dataclasses import dataclass

@dataclass
class Colors:

    purple = '\001\033[0;38;5;141m\002'
    blue = '\001\033[0;38;5;12m\002'
    gray = '\033[90m'
    red = '\001\033[1;31m\002'
    green = '\001\033[38;5;82m\002'
    orange = '\001\033[0;38;5;214m\002'

    underline = '\001\033[4m\002'
    end = '\001\033[0m\002'


@dataclass
class Symbols:
    success = f'{Colors.gray}[{Colors.end}{Colors.green}+{Colors.end}{Colors.gray}]{Colors.end}'
    failure = f'{Colors.gray}[{Colors.end}{Colors.red}-{Colors.end}{Colors.gray}]{Colors.end}'
    info = f'{Colors.gray}[{Colors.end}{Colors.blue}*{Colors.end}{Colors.gray}]{Colors.end}'
    question = f'{Colors.gray}[{Colors.end}{Colors.blue}?{Colors.end}{Colors.gray}]{Colors.end} %s {Colors.gray}»{Colors.end} '

class Prompt:

    @staticmethod
    def success(message: str):
        print(f'{Symbols.success} {message}')

    @staticmethod
    def failure(message: str):
        print(f'{Symbols.failure} {message}')

    @staticmethod
    def info(message: str):
        print(f'{Symbols.info} {message}')


    @staticmethod
    def ask(question: str):
        try:
            answer = input(Symbols.question % question)
            if (answer.strip() == ''):
                return Prompt.ask(question)
            else:
                return answer
            
        except (KeyboardInterrupt):
            Prompt.info('Exiting...')
            exit(0)
