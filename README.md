# Computing the nucleolus of a characteristic function form game.

## Nucleolus
Nucleolus is considered as the most stable solution concept for cooperative transferable-utility games. 
It always exists and is unique. 
Moreover, if the game has a non-empty core, then the nucleolus necessarily belongs to the core. 

## Algorithm
Here we have an implementation of Maschler's scheme of computing the nucleolus.  This involves solving exponentially many exponentially large linear programs. So this works only for really small games. However the implementation is straightforward, and can be used for quick testing.
