import getpass


class Manager:
    objdict = {}
    objlist = []
    objstr = ""
    majorfile = "test"

    #    majorfile = '/home/' + getpass.getuser() + '/.bashrc'

    def __init__(self, label, name, funk):
        self.label = label
        self.name = name
        self.funk = funk
        Manager.objdict[name] = self
        Manager.objlist.append(self)
        Manager.checker(self)

    def shortstr(self):
        return "{} {}".format(self.label, self.name)

    def __str__(self):
        if self.label == 'alias':
            return "\n{} {}={}\n".format(self.label, self.name, self.funk)
        elif self.label == 'function':
            return "\n{} {} {}\n".format(self.label, self.name, self.funk)

    def __repr__(self):
        var = ""
        if self.label == 'alias':
            var = 'Switches to'
        elif self.label == 'function':
            var = 'Functionality'
        return "\n {}: {} \n> {}: \n {} \n".format(self.label, self.name, var, self.funk)

    def checker(self):
        with open(Manager.majorfile, 'r+') as myfile:
            data = myfile.read()
            shortstr = str(self.shortstr)
            if shortstr in data:
                pass
            elif shortstr not in data:
                myfile.write(self.__str__())

    def shower(self):
        Manager.reader()
        return Manager.objdict[self].__repr__()

    @staticmethod
    def show_raw():
        with open(Manager.majorfile, 'r') as myfile:
            return myfile.read()

    @staticmethod
    def reader():
        with open(Manager.majorfile, 'r') as myfile:
            data = myfile.read()
            varstr = ""
            counter, alflag, funflag = 0, 0, 0
            while counter != (len(data)):
                varstr += (data[counter])
                aliasConEnd = varstr.replace(' ', '').endswith('"\n')
                aliasConStart = varstr.startswith('alias')
                funkConEnd = varstr.replace(' ', '').endswith('}\n')
                funkConStart = varstr.startswith('function')
                checker = data[counter]
                counter += 1
                if alflag == 1:
                    if aliasConEnd:
                        vararr = ((varstr.replace(' ', '=', 1)).split('='))
                        Manager(vararr[0], vararr[1], vararr[2])
                        varstr = ""
                        alflag = 0
                elif funflag == 1:
                    if funkConEnd:
                        vararr = ((varstr.replace(' ', '=', 2)).split('='))
                        Manager(vararr[0], vararr[1], vararr[2])
                        varstr = ""
                        funflag = 0
                elif checker == '\n':
                    if aliasConStart:
                        if aliasConEnd:
                            vararr = ((varstr.replace('\n', '').replace(' ', '=', 1)).split('='))
                            Manager(vararr[0], vararr[1], vararr[2])
                            varstr = ""
                        else:
                            alflag = 1
                    elif funkConStart:
                        if funkConEnd:
                            vararr = ((varstr.replace('\n', '').replace(' ', '=', 2)).split('='))
                            Manager(vararr[0], vararr[1], vararr[2])
                            varstr = ""
                        else:
                            funflag = 1
                    else:
                        varstr = ""

    def deleter(self):
        Manager.reader()
        for count in range(len(Manager.objlist)):
            if Manager.objdict[self] == Manager.objlist[count]:
                Manager.delwriter(Manager.objlist[count])
                Manager.objlist.pop(count)
                return "Deleted!"

    @classmethod
    def parser(cls):
        preobj = []
        for x in range(len(cls.objlist)):
            if cls.objlist[x].label == 'alias':
                strobj = "{} {}={}\n".format(cls.objlist[x].label, cls.objlist[x].name, cls.objlist[x].funk)
                preobj.append(strobj)
            if cls.objlist[x].label == 'function':
                strobj = "{} {} {}\n".format(cls.objlist[x].label, cls.objlist[x].name, cls.objlist[x].funk)
                preobj.append(strobj)
        return preobj

    def delwriter(self):
        with open(Manager.majorfile, 'r') as myfile:
            preobj = Manager.parser()
            data = myfile.read()
            varstr = ""
            varlist = []
            counter, objcount, alflag, funflag, doflag = 0, 0, 0, 0, 0
            while counter != (len(data)):
                varstr += (data[counter])
                aliasConEnd = varstr.replace(' ', '').endswith('"\n')
                aliasConStart = varstr.startswith('alias')
                funkConEnd = varstr.replace(' ', '').endswith('}\n')
                funkConStart = varstr.startswith('function')
                checker = data[counter]
                counter += 1
                if alflag == 1:
                    if aliasConEnd:
                        varstr = ""
                        varlist.append(preobj[objcount])
                        objcount += 1
                        alflag = 0
                elif funflag == 1:
                    if funkConEnd:
                        varstr = ""
                        varlist.append(preobj[objcount])
                        objcount += 1
                        funflag = 0
                elif doflag == 2:
                    if funkConStart and funkConEnd:
                        objcount += 1
                        varstr = ""
                        doflag = 0
                    elif aliasConStart and aliasConEnd:
                        objcount += 1
                        varstr = ""
                        doflag = 0
                elif checker == '\n':
                    if aliasConStart:
                        if self.shortstr in varstr:
                            if aliasConEnd:
                                varstr = ""
                                objcount += 1
                            else:
                                doflag = 2
                        elif aliasConEnd:
                            varstr = ""
                            varlist.append(preobj[objcount])
                            objcount += 1
                        else:
                            alflag = 1
                    elif funkConStart:
                        if self.shortstr in varstr:
                            if funkConEnd:
                                varstr = ""
                                objcount += 1
                            else:
                                doflag = 2
                        elif funkConEnd:
                            varstr = ""
                            varlist.append(preobj[objcount])
                            objcount += 1
                        else:
                            funflag = 1
                    else:
                        varlist.append(varstr)
                        varstr = ""
            Manager.objstr = ''.join(varlist)
            text_file = open(Manager.majorfile, 'w')
            text_file.write(Manager.objstr)
            text_file.close()
