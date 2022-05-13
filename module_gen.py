#!/usr/bin/python3

import sys, re
from pprint import pp


builtintypes = ['Bool', 'Int', 'Float', 'ID', 'Map']
# true functions, always return a value
builtinfun = ['eq', 'neq', 'lt', 'leq', 'gt', 'geq',
              'notb', 'andb', 'orb', 'printb',
              'addi', 'subi', 'muli', 'divi', 'printi',
              'addf', 'subf', 'mulf', 'divf', 'printf', 'bind ']
metavarre = re.compile('[a-z][0-9\']*$')
typere = re.compile('|'.join(builtintypes + ['[a-z][0-9\']*$']))


def process_typetoks(typetoks):
  # replace map type with assoc list and remove numbers/primes from metavars
  for j in range(len(typetoks) - 1, -1, -1):
    if typetoks[j] == 'map':
      typetoks[j] = '(({} * {}) list)'.format(typetoks[j+1], typetoks[j+2])
      del typetoks[j+1:j+3]
    elif typetoks[j] == 'id':
      typetoks[j] = 'string'
    elif metavarre.match(typetoks[j]):
      typetoks[j] = typetoks[j][0]


def process_syntok(tok):
  if tok in builtintypes:
    return tok.upper()
  if metavarre.match(tok):
    return tok[0]
  if tok[0] == '\\':
    return tok[1:]
  return tok


def split_list_on_elems(l, s, keep_delin=False):
  offset = 0 if keep_delin else 1
  splits = [i for (i, e) in enumerate(l) if e in s] + [None]
  return [l[splits[i]+offset:splits[i+1]] for i in range(len(splits) - 1)]


if len(sys.argv) != 2:
  print('Usage: module_gen.py <sem>')
  sys.exit(1)

# Read in semantics (.sem file)
fname = sys.argv[1]

sem = ''
with open('{}.sem'.format(fname), 'r') as f:
  for line in f.readlines():
    if line[0] != '#':
      sem += line

# Tokenize semantics
space = re.compile('\s*$')
tok = [s for s in re.split('(\s+|[a-zA-Z0-9_\']+)', sem) if not space.match(s)]

# Split into definitions (type definitions and relation definitions)
defns = split_list_on_elems(tok, ['contype', 'abstype', 'rel'], keep_delin=True)

types = []
contypes = []
syntoks = []
prules = []
rels = []
for defn in defns:
  # handle type definitions
  if defn[0] in ['contype', 'abstype']:
    x = defn[1] # type metavariable (should be a single character)
    s = x + ' = \n'

    con = defn[0] == 'contype'
    if con:
      prules.append([x])
      contypes.append(x)

    # split into variants
    variants = split_list_on_elems(defn, ['|'])

    for variant in variants:
      s += '  | ' + variant[0]

      typetoks = []
      if con:
        syntax = []
        indices = []

      for i, tok in enumerate(variant[1:]):
        if typere.match(tok):
          typetoks.append(tok.lower())

          if con:
            indices.append(i + 1)
            syntax.append(process_syntok(tok))

        elif con:
          ptok = process_syntok(tok)
          if ptok not in syntoks:
            syntoks.append(ptok)
          
          syntax.append('TOK' + str(syntoks.index(ptok)))

      if con:
        if len(indices) == 0:
          semstr = ' { ' + variant[0] + ' } '
        else:
          semstr = ' { ' + variant[0] + ' (' + ', '.join(
            ['$' + str(i) for i in indices]
          ) + ') }'

        prules[-1].append(' '.join(syntax) + semstr)
          

      process_typetoks(typetoks)

      # construct ocaml representation of variant
      if len(typetoks) > 0:
        s += ' of '
      s += ' * '.join(typetoks)
      s += '\n'

    types.append(s)

  # handle relation definitions
  elif defn[0] == 'rel':
    x = defn[1] # name of relation

    arri = defn.index('->')
    bracei = defn.index('{')
    intype = defn[2:arri] # input type
    outype = defn[arri+1:bracei] # output type

    process_typetoks(intype)
    process_typetoks(outype)

    s = '{} : {} -> {} option = function\n'.format(x, intype[0], outype[0])

    # split into rules
    rules = split_list_on_elems(defn[:-1], ['{', ';'])

    for rule in rules:
      arri = rule.index('->')
      pattern = rule[:arri]
      s += '  | {} '.format(' '.join(pattern))

      if 'when' not in rule:
        s += '->\n'
        s += '    Some ({})\n'.format(' '.join(rule[arri+1:]))

      else:
        wheni = rule.index('when')

        conds = split_list_on_elems(rule, ['when', 'and'])
        cond_binds = []
        cond_vals = []
        guard_vals = []
        for cond in conds:
          eqi = cond.index('=')
          cond_binds.append('Some ({})'.format(' '.join(cond[:eqi])))
          cond_vals.append(' '.join(cond[eqi+1:]))
          if cond[eqi+1] not in builtinfun:
            guard_vals.append(' '.join(cond[eqi+1:]))

        guards = ' <> None\n      && '.join(guard_vals)
        if len(guard_vals) > 0:
          s += '\n    when {} <> None -> \n'.format(
            ' <> None\n      && '.join(guard_vals)
          )
        else:
          s += '-> \n'

        s += '    begin match {} with\n'.format(' , '.join(cond_vals))
        s += '      | {} ->\n'.format(' , '.join(cond_binds))
        s += '        Some ({})\n'.format(' '.join(rule[arri+1:wheni]))
        s += '      | _ -> None\n'
        s += '    end\n'
      
    s += '  | _ -> None\n'
    rels.append(s)


typestring = ''
if len(types) > 0:
  typestring += 'type '
typestring += '\nand '.join(types)

relstring = ''
if len(rels) > 0:
  relstring += '\n\nlet rec '
relstring += '\nand '.join(rels)

with open('_{}/{}.ml'.format(fname, fname), 'w') as f:
  f.write('open Builtin\n\n{}{}'.format(typestring, relstring))

lextokstr = '\n'
for i, tok in enumerate(syntoks):
  lextokstr += '| "' + tok + '" { TOK' + str(i) + ' }\n'
with open('_{}/lexer.mll'.format(fname, fname), 'w') as f:
  f.write('''{
open Parser
open Printf
exception Eof
exception LexingError of string
}

let int = ['-']? ['0'-'9']+
let float = ['-']? ['0'-'9']+ ['.'] ['0'-'9']*
let id = ['a'-'z'] ['a'-'z' '0'-'9' '\\'']*
let ws = [' ' '\\t' '\\n']

rule token = parse
| ws          { token lexbuf }
''' + lextokstr + '''
| "true"      { TRUE }
| "false"     { FALSE }
| id as v     { ID(v) }
| int as n    { INT(int_of_string n) }
| float as n  { FLOAT(float_of_string n)}
| eof         { EOF }
| _           { raise (LexingError "error") }
''')

pstrs = [rule[0] + ' : ' + '\n  | '.join(rule[1:]) for rule in prules]
with open('_{}/parser.mly'.format(fname), 'w') as f:
  f.write('''%{
open ''' + fname.capitalize() + '''
open Printf
open Lexing
%}

%token <string> ID
%token <int> INT
%token <float> FLOAT
%token TRUE FALSE
%token ''' + ' '.join(['TOK' + str(i) for i in range(len(syntoks))]) + '''
%token EOF

''' + '\n'.join(['%type <{}.{}> {}'.format(
    fname.capitalize(), t, t) for t in contypes]
  ) + '''
%type <''' + fname.capitalize() + '''.e> file

%start file

%%
''' + '\n'.join(pstrs) + '''

file : e EOF { $1 }
''')
