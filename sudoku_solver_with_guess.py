from math import sqrt
from copy import deepcopy

def board_converter(row,m):
   board=[[0 for i in range(m)] for j in range(m)]
   k=0
   for i in range(m):
      for j in range(m):
         if row[k]=='0' or row[k]==0:
            board[i][j]='-'
         else:
            board[i][j]=int(row[k])
         # print(k)
         k+=1
   return board

def col_converter(board,m):
   col=[0 for i in range(m)]
   for i in range(m):
      sub_col=[0 for i in range(m)]
      for j in range(m):
         sub_col[j]=board[j][i]   
      col[i]=sub_col
   return col

def box_converter(board,m,n):
   box=[0 for i in range(m)]
   for k in range(m):
      a=int(int(k/n)*n)
      b=int((k%n)*n)
      sub_box=[]
      for i in range(a,n+a):  
         for j in range(b,n+b):
            sub_box.append(board[i][j])
      box[k]=sub_box
   return box

def blank(elements,m):
   blank_ele=[0 for i in range(m)]
   for k in range(m):
      a=[]
      for l in range(1,m+1):
         if l in elements[k]:
            continue
         a.append(l)
      blank_ele[k]=a    
   return blank_ele

def possible(board,row1,row2,row3,m):
   n=int(sqrt(m))  
   p=[]
   for i in range(m):
      sub=[]
      for j in range(m):
         sub2=[]
         if board[i][j]=='-':
            for k in range(1,m+1):
               if k in row1[i] and k in row2[j] and k in row3[int(j/n)+n*int(i/n)]:
                  sub2.append(k)
         sub.append(sub2)
      p.append(sub)
   return p

def reset(board,m,n):
      col=col_converter(board,m)
##   print(col)
      box=box_converter(board,m,n)
##   print(box) 
  
##     blank row elements
      b_row_e=blank(board,m)
##      print(b_row_e)
##     blank col elements
      b_col_e=blank(col,m)
##      print(b_col_e)
##     blank box elements
      b_box_e=blank(box,m)
##      print(b_box_e)
##   Possible elements in individiual small box
      poss_ele=possible(board,b_row_e,b_col_e,b_box_e,m)
      return col,box,b_row_e,b_col_e,b_box_e,poss_ele


## Solution starts from here         
def board_solver(board,m):
   n=int(sqrt(m))
   sol_board=deepcopy(board)
   solve=False
   while not solve:
      row=deepcopy(sol_board)
      col,box,b_row_e,b_col_e,b_box_e,poss_ele=reset(sol_board,m,n) 
##
      for i in range(m):
         for j in range(m):
            if len(poss_ele[i][j])==1:
               sol_board[i][j]=poss_ele[i][j][0]        
##                    reset everything
               col,box,b_row_e,b_col_e,b_box_e,poss_ele=reset(sol_board,m,n)


      
      for i in range(m):  
         for j in range(m):
            for e in poss_ele[i][j]:
               if sol_board[i][j]=='-':
               
##             for row-wise checking
                  p=0 
                  for k in range(m):
                     if sol_board[i][k]=='-':
                        if e in b_col_e[k] and e in b_box_e[int(k/n)+n*int(i/n)]:                     
                           p+=1
                  if p==1:
                     sol_board[i][j]=e
                     col,box,b_row_e,b_col_e,b_box_e,poss_ele=reset(sol_board,m,n)
                    
      

      
##             for column-wise checking  
                  p=0
                  for k in range(m): 
                     if sol_board[k][j]=='-':
                        if e in b_row_e[k] and e in b_box_e[int(j/n)+n*int(k/n)]:
                           p+=1
                  if p==1:
                     sol_board[i][j]=e
                     col,box,b_row_e,b_col_e,b_box_e,poss_ele=reset(sol_board,m,n)


##                for box-wise checking
                  p=0
                  for k in range(m):
                     if sol_board[n*int(i/n)+int(k/n)][n*int(j/n)+int(k%n)]=='-':
                        if e in b_row_e[n*int(i/n)+int(k/n)] and e in b_col_e[n*int(j/n)+int(k%n)]:
                           p+=1
                  if p==1:
                     sol_board[i][j]=e
                     col,box,b_row_e,b_col_e,b_box_e,poss_ele=reset(sol_board,m,n)
                  
##   for checking each iteration

##      display(row,m)
##      input("Enter for next iteration.")

      solve=(row==sol_board)
   return sol_board

def check(board):
   solve=True
   for i in board:
      for j in i:
         if j=='-':
            solve=False
            return solve
   return solve
def guess_check(board,m,n):
   col,box,b_row_e,b_col_e,b_box_e,poss_ele=reset(board,m,n)     
   for i in range(m):
      for j in range(m):
         if board[i][j]=='-':
            if poss_ele[i][j]==[]:
               
                  
               return True
   
#guessing method
def guess(board):
   m=int(len(board))
   n=int(sqrt(m))
   if check(board):
      print("Solution by guessing method:")
      display(board,m)
      a=input("Do you wanna check for other solutions(y/n)?: ")      
      if a.upper()=='Y':
         return
      a=input("Do you wanna solve other sudoku(y/n)?: ")
      if a.upper()=='Y':
         main()
      else:
         print("It was nice to play with you.")
   for i in range(m):
      for j in range(m):
         if board[i][j]=='-':
            col,box,b_row_e,b_col_e,b_box_e,poss_ele=reset(board,m,n)
            for e in poss_ele[i][j]:
               board[i][j]=e
               if guess_check(board,m,n):
                  continue
               else:
                  guess(board)
            board[i][j]='-'
            return
   



def display(board,m):
   n=int(sqrt(m))
   
   for i in range(m):
      if i%n==0:
         print( '\t\t','-'*(2*n*(n+1)+1))
      print('\t\t',end=' ')
      for j in range(m):
         if j%n==0:
             print('|',end=' ')
         print(board[i][j],end=' ')
      print('|')
   print('\t\t','-'*(2*n*(n+1)+1))
         


         
def main():

##   row=['3','4','2','0','0','2','0','0','0',
##        '0','0','2','0','1','4','3']

##   row=['0','0','0','0','9','0','0','0','1',
##       '0','1','7','6','0','4','3','9','5',
##       '0','9','0','0','0','1','7','0','4',
##       '1','0','8','0','4','5','0','0','3',
##       '0','0','0','2','0','9','0','0','0',
##       '9','0','0','1','6','0','4','0','2',
##       '2','0','3','9','0','0','0','4','0',
##       '7','4','9','8','0','3','2','5','0',
##       '5','0','0','0','7','0','0','0','0'
##       ]
##   row=['0','0','0','0','0','0','0','2','0',
##       '0','0','0','0','0','1','7','0','5',
##       '2','0','0','0','9','7','0','0','3',
##       '3','9','0','0','0','0','0','0','0',
##       '0','0','6','0','0','0','0','0','0',
##       '0','0','0','0','0','0','2','7','4',
##       '0','0','0','9','0','0','0','3','0',
##       '0','5','0','4','0','0','0','0','0',
##       '0','0','1','5','3','0','0','6','0'
##       ]
   
##   row=['0','0','0','0','0','0','0','2','0',
##       '0','0','0','0','0','1','7','0','5',
##       '2','0','0','0','9','7','0','0','3',
##       '3','9','0','0','0','0','0','0','0',
##       '0','0','6','0','0','0','0','0','0',
##       '0','0','0','0','0','0','2','7','4',
##       '0','0','0','9','0','0','0','3','0',
##       '0','5','0','4','0','0','0','0','0',
##       '0','0','1','5','3','0','0','6','0'
##       ]

##Multiple solution
##   row='035190800002000000608040000200008315000000000571400008000930401000000700009081650'

   row=input("Enter entry row-wise and box-wise : ")
   m=int(sqrt(len(row)))
   board=board_converter(row,m)
   print("Your matrix is :")
   display(board,m)
   solved=board_solver(board,m)
   solve=check(solved)
   if not solve:
      print("The solution I got without guessing:")
      display(solved,m)
      guess(solved)
      print("There is no other solution.")
      a=input("Do you wanna solve other sudoku(y/n)?: ")
      if a.upper()=='Y':
         main()
      else:
         print("It was nice to play with you.")
   else:
      print('Your solution is here : ')
      display(solved,m)
      
      
main()
