 pow _ 0 = 1
 pow a 1 = a
 pow a 2 = a * a
 pow a b = pow a (b `div` 2) * pow a (b - (b `div` 2))
 
 
 main = let i = pow 2 10000000 in print $ (length . show) i
