qsort :: Ord a => [a] -> [a]
 
qsort [] = []
qsort (x:xs) = qsort l ++ [x] ++ qsort g
                 where l = filter (<x) xs
                       g = filter (>=x) xs

main = print $ qsort [1,10,2,9,3,7,2]
