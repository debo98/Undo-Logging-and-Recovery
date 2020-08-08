import sys

class Undo:
    def __init__(self, fileName, roundRobinCounter):
        self.lines = []
        with open(fileName, 'r') as fd:
            self.lines = fd.readlines()
        self.roundRobinCounter = roundRobinCounter
        self.main_var = {}
        self.sec_var = {}
        self.ram = {}
        self.disk = {}
        self.transactions = [[]]
        self.now = []
        self.curr_t = 1
        self.TOT = 0
    
    def parseContent(self):
        tid = 1	
        for i in range(len(self.lines)):
            if len(self.lines[i]) == 1:
                j = i + 1
                tempList = []
                while j < len(self.lines) and len(self.lines[j]) != 1:
                    tempList.append(self.lines[j].strip('\n').split(' '))
                    j+=1
                self.transactions.append(tempList)
                del self.transactions[tid][0:1]	
                tid += 1
                i = j
            else:
                if i == 0:
                    for j in range(0, len(self.lines[i].split(' ')), 2):
                        self.main_var[self.lines[i].split(' ')[j]] = int(self.lines[i].split(' ')[j+1])	
                        self.disk[self.lines[i].split(' ')[j]] = int(self.lines[i].split(' ')[j+1])
                i+=1


        for i in range(1, len(self.transactions)):
            for j in range(len(self.transactions[i])):
                tmp = []
                
                if 'READ' in self.transactions[i][j][0]:
                    tmp.append('R')
                    x = self.transactions[i][j][0]
                    x = x.split('(')
                    x = x[1]
                    x = x.split(')')
                    x = x[0]
                    x = x.split(',')
                    temp = []
                    for element in x:
                        temp.append(element.strip(' '))
                    x = temp
                    if x[0] not in self.main_var:
                        self.sec_var[x[0]] = '-'
                    if x[1] not in self.main_var:
                        self.sec_var[x[1]] = '-'	
                    tmp.append(x[0])
                    tmp.append(x[1])
                    self.transactions[i][j] = tmp
                elif 'WRITE' in self.transactions[i][j][0]:			
                    tmp.append('W')
                    x = self.transactions[i][j][0]
                    x = x.split('(')
                    x = x[1]
                    x = x.split(')')
                    x = x[0]
                    x = x.split(',')
                    temp = []
                    for element in x:
                        temp.append(element.strip(' '))
                    x = temp
                    if x[0] not in self.main_var:
                        self.sec_var[x[0]]='-'
                    if x[1] not in self.main_var:
                        self.sec_var[x[1]]='-'
                    tmp.append(x[0])
                    tmp.append(x[1])
                    self.transactions[i][j]=tmp		
                elif 'OUTPUT' in self.transactions[i][j][0]:
                    tmp.append('O')                    
                    x = self.transactions[i][j][0]
                    x = x.split('(')
                    x = x[1]
                    x = x.split(')')
                    x = x[0]
                    x = x.split(',')
                    temp = []
                    for element in x:
                        temp.append(element.strip(' '))
                    x = temp
                    if x[0] not in self.main_var:
                        self.sec_var[x[0]]='-'
                    tmp.append(x[0])
                    self.transactions[i][j] = tmp		
                else:
                    tmp.append('V')
                    tmp.append(self.transactions[i][j][0])
                    signs = ['-','+','/','*']
                    
                    for s in signs:
                        if s in self.transactions[i][j][2]:
                            tmp.append(s)
                            break
                    tmp.append(int(self.transactions[i][j][2][len(self.transactions[i][j][2])-1]))
                    self.transactions[i][j] = tmp		
        for i in self.transactions:
            self.now.append(0)

    def addLog(self, string):
        print(string)
        out1 = []
        out2 = []
        for key in self.ram:
            if key in self.main_var:
                out2.append([key, self.ram[key]])	
        for key in self.disk:
            out1.append([key, self.disk[key]])

        out2.sort(key = lambda x:x[0])	
        idx = 0
        for i in out2:
            if idx == len(out2) - 1:
                print(i[0], i[1], end = '')
                break
            print(i[0], i[1], end = ' ')
            idx += 1		
        print()	
        idx = 0
        out1.sort(key = lambda x:x[0])	
        for i in out1:
            if idx == len(out1) - 1:
                print(i[0], i[1], end = '')
                break
            print(i[0], i[1], end = ' ')
            idx += 1		
        print()	
    
    def exec(self):
        while True:
            if self.TOT == (len(self.transactions)-1):
                break
            if self.curr_t >= len(self.transactions):
                self.curr_t = 1		          
            if self.now[self.curr_t] == 0:
                self.addLog('<START T' + str(self.curr_t) + '>')

            for i in range(self.now[self.curr_t], min(len(self.transactions[self.curr_t]),self.now[self.curr_t] + roundRobinCounter)):
                comm = self.transactions[self.curr_t][i]
                if comm[0] == 'R':
                    if comm[1] in self.ram:
                        self.ram[comm[2]] = self.ram[comm[1]]
                        self.sec_var[comm[2]] = self.ram[comm[1]]
                        self.ram[comm[1]] = self.ram[comm[1]]
                        self.main_var[comm[1]] = self.ram[comm[1]]
                    else:	
                        self.ram[comm[2]] = self.disk[comm[1]]
                        self.sec_var[comm[2]] = self.disk[comm[1]]
                        self.ram[comm[1]] = self.disk[comm[1]]
                        self.main_var[comm[1]] = self.disk[comm[1]]
                        
                if comm[0] == 'W':	
                    string = '<T'+str(self.curr_t)+', '+str(comm[1])+', ' + str(self.main_var[comm[1]])+'>'
                    self.main_var[comm[1]] = self.sec_var[comm[2]]
                    self.ram[comm[1]] = self.sec_var[comm[2]]
                    self.addLog(string)
                elif comm[0]=='O':
                    self.disk[comm[1]] = self.ram[comm[1]]		
                elif comm[0] == 'V':
                    if comm[2] == '+':
                        self.sec_var[comm[1]] += comm[3]
                    elif comm[2] == '-':
                        self.sec_var[comm[1]] -= comm[3]
                    elif comm[2] == '*':
                        self.sec_var[comm[1]] = self.sec_var[comm[1]]*comm[3]
                    elif comm[2]=='/':
                        self.sec_var[comm[1]] = self.sec_var[comm[1]]/comm[3]
                    self.ram[comm[1]]=self.sec_var[comm[1]]
                if i == len(self.transactions[self.curr_t])-1:
                    self.addLog('<COMMIT T'+str(self.curr_t)+'>')
                    self.TOT += 1
            self.now[self.curr_t] += roundRobinCounter
            self.curr_t+=1

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) == 3:
        fileName = arguments[1]
        roundRobinCounter = int(arguments[2])
        obj = Undo(fileName, roundRobinCounter)
        obj.parseContent()
        obj.exec()
    else:
        print("Input Error")
        exit(0)