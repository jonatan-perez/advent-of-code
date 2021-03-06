from collections import namedtuple

packet = namedtuple("packet", ("version", "type_id", "value", "subpackets"))

def convert_to_hex(file):
    if file == "input":
        with open(f"2021/day16-packet-decoder/{file}.txt") as f:
            input = f.readline().rstrip("\n")
    else:
        input = file
        
    hex_to_bin = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111"
    }

    transmission = ""
    for hex in input:
        transmission += hex_to_bin[hex]
    return transmission

def decodeTransmission(transmission, i):
    version = int(transmission[i:i + 3], 2)
    type_id = int(transmission[i + 3:i + 6], 2)
    i += 6
    if type_id == 4:
        value, i = decodeLiteral(transmission, i)
        return packet(version, type_id, value, []), i

    length_type_id = transmission[i]
    i += 1
    if length_type_id == "0":
        subpackets, i = getSubpacketsByLength(transmission, i)
    elif length_type_id == "1":
        subpackets, i = getSubpacketsByNumber(transmission, i)
    value = 0
    return packet(version, type_id, value, subpackets), i

def decodeLiteral(transmission, i):
    next_num = transmission[i:i + 5]
    i += 5
    num_bits = ""
    while next_num[0] == "1":
        num_bits += next_num[1:]
        next_num = transmission[i:i + 5]
        i += 5
    num_bits += next_num[1:]
    binary_literal = int(num_bits, 2)

    return binary_literal, i

def getSubpacketsByLength(transmission, i):
    subpackets = []
    length = int(transmission[i:i + 15], 2)
    i += 15
    length_used = 0
    while length_used < length:
        subpacket, new_i = decodeTransmission(transmission, i)
        subpackets.append(subpacket)
        length_used += new_i - i
        i = new_i
    return subpackets, i


def getSubpacketsByNumber(transmission, i):
    subpackets = []
    num_subpackets = int(transmission[i: i + 11], 2)
    i += 11
    for x in range(num_subpackets):
        subpacket, i = decodeTransmission(transmission, i)
        subpackets.append(subpacket)
    return subpackets, i

def sumVersions(packet):
    total = packet.version
    for subpacket in packet.subpackets:
        total += sumVersions(subpacket)
    return total

def get_answer(file):
    transmission = convert_to_hex(file)
    packet = decodeTransmission(transmission, 0)[0]
    return sumVersions(packet)
    
print(get_answer("input"))