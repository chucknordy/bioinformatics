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

#  RSUB  	Identifying Reversing Substitutions 

import argparse
import os
import time
from helpers import read_strings
from newick  import newick_to_adjacency_list
from   fasta import FastaContent

def rsub(T,Assignments):
    Adj =newick_to_adjacency_list(T)
    fc  = FastaContent(Assignments)
    x=0
    
if __name__=='__main__':
    start = time.time()
    parser = argparse.ArgumentParser('RSUB  	Identifying Reversing Substitutions')
    parser.add_argument('--sample',   default=False, action='store_true', help='process sample dataset')
    parser.add_argument('--rosalind', default=False, action='store_true', help='process Rosalind dataset')
    args = parser.parse_args()
    if args.sample:
        print(rsub('(((ostrich,cat)rat,mouse)dog,elephant)robot;',
                   ['>robot',
                   'AATTG',
                   '>dog',
                   'GGGCA',
                   '>mouse',
                   'AAGAC',
                   '>rat',
                   'GTTGT',
                   '>cat',
                   'GAGGC',
                   '>ostrich',
                   'GTGTC',
                   '>elephant',
                   'AATTC']))
        
     
    if args.rosalind:
        Input  = read_strings(f'data/rosalind_{os.path.basename(__file__).split(".")[0]}.txt')
 
        Result = rsub(Input[0],Input[1:])
        
        print (Result)
        with open(f'{os.path.basename(__file__).split(".")[0]}.txt','w') as f:
            for line in Result:
                f.write(f'{line}\n')
                
    elapsed = time.time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')    
