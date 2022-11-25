import numpy as np

class addnlInfo:
    def __init__(self) -> None:
        pass



def charFun(players=None, infoObj = None) -> float:
    # The char fun being implemented is as follows.
    # We associate v_i and w_i for each i randomly
    # v(S) =  sum_i v_i - len(S) * \min_i w_i
    if players is None: 
        players = [i for i in range(n)]
    players = set(players)
    v = infoObj.v
    w = infoObj.w
    ans = sum([v[pp] for pp in players]) - min([w[pp] for pp in players])
    return ans

def charFunBenedek(S, infoObj=None):
    """
    Example shown in Finding and verifying the nucleolus of cooperative games - supplement
    Benedek et al. Math Programming (2021) 190:135-170
    DOI: 10.1007/s10107-020-01527-9
    The nucleolus is(2.75, 3.75, 5.5)
    """
    l = sorted(list(S))
    c = {
        (1,):1,
        (2,):2,
        (3,):5,
        (1,2):6,
        (1,3):7,
        (2,3):8,
        (1,2,3):12
    }
    return c[tuple(l)]


if __name__ == "__main__":
    import itertools
    n=6
    infoObj = addnlInfo()
    infoObj.v = {i: int((i*i-20*i +100)/10)+ np.random.randint(0, 5) for i in range(20)}
    infoObj.w = {i: int(((i%10)*(i%10)-6*(i%10))/2) + np.random.randint(0, 10) for i in range(20)}
    N = [i for i in range(n)]
    for i in range(len(N)):
        for S in itertools.combinations(N, i+1):
            print(S, ":", charFun(S, infoObj))