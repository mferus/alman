class Statement:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return f'{self.content}'


class Alias(Statement):
    def __init__(self, name, command):
        super().__init__(self)
        self.name = name
        self.command = command

    def __repr__(self):
        return f'alias {self.name}={self.command}'


class Function(Statement):
    def __init__(self, name, body):
        super().__init__(self)
        self.name = name
        self.body = body

    def __repr__(self):
        return f'function {self.name} {self.body}'


class Bashrc:
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def get_functions(self):
        function_list = []
        for statement in self.statement_list:
            if isinstance(statement, Function):
                function_list.append(statement)
        return function_list

    def get_aliases(self):
        alias_list = []
        for statement in self.statement_list:
            if isinstance(statement, Alias):
                alias_list.append(statement)
        return alias_list

    def get_alias(self, alias):
        for statement in self.statement_list:
            if not hasattr(statement, 'name'):
                continue
            elif alias == statement.name:
                return statement

    def get_function(self, function):
        for statement in self.statement_list:
            if not hasattr(statement, 'name'):
                continue
            elif function == statement.name:
                return statement
        return

    def add_alias(self, alias):
        self.statement_list.append(alias)
        return 0

    def add_function(self, function):
        self.statement_list.append(function)
        return 0

    def delete_function(self, function):
        for statement in self.statement_list:
            if not isinstance(statement, Function):
                continue
            elif function == statement.name:
                self.statement_list.remove(statement)
                return 0
        return None

    def delete_alias(self, alias):
        for statement in self.statement_list:
            if not isinstance(statement, Alias):
                continue
            elif alias == statement.name:
                self.statement_list.remove(statement)
                return 0
        return None


class BashrcParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(directory):
        with open(directory, 'r') as my_file:
            data = my_file.read()
            working_string = ""
            statement_list = []
            counter, alias_flag, function_flag = 0, 0, 0
            while counter != (len(data)):
                working_string += (data[counter])
                alias_ending_condition = working_string.replace(' ', '').endswith('"\n')
                alias_start_condition = working_string.startswith('alias')
                function_ending_condition = working_string.replace(' ', '').endswith('}\n')
                function_start_condition = working_string.startswith('function')
                checker = data[counter]
                counter += 1
                if alias_flag == 1:
                    if alias_ending_condition:
                        working_array = (working_string.replace(' ', '=', 1)).split('=')
                        alias = Alias(working_array[1], working_array[2])
                        statement_list.append(alias)
                        working_string = ""
                        alias_flag = 0
                elif function_flag == 1:
                    if function_ending_condition:
                        working_array = (working_string.replace(' ', '=', 2)).split('=')
                        created_function = Function(working_array[1], working_array[2])
                        statement_list.append(created_function)
                        working_string = ""
                        function_flag = 0
                elif checker == '\n':
                    if alias_start_condition:
                        if alias_ending_condition:
                            working_array = (working_string.replace(' ', '=', 1)).split('=')
                            alias = Alias(working_array[1], working_array[2])
                            statement_list.append(alias)
                            working_string = ""
                        else:
                            alias_flag = 1
                    elif function_start_condition:
                        if function_ending_condition:
                            working_array = (working_string.replace(' ', '=', 2)).split('=')
                            created_function = Function(working_array[1], working_array[2])
                            statement_list.append(created_function)
                            working_string = ""
                        else:
                            function_flag = 1
                    else:
                        statement = Statement(working_string)
                        statement_list.append(statement)
                        working_string = ""

            return Bashrc(statement_list)


class BashrcSerializer:
    def __init__(self):
        pass

    @staticmethod
    def serialize(bashrc, directory):
        with open(directory, 'a') as bashrc_file:
            bashrc_file.seek(0)
            bashrc_file.truncate()
            for statement in bashrc.statement_list:
                bashrc_file.write(statement.__repr__())


class BashrcParserError(Exception):
    pass


class ObjectNotFoundError(BashrcParserError):
    pass
