#!/usr/bin/env python3

import sys
import os

# Libleo encryptor. v0.1
# called via: encrypt_libleo.py [rom path] [map path]

# Changelog:
# v0.1: It exists. Please read the ROM in and do 1 write rather than 100s though

print(sys.argv[1], sys.argv[2])

# Open the 2 files
rom_file = open(sys.argv[1], 'r+b')
map_file = open(sys.argv[2], 'r')

# Return a virtual address for a given function.
def get_address_from_map(Lines, name):
    for line in Lines:
        if name in line:
            return line.split()[0]
    return -1 # we didnt find anything. sad day.

def encrypt_leobootgame2(rom_file, vaddr, rom_addr, key):
    func_size = 804 # DO NOT MODIFY THE SIZE OF THE FUNCTION. TODO: Dont hardcode these values.. somehow
    i = 0
    rom_file.seek(int(rom_addr, 16), os.SEEK_SET)
    for i in range(i, func_size, 4):
        ba = bytearray(rom_file.read(4))
        rom_file.seek(-4, os.SEEK_CUR)
        ba[2] = (ba[2] + key) & 0xFF
        ba[3] = (ba[3] - key) & 0xFF
        rom_file.write(ba)
    return 0

def encrypt_leobootgame3(rom_file, vaddr, rom_addr, key):
    func_size = 0x60
    i = 0
    rom_file.seek(int(rom_addr, 16), os.SEEK_SET)
    for i in range(i, func_size, 4):
        ba = bytearray(rom_file.read(4))
        rom_file.seek(-4, os.SEEK_CUR)
        ba[2] = (ba[2] + key) & 0xFF
        ba[3] = (ba[3] - key) & 0xFF
        rom_file.write(ba)
    return 0

Lines = map_file.readlines()

# Find the virtual addresses for each function to encrypt.
game2_addr = hex(int(get_address_from_map(Lines, "__LeoBootGame2"), 16))
game3_addr = hex(int(get_address_from_map(Lines, "__LeoBootGame3"), 16))

game2_rom_addr = hex(int(game2_addr, 16) - 0x7FFFF400)
game3_rom_addr = hex(int(game3_addr, 16) - 0x7FFFF400)

game2_addr_int = int(game2_addr, 16)

# Calculate the encryption key.
key = ((game2_addr_int & 0xFF000000) >> 0x18) + ((game2_addr_int & 0x00FF0000) >> 0x10) + ((game2_addr_int & 0x0000FF00) >> 0x08) + ((game2_addr_int & 0x000000FF)) & 0xFF

encrypt_leobootgame2(rom_file, game2_addr, game2_rom_addr, key)
encrypt_leobootgame3(rom_file, game3_addr, game3_rom_addr, key)
