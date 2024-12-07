from enum import Enum
import pygame
from games import Game
import reader

#pygame.init()


# 10:9 aspect
SCREEN_SCALE = 6
SCREEN_WIDTH = 160 * SCREEN_SCALE
SCREEN_HEIGHT = 144 * SCREEN_SCALE

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# clock = pygame.time.Clock()


class Colors(Enum):
    White = '\033[48;2;255;255;255m  \033[0m'   # 1,1
    Gray1 = '\033[48;2;169;169;169m  \033[0m'   # 0,1
    Gray2 = '\033[48;2;84;84;84m  \033[0m'      # 1,0
    Black = '\033[48;2;0;0;0m  \033[0m'         # 0,0

def print_tile(location):
    
    game_bytes = reader.get_bytes(Game.PokemonRed, location, location+16)
    
    for line_bytes_i in range(0, len(game_bytes), 2):
        for bit_i in range(8):
            m_bit = (game_bytes[line_bytes_i] >> (7-bit_i)) & 1
            l_bit = (game_bytes[line_bytes_i+1] >> (7-bit_i)) & 1
        
            if m_bit == 0 and l_bit == 0:
                print(Colors.White.value, end='')
            elif m_bit == 0 and l_bit == 1:
                print(Colors.Gray2.value, end='')
            elif m_bit == 1 and l_bit == 0:
                print(Colors.Gray1.value, end='')
            else:
                print(Colors.Black.value, end='')
    
        print()



#start = 0x55ac
#end = start + 256


S_TILE = 0x568c

print(reader.get_game_name(Game.PokemonRed))


for i in range(2):
    print_tile(S_TILE + (i * 16))
    
'''
#w 
print_pixel(S_TILE + (31 * 16))
#i
print_pixel(S_TILE + (32 * 16))
'''



# Color palette test
'''
print(Colors.White.value)
print(Colors.Gray1.value)
print(Colors.Gray2.value)
print(Colors.Black.value)
'''


            
            
print()
        

#00000110
#00000110

"""
for y in range(SCREEN_HEIGHT - 1):
    for x in range(SCREEN_WIDTH - 1):
        screen.set_at((x, y), pygame.Color((255, 0, 0)))

pygame.display.flip()
"""


# pygame.quit()
