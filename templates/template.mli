(** [e] is the type of an expression. A full program should have type [e]. *)
type e

(** [c] is the type of a configuration. The primary evaluation of a program is
  * a relation between configurations, so a configuration should store both a
  * program and any necessary state.
*)
type c

(** [init e] is the default configuration of a given expression. This function
  * is used to take a program and turn it into something that can be stepped. It
  * is [None] if [e] is not a valid starting expression.
*)
val init: e -> c option

(** [step c] is the result of taking a single evaluation step on [c]. It is
  * [None] if [c] is stuck.
*)
val step: c -> c option