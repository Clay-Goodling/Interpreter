(* General comparison relations *)
let eq (e1 : 'a) (e2 : 'a) : bool option =
  Some (e1 = e2)
let neq (e1 : 'a) (e2 : 'a) : bool option =
  Some (e1 <> e2)
let lt (e1 : 'a) (e2 : 'a) : bool option =
  Some (e1 < e2)
let leq (e1 : 'a) (e2 : 'a) : bool option =
  Some (e1 <= e2)
let gt (e1 : 'a) (e2 : 'a) : bool option =
  Some (e1 > e2)
let geq (e1 : 'a) (e2 : 'a) : bool option =
  Some (e1 >= e2)

(* Boolean relations *)
let notb (b : bool) : bool option =
  Some (not b)
let andb (b1 : bool) (b2 : bool) : bool option =
  Some (b1 && b2)
let orb (b1 : bool) (b2 : bool) : bool option =
  Some (b1 || b2)
let printb (b : bool) : bool option =
  print_endline (if b then "True" else "False");
  Some b

(* Integer relations *)
let addi (n1 : int) (n2 : int) : int option =
  Some (n1 + n2)
let subi (n1 : int) (n2 : int) : int option =
  Some (n1 - n2)
let muli (n1 : int) (n2 : int) : int option =
  Some (n1 * n2)
let divi (n1 : int) (n2 : int) : int option =
  Some (n1 / n2)
let printi (n : int) : int option =
  print_int n;
  print_newline ();
  Some n

(* Float relations *)
let addf (n1 : float) (n2 : float) : float option =
  Some (n1 +. n2)
let subf (n1 : float) (n2 : float) : float option =
  Some (n1 -. n2)
let mulf (n1 : float) (n2 : float) : float option =
  Some (n1 *. n2)
let divf (n1 : float) (n2 : float) : float option =
  Some (n1 /. n2)
let printf (n : float) : float option =
  print_float n;
  print_newline ();
  Some n

(* Map relations *)
let bind (s : ('a * 'b) list) (k : 'a) (v : 'b) : ('a * 'b) list option =
  Some ((k, v) :: s)
let index (k : 'a) (s : ('a * 'b) list) : 'b option =
  List.assoc_opt k s