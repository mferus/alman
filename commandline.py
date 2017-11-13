import argparse
import alman

alman_parser = alman.BashrcParser()
directory = 'test'
bashrc = alman_parser.parse(directory)

parser = argparse.ArgumentParser(description='Alman is file manager for bashrc file')
views = parser.add_mutually_exclusive_group()
add_and_delete = parser.add_mutually_exclusive_group()

views.add_argument("--show-aliases", help="Show aliases",
                   action="store_true"
                   )
views.add_argument("--show-functions", help="Show functions",
                   action="store_true"
                   )
views.add_argument("--all", help="Show all aliases and functions",
                   action="store_true"
                   )
views.add_argument("--show-alias", help="Show specific alias",
                   metavar="<name>"
                   )
views.add_argument("--show-function", help="Show specific function",
                   metavar="<name>"
                   )

add_and_delete.add_argument("--add-alias",
                            help="Add alias to bashrc file. "
                                 "Example: "
                                 "alman --add-alias vi vim", nargs=2,
                            metavar=("<name>", "<command>")
                            )
add_and_delete.add_argument("--add-function",
                            help="Add function to bashrc file. "
                                 "Example: "
                                 "alman --add-function 'clds' 'cl; cd \"$@\" && ls;'", nargs=2,
                            metavar=("<name>", "<body>")
                            )
add_and_delete.add_argument("--remove-alias",
                            help="Remove alias from bashrc file",
                            metavar="<name>"
                            )
add_and_delete.add_argument("--remove-function",
                            help="Remove function from bashrc file",
                            metavar="<name>"
                            )

args = parser.parse_args()

# Views
if args.show_aliases:
    for alias in bashrc.get_aliases():
        print(f' Alias: {alias.name}\n > {alias.command}')

elif args.show_functions:
    for function in bashrc.get_functions():
        print(f' Function: {function.name}\n > {function.body}')

elif args.all:
    print('-- Aliases --\n')
    for alias in bashrc.get_aliases():
        print(f' Alias: {alias.name}\n > {alias.command}')
    print('-- Functions --\n')
    for function in bashrc.get_functions():
        print(f' Function: {function.name}\n > {function.body}')

elif args.show_alias:
    alias = bashrc.get_alias(args.show_alias)
    if alias is None:
        print(f'Alias {args.show_alias} could not be found')
    else:
        print(alias.__repr__())

elif args.show_function:
    function = bashrc.get_function(args.show_function)
    if function is None:
        print(f'Function {args.show_function} could not be found')
    else:
        print(function.__repr__())

# Add

elif args.add_alias:
    check_alias = bashrc.get_alias(args.add_alias[0])
    if check_alias is not None:
        print(f'Alias {args.add_alias} already exist.')
    command = f'"{args.add_alias[0]}"'
    alias = alman.Alias(args.add_alias[1], command)
    bashrc.add_alias(alias)
    serializer = alman.BashrcSerializer()
    serializer.serialize(bashrc, directory)


elif args.add_function:
    check_function = bashrc.get_function(args.add_function[0])
    if check_function is not None:
        print(f'Function {args.add_function} already exist.')
    name = f'{args.add_function[0]}()'
    body = '{ ' + args.add_function[1] + ' }'
    function = alman.Function(name, body)
    bashrc.add_function(function)
    serializer = alman.BashrcSerializer()
    serializer.serialize(bashrc, directory)

# Delete

elif args.remove_alias:
    if bashrc.delete_alias(args.remove_alias) is None:
        print(f'Alias {args.remove_alias} could not be found')
    else:
        serializer = alman.BashrcSerializer()
        serializer.serialize(bashrc, directory)
elif args.remove_function:
    if bashrc.delete_function(args.remove_function) is None:
        print(f'Function {args.remove_function} could not be found')
    else:
        serializer = alman.BashrcSerializer()
        serializer.serialize(bashrc, directory)
