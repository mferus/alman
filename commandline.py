import sys
import getopt
import Manager

def usage():
    print("this is help message.\n Thank you mustard.")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "har:s:", ["help", "show-raw", "add", "remove=", "show="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-a", "--add"):
            print("Alias or function?")
            label = input(">")
            print("string which will call an ", label)
            name = input(">")
            print(name, "will do:")
            funk = input(">")
            Manager.Manager(label, name, funk)

        elif o in ("-s", "--show"):
            print(Manager.Manager.shower(a))
        elif o in ("-r", "--remove"):
            print(Manager.Manager.deleter(a))
        elif o == "--show-raw":
            Manager.Manager.show_raw()
        else:
            assert False, "unhandled option"
    # ...

if __name__ == "__main__":
    main()