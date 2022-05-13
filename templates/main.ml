let rec multistep step = function
  | None -> None 
  | Some e -> multistep step (step e)

let () =
  let _ =
    if Array.length Sys.argv <> 2 then
      (Printf.printf "Usage: fname <file>\n";
       exit 0) in
  let filename = Sys.argv.(1) in
  let lexbuf = Lexing.from_channel (open_in filename) in
  let e =
    try Parser.file Lexer.token lexbuf
    with Parsing.Parse_error ->
      print_endline "Syntax error.";
      exit 1 in
  ignore (multistep Fname.step (Fname.init e))