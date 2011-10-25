#!/usr/bin/env python3
#coding: UTF-8
#

import Compiler

def apply_modifiers(text, modifiers):
    r = ""
    for m in modifiers: r += "Modifier." + m + "("
    r += text
    for m in modifiers: r += ")"
    return r

class Template:
    
    def __init__(self, file):
        
        self.file = file
        self.indentation = 2
        
    
    def parse(self):
        
        f = open('test.py', 'w')
        
        f.write('#!/usr/bin/env python3\n')
        f.write('#coding: UTF-8\n')
        f.write('import Modifier\n')
        f.write('class Template:\n')
        f.write(' def __init__(self, **kwargs):\n')
        f.write('  self.vars = kwargs\n')
        f.write(' def send(self, str):\n')
        f.write('  print(str, end="")\n')
        f.write(' def render(self):\n')
        f.write('  self.send("""')
        
        command = None
        variable_name = None
        variable_assign = None
        variable_modifiers = list()
        compiler_function = None
        text = ''
        
        c = self.file.read(1)
        next = self.file.read(1)
        
        while c:
            
            if c == '\r':
                continue
            
            if command is None:
                
                if c == '{':
                    if next in (' ', '\t', '\r', '\n'):
                        text += c
                    elif next == '$':
                        command = 'variable'
                        variable_name = None
                        variable_assign = None
                        variable_modifiers = list()
                        c, next = next, self.file.read(1)
                    else:
                        command = 'compiler'
                        compiler_function = None
                elif c == '\n':
                    f.write(text + '\\n')
                    text = ''
                elif c == '\\':
                    text += '\\\\'
                elif c == next == '"':
                    
                    c, next = next, self.file.read(1)
                    
                    text += '"' + c
                    
                    if '"' == c == next:
                        next = '\\"'
                    
                else:
                    text += c
                
                if command is not None:
                    f.write(text if not text.endswith('"') else (text[:-1]+'\\"'))
                    f.write('""")\n');
                    text = ''
                
            elif command == 'variable':
                
                if c == '=':
                    variable_assign, text = text, ''
                elif c == '|':
                    if variable_name is None:
                        variable_name, text = text, ''
                    else:
                        variable_modifiers.insert(0, text)
                        text = ''
                elif c == '}':
                    
                    if variable_name is None:
                        variable_name = text
                    elif len(text):
                        variable_modifiers.insert(0, text)
                    
                    f.write(' ' * self.indentation)
                    if variable_assign is None:
                        f.write('self.send(' + apply_modifiers('self.vars["' + variable_name + '"]', variable_modifiers) + ')\n')
                    elif text.startswith('$'):
                        f.write('self.vars["' + variable_assign + '"] = ' + apply_modifiers('self.vars["' + variable_name + '"]', variable_modifiers) + '\n')
                    else:
                        f.write('self.vars["' + variable_assign + '"] = """' + text + '"""\n')
                    
                    f.write(' ' * self.indentation)
                    f.write('self.send("""')
                    
                    command = None
                    text = ''
                    
                else:
                    text += c
                
            elif command == 'compiler':
                
                if c == '}':
                    
                    if compiler_function is None:
                        compiler_function, text = text, ""
                    
                    f.write(Compiler.functions[compiler_function](text, self) + '\n')
                    f.write(' ' * self.indentation)
                    f.write('self.send("""')
                    
                    if next == '\n':
                        c, next = next, self.file.read(1)
                    
                    command = None
                    text = ''
                    
                elif c == ' ' and compiler_function is None:
                    compiler_function = text
                    text = ''
                else:
                    text += c
                
            
            c, next = next, self.file.read(1)
        
        f.write('""")');
        f.close()
        
    

Template(open("test.tpl")).parse()
