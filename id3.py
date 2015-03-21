import binascii

'''
###
1) Identify tag as ID3v2.3
    An ID3v2 tag can be detected with the following pattern:
    $49 44 33 yy yy xx zz zz zz zz
    Where yy is less than $FF, xx is the 'flags' byte and zz is less than $80.

2) Use flag in head to identify if there is an extended header
    The version is followed by one the ID3v2 flags field, of which currently only three flags are used.
    a - Unsynchronisation
    Bit 7 in the 'ID3v2 flags' indicates whether or not unsynchronisation is used (see section 5 for details); a set bit indicates usage.
    b - Extended header
    The second bit (bit 6) indicates whether or not the header is followed by an extended header. The extended header is described in section 3.2.
    c - Experimental indicator
    The third bit (bit 5) should be used as an 'experimental indicator'. This flag should always be set when the tag is in an experimental stage.

3) Work on frames
###
'''

file_mp3 = r"C:\Users\Mike\Desktop\Pictures of Success.mp3"
#file_mp3 = r"C:\Users\Mike\Desktop\Get Up.mp3"
file_m4a = r"C:\Users\Mike\Desktop\On Distant Shores.m4a"
file_epub = r"C:\Users\Mike\Desktop\Emma.epub"

def hex_to_num(to_convert):
    return int(binascii.hexlify(to_convert),16)

def calc_tag_size(list_of_size_bytes):
    NUM_OF_RETAINED_BITS = 7 #only want the lowest 7 bits as we have to ignore the MSb

    binary_string = ""

    for byte in reversed(list_of_size_bytes): #Need to reverse the list to be able to concat in a consistent way
        for bit_index in range(NUM_OF_RETAINED_BITS):
            recreated_bit = (ord(byte) >> bit_index) & 1 #ord because the byte was read as a utf-8 char
            binary_string = str(recreated_bit) + binary_string

    return int(binary_string, 2)

count = 0



with open(file_mp3,"rb") as mp3_file:

    # Header
    id3_identifier = mp3_file.read(3)
    print("Identifier: " + id3_identifier.decode("utf-8"))

    id3_major_version = hex_to_num(mp3_file.read(1))
    id3_revision_number = hex_to_num(mp3_file.read(1))
    print("Version: " + str(id3_major_version) + "." + str(id3_revision_number))

    id3_flags = mp3_file.read(1)
    print("Flags: " + str(id3_flags))

    NUM_OF_SIZE_BYTES = 4
    id3_size_bytes_list = [mp3_file.read(1) for byte in range(NUM_OF_SIZE_BYTES)] #want to read one byte at a time
    id3_size = calc_tag_size(id3_size_bytes_list)
    print("Size: " + str(id3_size))

    # Frames

    while count < 25:
        #Space
        print("")
        # Frame ID
        frame_id = mp3_file.read(4).decode("utf-8")
        print("Flag ID: " + frame_id)
        # Length
        length_bytes = mp3_file.read(4)
        length = int(binascii.hexlify(length_bytes),16) - 1
        print("Length bytes: " + str(length_bytes))
        print("Length: " + str(length))
        # Flags
        frame_flags = mp3_file.read(3)
        print("Frame flags: " + str(frame_flags))
        # Frame info
        if(length > 1000):
            mp3_file.seek(length,1)
            print("Skipped: too large")
        else:
            try:
                info = mp3_file.read(length).decode("utf-8")
            except(UnicodeDecodeError):
                info = mp3_file.read(length).decode("utf-16")
            print(info)
        count+= 1



