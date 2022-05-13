# Arbitrary Language Interpreter

## Vision

My vision is simple: to build a system capable of taking the semantics of an arbitrary language and turning it into an interpreter for that language. For example, the system could take the following file and generate an interpreter for the call-by-name lambda calculus.

    # The type of expressions. Required.
    type e ::=
      | Var String
      | Abs lambda String . e
      | App e e

    # The type of a configuration. Not particularly useful in this case, but
    # required for consistancy in stepping.
    type c ::=
      | Config e

    # The type of a substitution in progress. For use in beta reduction.
    type s ::=
      | Sub e{String / e}

    # A relation to initialize an expression into a configuration ready to be
    # stepped. Again not usefull in this case, but required for consistency.
    rel init e -> c
    { e -> Config e
    }

    # A relation from a substitution to the expression that results from that
    # substitution being caried out.
    rel sub s -> e
    { Sub (Var x', x, e2)       -> e2             when true = eq x x'
    ; Sub (Abs (x', e'), x, e2) -> Abs (x', e')   when true = eq x x'
    ; Sub (Abs (x', e'), x, e2) -> Abs (x', e'')  when false = eq x x' and e'' = sub (Sub (e', x, e2))
    ; Sub (App (e1, e2), x, e3) -> App (e1', e2') when e1' = sub (Sub (e1, x, e3)) and e2' = sub (Sub (e2, x, e3))
    }

    # The basic relation between configurations which represents a program being
    # executed. Required.
    rel step c -> c
    { Config (App (e1, e2))          -> Config (App (e1', e2)) when Config e1' = step (Config e1)
    ; Config (App (Abs (x, e1), e2)) -> Config e1'             when e1' = sub (Sub (e1, x, e2))
    }

## Status

At present, I have a script which can generate an ocaml module containing the same information as a semantic file. When run on the above semantics for the call-by-name lambda calculus, it creates the following ocaml code:

    type e = 
      | Var of string
      | Abs of string * e
      | App of e * e

    and c = 
      | Config of e

    and s = 
      | Sub of e * string * e


    let rec init : e -> c option = function
      | e ->
        Some (Config e)
      | _ -> None

    and sub : s -> e option = function
      | Sub ( Var x' , x , e2 ) 
        when eq x x' <> None -> 
        begin match eq x x' with
          | Some (true) ->
            Some (e2)
          | _ -> None
        end
      | Sub ( Abs ( x' , e' ), x , e2 ) 
        when eq x x' <> None -> 
        begin match eq x x' with
          | Some (true) ->
            Some (Abs ( x' , e' ))
          | _ -> None
        end
      | Sub ( Abs ( x' , e' ), x , e2 ) 
        when eq x x' <> None
          && sub ( Sub ( e' , x , e2 )) <> None -> 
        begin match eq x x' , sub ( Sub ( e' , x , e2 )) with
          | Some (false) , Some (e'') ->
            Some (Abs ( x' , e'' ))
          | _ -> None
        end
      | Sub ( App ( e1 , e2 ), x , e3 ) 
        when sub ( Sub ( e1 , x , e3 )) <> None
          && sub ( Sub ( e2 , x , e3 )) <> None -> 
        begin match sub ( Sub ( e1 , x , e3 )) , sub ( Sub ( e2 , x , e3 )) with
          | Some (e1') , Some (e2') ->
            Some (App ( e1' , e2' ))
          | _ -> None
        end
      | _ -> None

    and step : c -> c option = function
      | Config ( App ( e1 , e2 )) 
        when step ( Config e1 ) <> None -> 
        begin match step ( Config e1 ) with
          | Some (Config e1') ->
            Some (Config ( App ( e1' , e2 )))
          | _ -> None
        end
      | Config ( App ( Abs ( x , e1 ), e2 )) 
        when sub ( Sub ( e1 , x , e2 )) <> None -> 
        begin match sub ( Sub ( e1 , x , e2 )) with
          | Some (e1') ->
            Some (Config e1')
          | _ -> None
        end
      | _ -> None


## Next Steps

My next steps are to write scripts to generate a lexer and parser for the language, and tie everything together into a usable system. I intend to use ocamllex and ocamlyacc to generate the actual lexer and parser, but I need the system to be able to create the .mll and .mly files that these tools use.
