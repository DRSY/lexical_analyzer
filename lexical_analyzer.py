import ply.lex as lex
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox

#reserved tokens
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'do' : 'DO',
    'switch' : 'SWITCH',
    'case' : 'CASE',
    'break' :'BREAK',
    'continue' : 'CONOTINUE',
    'void' : 'VOID',
    'char' : 'CHAR',
    'short' : 'SHORT',
    'int' : 'INT',
    'double' : 'DOUBLE',
    'float' : 'FLOAT',
    'long' : 'LONG',
    'return' : 'RETURN',
    'main' : 'MAIN',
    'class' : 'CLASS',
    'const' : 'CONST',
    'static' : 'STATIC',
    'printf' : 'PRINTF',
    'scanf' : 'SCANF',
}

# List of token names.
tokens = [
    'ID',         #标识符
    'NUMBER',     #整数
    'NUMERIC',    #浮点数
    'PLUS',       #加号 +
    'MINUS',      #减号 -
    'TIMES',      #乘号 *
    'DIVIDE',     #除号 /
    'MOD',        #模运算符号 %
    'LPAREN',     #左小括号
    'RPAREN',     #右小括号
    'EQUAL',      #等号
    'GREATER',    #大于号
    'SMALLER',    #小于号
    'COLON',       #分号
    'STRING',      #字符串
    'CHARACTER',   #单个字符
    'GREATEREQ',    #大于等于号
    'SMALLEREQ',    #小于等于号
    'SELFPLUS',     #++
    'SELFMINUS',    #--
    'MINUSEQ',      #-=
    'PLUSEQ',       #+=
    'TIMESEQ',      #*=
    'DIVIDEEQ',     #/=
    'MODEQ',        #%=
    'ASSIGN',      #赋值号
    'LBRACE',    #左花括号
    'RBRACE',   #右花括号
    'LBRACKET',  #左中括号
    'RBRACKET',  #右中括号
    'COMMENT',    #注释
    'PREPROCESS',  #预处理指令
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SELFPLUS = r'\+\+'
t_SELFMINUS = r'--'
t_PLUSEQ = r'\+='
t_MINUSEQ = r'-='
t_TIMESEQ = r'\*='
t_MODEQ = r'%='
t_DIVIDEEQ = r'/='
t_GREATEREQ = r'>='
t_SMALLEREQ = r'<='
t_EQUAL = r'=='
t_GREATER = r'>'
t_SMALLER = r'<'
t_COLON = r';'
t_ASSIGN = r'='


# A regular expression rule with some action code
def t_COMMENT(t):
    r'//.*'
    pass

def t_PREPROCESS(t):
    r'\#.*'
    pass

def t_STRING(t):
    r'".*"'
    t.value = str(t.value)
    return t

def t_CHARACTER(t):
    r"'[a-zA-Z]'"
    t.value = str(t.value)
    return t

def t_NUMERIC(t):
    r'\d+\.\d*'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'([a-zA-Z]|_)([a-zA-Z]|\d|_)*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print('Illegal character{0} line:{1}'.format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)


class myWindow(Tk):

    def __init__(self):
        super().__init__()
        self.lexer = lex.lex()
        self.setUI()

    def lexical_analyze(self, filepath):
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
                occur = False
                auxilary = []

                # 处理多行注释
                for index, line in enumerate(lines):
                    if occur == False:
                        if line.find(r'/*') != -1:
                            occur = True
                            auxilary.append(False)
                        else:
                            auxilary.append(True)
                    else:
                        if line.find(r'*/') != -1:
                            occur = False
                            auxilary.append(False)
                        else:
                            auxilary.append(False)
                new_lines = [lines[i] for i in range(len(lines)) if auxilary[i] == True]

                new_content = ''.join(new_lines)  # 去掉了多行注释的源程序
                self.text2.insert(1.0, new_content)
                self.lexer.input(new_content)
                print('(类型 , 单词符号):')
                result = ''
                while True:
                    tok = self.lexer.token()
                    if not tok:
                        break
                    outputStr = '({} , {})'.format(tok.type, tok.value)
                    result += outputStr + '\n'
                self.textvar.set(result)
                self.text1.insert(1.0, self.textvar.get())
        except:
            tkinter.messagebox.showwarning(title='Warning', message='出错了!')

    def openfile(self):
        filepath = tkinter.filedialog.askopenfilename()
        self.text1.delete(1.0, END)
        self.text2.delete(1.0, END)
        self.lexical_analyze(filepath)

    def setUI(self):
        self.menu = Menu(self)
        self.menu.add_command(label='Open', command=self.openfile)
        self.menu.add_command(label='quit', command=self.quit)
        self.config(menu=self.menu)
        self.title('词法分析器')
        self.geometry('500x600')
        self.topLabel = Label(self, text='Output')
        self.topLabel.pack(side=TOP)
        self.verticalscrollbar = Scrollbar(self, orient = VERTICAL)
        self.text1 = Text(self, width=200, height=20, yscrollcommand=self.verticalscrollbar.set)
        self.verticalscrollbar.config(command = self.text1.yview)
        self.verticalscrollbar.pack(fill = 'y', side = RIGHT, anchor = N)
        self.text1.pack()
        self.codelabel = Label(self, text='Code')
        self.codelabel.pack()
        self.text2 = Text(self, width=200, height=30)
        self.text2.pack()
        self.textvar = StringVar()
        self.mainloop()


if __name__ == '__main__':
    window = myWindow()