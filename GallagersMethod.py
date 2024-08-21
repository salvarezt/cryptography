from random import randint
from FiniteFieldRepresentation import fieldInt as fint
from FiniteFieldMatrices import fieldIntMatrix as fmatrix

def bitFlippingAlgorithm(A : fmatrix, x : fmatrix) -> fmatrix:
    """
    By flipping bits from the vector x this
    outputs a solution vector for the equation
    Ax = 0.
    """
    
    n, _ = x.dim
    # degree[i] will be the number of instances of
    # the variable x_i in the equations
    # represented by the matrix A.
    degree = [0 for _ in range(n)]

    Abool = A.toBoolMatrix()
    m, _ = A.dim # A is an m x n matrix.

    for i in range(m):
        for j in range(n):
            if Abool[i][j]:
                # If variable x_j appears in equation (i) then:
                degree[j] += 1 # The amount of times x_j appears gets increased.
    
    s = A * x # syndrome (column vector)
    sbool = s.toBoolMatrix()

    iszero = False

    while not iszero: # While the syndrome isn't 0

        # fail[i] is the amount of wrong equations
        # where the variable x_i appears.
        fail = [0 for _ in range(n)]
        
        iszero = True # Assume that the syndrome was 0.
        
        for i in range(m):
            """
            If the syndrome has a non-zero
            value. Then the boolean version
            of that value will be True. Since
    
            0 -> False
            otherwise -> True
            """
            if not sbool[i][0]: # If s[i] is 0, then:
                continue # Check the next coordinate

            # To get here, at least one coordinate
            # of the syndrome was non-zero
            iszero = False
            
            for j in range(n): # For each variable x_j
                if Abool[i][j]: # If the variable appears on equation (i)
                    fail[j] += 1 # Then, equation (i) failed.
                # This is because the i-th value of the syndrome is non-zero.
                # And we want the syndrome to be zero.

        if iszero: # If the syndrome is zero, then we're done.
            break
        
        failureRate = [fail[i] / degree[i] for i in range(n)]
        maxFailureRate = max(failureRate)

        etemp = [0 for _ in range(n)]
        for i in range(n):
            if failureRate[i] == maxFailureRate:
                etemp[i] += randint(1, x.fieldSize - 1)
                break

        etemp = fmatrix([etemp], x.primeBase, x.primePower)
        x = x + etemp.T()

        s = A * x # Recalculate the syndrome (column vector)
        sbool = s.toBoolMatrix()
        
    return x
    
def main():

    # F11 (enviar numeros de tel, cedulas) 0..9 " "
    # F27 (alfabeto usual) 0..25 " "
    # F2, F16, F256 (Imagenes)
    # F2 -> 24-tuplas
    # F16 -> 6-tuplas 16a + b, 0..15
    # F256 -> 3-tuplas
    
    P = [[10, 10],
         [10, 9],
         [10, 8],
         [10, 7],
         [10, 6]]

    prime = 11
    power = 1
    
    P = fmatrix(P, prime, power)

    n, m = P.dim
    I = fmatrix.matrixEye(n, prime, power)
    G = (I | P)

    #print(G)

    I = fmatrix.matrixEye(m, prime, power)
    H = ((- P).T() | I)
    
    #print(H) # La version booleana de la matriz H.
    
    x = [[5, 0, 5, 1, 4]]
    x = fmatrix(x, prime, power)
    xG = x * G
    #print(x) # El mensaje original y el extendido.
    
    e = [[0, 0, 0, 0, 7, 0, 0]]
    e = fmatrix(e, prime, power)

    print(xG, xG + e)
    print(bitFlippingAlgorithm(H, (xG + e).T()).T())
    return 0

if __name__ == '__main__':
    main()
