# Example:

'''
#Ac { background-position: 0px 0px; }
#twoc { background-position: -73px 0px; }
#As { background-position: 0px -98px; }
'''

# It goes A to K
# C S H D
ranks = list('A23456789TJQK')
width = 73
height = 98

for j, suit in enumerate('cshd'):
    for i, rank in enumerate(ranks):
        print('#{}{} {{ background-position: {}px {}px }}'.format(
            suit, rank, i * (-width), j * (-height)
        ))
