import numpy as np
from scipy.sparse import coo_matrix, linalg

def MyInv(Amat, Vec, FreeDofs: np.ndarray = None):
    """
    Custom matrix inversion function.
    """
    if FreeDofs is None:
        FreeDofs = np.array(np.ones(Vec.FV().NumPy().shape), dtype=bool)
    numFree = np.sum(FreeDofs)
    A_data = list(Amat.COO())
    
    A_coo = coo_matrix((A_data[2].NumPy(), (np.array(A_data[0]), np.array(A_data[1]))), Amat.shape)
    A_csr = A_coo.tocsr()
    A_new_csr = A_csr[FreeDofs][:, FreeDofs]
    b = Vec.FV().NumPy()[FreeDofs]
    
    # 使用spsolve求解Ax = b
    x = linalg.spsolve(A_new_csr, b)
    res = np.zeros(FreeDofs.shape)
    res[FreeDofs] = x
    return res

def Pos_Transformer(Pos_GF, dim=None):
    """
    Position transformer function.
    """
    if dim is None:
        dim = Pos_GF.dim
    else:
        assert(Pos_GF.dim == dim)
    N = int(len(Pos_GF.vec) / dim)
    coords = Pos_GF.vec.Reshape(N).NumPy().copy()
    return coords.T