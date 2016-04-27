import System.Environment
        
fib :: Int -> Integer    
fib = (map fib' [0..] !!)    
  where fib' 0 = 0    
        fib' 1 = 1    
        fib' i = fib(i-2)+fib(i-1)
        
main :: IO()  
main = do
  args <- getArgs
  print $ case null args of
    True -> 0                                                                           
    _ -> fib n
      where n = read(head args)
