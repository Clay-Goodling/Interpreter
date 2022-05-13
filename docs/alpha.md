# Arbitrary Language Interpreter

## Vision

My vision is simple: to build a system capable of taking the semantics of azz language and turning it into an interpreter for that language. For example, the system could take the following file and generate an interpreter for the arith language.

    type x ::=
      | String

    type n ::=
      | Int

    type e ::=
      | (e)
      | x
      | n
      | e + e
      | e * e
      | x := e; e

    type s ::=
      | Map x -> n

    type c ::=
      | (s, e)
      
    rel init e -> c
    { init e = ([], e)
    }

    rel step c -> c
    { step (s, ( e ))       = (s, e)
    , step (s, x)           = (s, n)             when n = index x s
    , step (s, e1 + e2)     = (s', e1' + e2)     when (s', e1') = step (s, e1) 
    , step (s, n + e2)      = (s', n + e2')      when (s', e2') = step (s, e2)
    , step (s, n1 + n2)     = (s', n3)           when n3 = addi n1 n2
    , step (s, e1 * e2)     = (s', e1' * e2)     when (s', e1') = step (s, e1)
    , step (s, n * e2)      = (s', n * e2')      when (s', e2') = step (s, e2)
    , step (s, n1 * n2)     = (s', n3)           when n3 = muli n1 n2
    , step (s, x := e1; e2) = (s', x := e1', e2) when (s', e1') = step (s, e1)
    , step (s, x := n; e2)  = (s', e2)           when s' = bind s x n
    }

## Status

At present, I have the first piece of a script which can generate an ocaml module containing the same information as a semantic file. This piece handles only the types and ignores the relations. This is not a lot of concrete code, but the majority of my initial work was in designing the language to describe semantics and figuring out the format of the module which would describe a language.

## Next Steps

My next steps are to finish the script which will generate the module containing language information and to write scripts to generate a lexer and parser for the language. I intend to use ocamllex and ocamlyacc to generate the actual lexer and parser, but I need a way to create the .mll and .mly files that these tools use.
