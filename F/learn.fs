printfn "你为什么不问问神奇海螺呢？"
printfn "你确定你是男孩子么？"
printfn "True: %A,False: %A" true false
let s = @"special\b\r\nstring"
printfn "raw string: %A" s
printfn "I just a slice: %A" s.[0..6]

let reverse (a,b,c) = (c,b,a)

let t = (1,'2',3)
printfn "original: %A, reversed: %A" t (reverse t)

let source = [1 .. 10]

let print a = printfn "%A" a

let isOdd n = n % 2 <> 0

//pipes

print <| List.filter isOdd source
List.filter isOdd source |> print

//composition

let sum a = a + a
let multi a = (*) a a

printfn "sum perfer than multi: %A" <| List.map (sum >> multi) source
printfn "multi perfer than sum: %A"<| List.map (sum << multi) source

//List

let yields1 = [ for i in 0..9 do yield i * i]
let yields2 = [ for i in 0..9 -> i * i]

print yields1
print yields2

print <| List.sum (List.map List.length [yields1;yields2])

// Array

let arr = [| 1..10 |]

print arr

let initArr = Array.init 10 (fun x->x*x)

print initArr

initArr.[0] <- 12306

print initArr

//Recursive

let rec fib = function
  | 0 -> 0
  | 1 -> 1
  | n -> fib(n-1) + fib(n-2)

let rec sumList = function
  | [] -> 0
  | x::xs -> x + sumList xs

print <| sumList [1..100]

//record

[<Struct>]
type User = { id:int; name:string }

let a = { id = 0; name = "a" }

print a

let a2 = { a with id = 1 }

print a2

//adt

type Option<'a> = 
  | Some of 'a
  | None

let some = Some 123
let none = None

let show a =
  match a with
    | Some a -> print a
    | None -> print None

show <| some
show <| none

type Either<'a,'b> =
  | Left of 'a
  | Right of 'b

let left = Left 123
let right = Right 3211

print left
print right

//active pattern

let (|Left|Right|) a = if a >= 0 then Left a else Right a

match -10086 with 
  | Left a -> print a
  | Right a -> print -a

//classes 

type Pointer(x:int,y:int) =
  let position = match (x,y) with
    | (x,y) when x < 0 && y > 0 -> 1
    | (x,y) when x > 0 && y > 0 -> 2
    | (x,y) when x < 0 && y < 0 -> 3
    | (x,y) when x > 0 && y < 0 -> 4
    | _ -> 0
  member this.X = x
  member this.Y = y
  member this.Position = position

let p = Pointer(12,-1)
print p.Position

type State<'T>(init:'T) =
  let mutable store = init
  member this.get = store
  member this.set b = store <- b
  interface System.IDisposable with
    member this.Dispose() = print "Dispose"


//let st = new State<int>(123456)
let st = State(123456)

print st.get

st.set 654321

print st.get

//Parallel

let bigArr = [| 0 .. 1000000 |]

let result = 
  bigArr
  |> Array.Parallel.map multi
  |> print
  
