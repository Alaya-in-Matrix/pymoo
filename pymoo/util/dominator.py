import numpy as np


class Dominator:

    @staticmethod
    def get_relation(a, b, cva=None, cvb=None):

        if cva is not None and cvb is not None:
            if cva < cvb:
                return 1
            elif cvb < cva:
                return -1

        val = 0
        for i in range(len(a)):
            if a[i] < b[i]:
                # indifferent because once better and once worse
                if val == -1:
                    return 0
                val = 1
            elif b[i] < a[i]:
                # indifferent because once better and once worse
                if val == 1:
                    return 0
                val = -1
        return val

    @staticmethod
    def calc_domination_matrix_loop(F, G):
        n = F.shape[0]
        CV = np.sum(G * (G > 0).astype(np.float), axis=1)
        M = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                M[i, j] = Dominator.get_relation(F[i, :], F[j, :], CV[i], CV[j])
                M[j, i] = -M[i, j]

        return M

    @staticmethod
    def calc_domination_matrix(F, G):

        if G is None:
            constr = np.zeros((F.shape[0],F.shape[0]))
        else:
            # consider the constraint violation
            CV = np.sum(G * (G > 0).astype(np.float), axis=1)
            constr = (CV[:, None] < CV) * 1 + (CV[:, None] > CV) * -1

        # look at the obj for dom
        smaller = np.any(F[:, np.newaxis] < F, axis=2)
        larger = np.any(F[:, np.newaxis] > F, axis=2)
        dom = np.logical_and(smaller, np.logical_not(larger)) * 1 \
              + np.logical_and(larger, np.logical_not(smaller)) * -1

        # if cv equal then look at dom
        M = constr + (constr == 0) * dom
        return M

