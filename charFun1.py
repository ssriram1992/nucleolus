import numpy as np

class addnlInfo:
    def __init__(self) -> None:
        pass

n=20
infoObj = addnlInfo()
infoObj.v = {i: int((i*i-20*i +100)/10)+ np.random.randint(0, 5) for i in range(20)}
infoObj.w = {i: int(((i%10)*(i%10)-6*(i%10))/2) + np.random.randint(0, 10) for i in range(20)}
print(infoObj.v, infoObj.w, sep='\n\n\n')

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

if __name__ == "__main__":
    import itertools
    N = [i for i in range(6)]
    for i in range(len(N)):
        for S in itertools.combinations(N, i+1):
            print(S, ":", charFun(S, infoObj))