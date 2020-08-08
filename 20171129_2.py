import sys

class UndoR:
    def __init__(self, fileName):
        self.lines = []
        with open(fileName, 'r') as fd:
            self.lines = fd.readlines()
        self.var = {}
        self.F = {}
        self.hold = []
        self.go = 1000000000000
        self.commited = []	
    
    def parseFile(self):
        for line in self.lines:
            if len(line)>1:
                self.hold.append(line)
                self.hold[len(self.hold)-1]=self.hold[len(self.hold)-1].strip('\n')
                self.hold[len(self.hold)-1]=self.hold[len(self.hold)-1].strip('<')
                self.hold[len(self.hold)-1]=self.hold[len(self.hold)-1].strip('>')

        for i in range(len(self.hold)):
            self.hold[i] = self.hold[i].split(' ')
            for j in range(len(self.hold[i])):
                self.hold[i][j]=self.hold[i][j].strip(',')	
                self.hold[i][j]=self.hold[i][j].strip(')')	
                self.hold[i][j]=self.hold[i][j].strip('(')	

        for i in range(1,len(self.hold[0]),2):
            self.var[self.hold[0][i-1]]=int(self.hold[0][i])	

        for i in range(1,len(self.hold)):
            if self.hold[i][0]=='START':
                if len(self.hold[i])==2:
                    tmp=[]
                    tmp.append('S')
                    tmp.append(self.hold[i][1])
                    if self.hold[i][1] not in self.F:
                        tempInd = self.hold[i][1]
                        self.F[tempInd] = i
                else:
                    tmp = ['SC']
                    for j in range(2, len(self.hold[i])):
                        tmp.append(self.hold[i][j])
            elif self.hold[i][0]=='COMMIT':
                tmp = ['C']
                tmp.append(self.hold[i][1])
            elif self.hold[i][0 ]== 'END':
                tmp = ['E']
            else:
                tmp=['V']
                tmp.append(self.hold[i][0])
                tmp.append(self.hold[i][1])
                tmp.append(int(self.hold[i][2]))
            self.hold[i]=tmp	

        # for i in self.hold:
        #     print(i)

    def printVar(self):
        out = []
        for key in self.var:
            out.append([key, self.var[key]])
        idx = 0  
        out.sort(key=lambda x:x[0])
        for i in out:
            print(i[0], i[1], end = '')
            if idx < (len(out)-1):
                print(' ', end = '')
            idx += 1	
        print('')		

    def exec(self):
        check=0
        for i in range(len(self.hold)-1,0,-1):
            if self.hold[i][0]=='S':
                if i == self.go:
                    break
            if self.hold[i][0]=='SC':
                if check != 1:
                    for j in range(1, len(self.hold[i])):
                        if(self.go > self.F[self.hold[i][j]]):
                            self.go = self.F[self.hold[i][j]]
                else:
                    break
                        
            if self.hold[i][0]=='E':
                check=1
            if self.hold[i][0]=='C':
                self.commited.append(self.hold[i][1])
            if self.hold[i][0]=='V':
                if self.hold[i][1] not in self.commited:
                    self.var[self.hold[i][2]]=self.hold[i][3]

if __name__== "__main__":

    arguments = sys.argv

    if(len(arguments) == 2):
        fileName = arguments[1]
        obj = UndoR(fileName)
        obj.parseFile()
        obj.exec()
        obj.printVar()
    else:
        print("ERROR")
        exit()