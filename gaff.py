#    Copyright (C) 2019 Greenweaves Software Limited
#
#    This is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This software is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

# gaff.py Global Alignment with Scoring Matrix and Affine Gap Penalty

from align import san_kai

def gaff(s,t):
    score,s1,t1 = san_kai([s0 for s0 in s],[t0 for t0 in t])
    return score,''.join(s1),''.join(t1)

if __name__=='__main__':
    from helpers import create_strings
    #score,s,t = gaff('PRTEINS','PRTWPSEIN')
    strings   = create_strings(fasta=True)
    #print (strings[0])
    #print (strings[1])
    score,s,t = gaff(strings[0],strings[1])
    print (score)
    print (s)
    print (t)        
    with open('gaff.txt','w') as o:
        o.write('{0}\n'.format(score))
        o.write('{0}\n'.format(s))
        o.write('{0}\n'.format(t))