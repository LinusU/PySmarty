#!/usr/bin/env python3
#coding: UTF-8
#

import re

def parse_condition(condition):
    
    ret = list()
    parts = condition.split(" ")
    
    for part in parts:
        if part.startswith("$"):
            ret.append('self.vars["' + part[1:] + '"]')
        else:
            ret.append(part)
    
    return (' '.join(ret))

def ldelim(tag_arg, template): return (' ' * template.indentation) + "self.send('{')"
def rdelim(tag_arg, template): return (' ' * template.indentation) + "self.send('}')"

def start_if(tag_arg, template):
    template.indentation += 1
    return (' ' * (template.indentation - 1)) + 'if ' + parse_condition(tag_arg) + ':'

def start_elseif(tag_arg, template):
    return (' ' * (template.indentation - 1)) + 'elif ' + parse_condition(tag_arg) + ':'

def start_else(tag_arg, template):
    return (' ' * (template.indentation - 1)) + 'else:'

def start_for(tag_arg, template):
    template.indentation += 1
    
    r = re.match('\$([a-zA-Z0-9_]+)=(-?)(\$[a-zA-Z0-9_]+|[0-9]+)\ to\ (-?)(\$[a-zA-Z0-9_]+|[0-9]+)(\ step\ (-?)(\$[a-zA-Z0-9_]+|[0-9]+))?', tag_arg)
    
    if r:
        return (
            (' ' * (template.indentation - 1)) +
            'for self.vars["' + r.group(1) + '"] in range(' +
            r.group(2) + (r.group(3) if not r.group(3).startswith('$') else 'self.vars["' + r.group(3)[1:] + '"]') + ', ' +
            r.group(4) + (r.group(5) if not r.group(5).startswith('$') else 'self.vars["' + r.group(5)[1:] + '"]') + 
            ('' if not r.group(6) else (', ' + r.group(7) + (r.group(8) if not r.group(8).startswith('$') else 'self.vars["' + r.group(8)[1:] + '"]'))) +
            '):'
        )
    else:
        return (' ' * (template.indentation - 1))

def start_foreach(tag_arg, template):
    template.indentation += 1
    
    r = re.match('\$([a-zA-Z0-9_]+)\ as\ (\$([a-zA-Z0-9_]+)=>)?\$([a-zA-Z0-9_]+)', tag_arg)
    
    if r:
        return (' ' * (template.indentation - 1)) + ((
            'for self.vars["' + r.group(3) + '"], self.vars["' + r.group(4) + '"] in enumerate(self.vars["' + r.group(1) + '"]):'
        ) if r.group(3) else (
            'for self.vars["' + r.group(4) + '"] in self.vars["' + r.group(1) + '"]:'
        ))
    else:
        return (' ' * (template.indentation - 1))

def start_include(tag_arg, template):
    return (' ' * template.indentation)

def end(tag_arg, template):
    template.indentation -= 1
    return (' ' * template.indentation)

functions = {
    'ldelim': ldelim,
    'rdelim': rdelim,
    'if': start_if,
    'elseif': start_elseif,
    'else': start_else,
    '/if': end,
    'for': start_for,
    '/for': end,
    'foreach': start_foreach,
    '/foreach': end
}
