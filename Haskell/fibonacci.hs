import System.Environment

fib :: Int -> Integer            
fib = (map fib' [0..] !!)        
  where fib' 0 = 0               
        fib' 1 = 1               
        fib' i = fib(i-2)+fib(i-1)

main :: IO()  
main = do
  args <- getArgs
  putStrLn $ case length args of
    0 -> "need param"
    _ -> show $ fib $ n
      where n = read(args !! 0)
