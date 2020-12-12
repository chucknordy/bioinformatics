#   Copyright (C) 2020 Greenweaves Software Limited

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

#  MULT Multiple Alignment

import argparse
import os
import time
from   helpers import read_strings
from   numpy   import argmax,ravel

def score(chars,
          match       = 0,
          mismatch    = -1):    
    return sum(match if chars[i]==chars[j] else  mismatch for i in range(len(chars)) for j in range(i+1,len(chars)))

def score_strings(s,t,u,v):
    return sum(score([s[i],t[i],u[i],v[i]]) for i in range(len(s)))
    
def MultipleAlignment(Strings,
                      match       = 0,
                      mismatch    = -1):
 
    s = [[[[0 for l in range(len(Strings[3])+1)]     \
              for k in range(len(Strings[2])+1)]     \
              for j in range(len(Strings[1])+1)]     \
              for i in range(len(Strings[0])+1) ]
    
    moves = [
        [-1, -1, -1, -1],
        
        [-1, -1, -1,  0],
        [-1, -1,  0, -1],
        [-1,  0, -1, -1],
        [ 0, -1, -1, -1],
        
        [-1, -1,  0,  0],
        [-1,  0, -1,  0],
        [ 0, -1, -1,  0],
        [ 0,  0,  0, -1],
        [ 0, -1,  0, -1],
        [ 0,  0, -1, -1],
        
        [-1,  0,  0,  0],
        [0,  -1,  0,  0],
        [0,   0,  -1, 0],
        [0,   0,   0,  -1]
    ]
    
    path = {}
    
    for i in range(1,len(Strings[0])+1):
        for j in range(1,len(Strings[1])+1):
            for k in range(1,len(Strings[2])+1): 
                for l in range(1,len(Strings[3])+1):
 
                    scores = [ 
                        s[i-1][j-1][k-1][l-1] + score([Strings[0][i-1], Strings[1][j-1], Strings[2][k-1], Strings[3][l-1]]),
                        
                        s[i-1][j-1][k-1][l]   + score([Strings[0][i-1], Strings[1][j-1], Strings[2][k-1], '-']),
                        s[i-1][j-1][k][l-1]   + score([Strings[0][i-1], Strings[1][j-1], '-',             Strings[3][l-1]]),
                        s[i-1][j][k-1][l-1]   + score([Strings[0][i-1], '-',             Strings[2][k-1], Strings[3][l-1]]),
                        s[i][j-1][k-1][l-1]   + score(['-',             Strings[1][j-1], Strings[2][k-1], Strings[3][l-1]]),
                        
                        s[i-1][j-1][k][l]   + score([Strings[0][i-1], Strings[1][j-1], '-', '-']),
                        s[i-1][j][k-1][l]   + score([Strings[0][i-1], '-',             Strings[2][k-1], '-']),
                        s[i][j-1][k-1][l]   + score(['-',             Strings[1][j-1], Strings[2][k-1], '-']),
                        s[i-1][j][k][l-1]   + score([Strings[0][i-1], '-',             '-',             Strings[3][l-1]]),
                        s[i][j-1][k][l-1]   + score(['-',             Strings[1][j-1], '-',             Strings[3][l-1]]),                      
                        s[i][j][k-1][l-1]   + score(['-',             '-',             Strings[2][k-1], Strings[3][l-1]]),
                        
                                                
                        s[i-1][j][k][l]       + score([Strings[0][i-1], '-',             '-',             '-']),
                        s[i][j-1][k][l]       + score(['-',             Strings[1][j-1], '-',             '-']),
                        s[i][j][k-1][l]       + score(['-',             '-',             Strings[2][k-1], '-']),
                        s[i][j][k][l-1]       + score(['-',             '-',             '-',             Strings[3][l-1]]),                        
                        
                    ]
                    index           = argmax(scores)
                    s[i][j][k][l]   = scores[index]
                    path[(i,j,k,l)] = moves[index]
            #print (i,j,k,l,path[(i,j,k,l)])        
    i  = len(Strings[0])
    j  = len(Strings[1])
    k  = len(Strings[2])
    l  = len(Strings[3])
    Alignment = [[] for s in Strings]
    while i>0 and j>0 and k>0 and l>0:
        d_indices = path[(i,j,k,l)]
        i += d_indices[0]
        j += d_indices[1]
        k += d_indices[2]
        l += d_indices[3]
        for m in range(len(d_indices)):
            if d_indices[m]==0:
                Alignment[m].append('-')
            else:
                index = [i,j,k,j][m]
                Alignment[m].append(Strings[m][index])
 
    return s[len(Strings[0])][len(Strings[1])][len(Strings[2])][len(Strings[3])], Alignment

if __name__=='__main__':
    start = time.time()
    parser = argparse.ArgumentParser('MULT Multiple Alignment')
    parser.add_argument('--sample',   default=False, action='store_true', help='process sample dataset')
    parser.add_argument('--rosalind', default=False, action='store_true', help='process Rosalind dataset')
    args = parser.parse_args()
    if args.sample:
        print (score_strings('ATAT-CCG',
                             '-T---CCG',
                             'ATGTACTG',
                             'ATGT-CTG'))
        print (MultipleAlignment(['ATATCCG',
                                  'TCCG',
                                  'ATGTACTG',
                                  'ATGTCTG']))
        
    

    if args.rosalind:
        Input  = read_strings(f'data/rosalind_{os.path.basename(__file__).split(".")[0]}.txt')
 
        score, Alignment = MultipleAlignment(Input[1], Input[3], Input[5], Input[7])
        print (Result)
        with open(f'{os.path.basename(__file__).split(".")[0]}.txt','w') as f:
            print (score)
            f.write(f'{score}\n')
            for line in Alignment:
                print (line)
                f.write(f'{line}\n')
                
    elapsed = time.time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')    
