import binascii

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



#purpose = "read"
purpose = "do"

with open(file_mp3,"rb") as f:
    id3_identifier = f.read(3)
    print("Identifier: " + id3_identifier.decode("utf-8"))
    id3_major_version = hex_to_num(f.read(1))
    id3_revision_number = hex_to_num(f.read(1))
    print("Version: " + str(id3_major_version) + "." + str(id3_revision_number))
    id3_flags = f.read(1)
    print("Flags: " + str(id3_flags))
    NUM_OF_SIZE_BYTES = 4
    id3_size_bytes_list = [f.read(1) for byte in range(NUM_OF_SIZE_BYTES)] #want to read one byte at a time
    id3_size = calc_tag_size(id3_size_bytes_list)
    print("Size: " + str(id3_size))

    if(purpose=="read"):
        byte = f.seek(5000,1)
        byte = f.read(1)
        while count < 2000:
            print(byte)
            byte = f.read(1)
            count+=1
    if(purpose=="do"):
        while count < 25:
            #Space
            print("")
            # Frame ID
            try:
                frame_id = f.read(4).decode("utf-8")
                print("ID: " + frame_id)
            except(UnicodeDecodeError):
                print("Yo I don't know what this is")
                print(f.read(4))
            # Length
            length_bytes = f.read(4)
            length = int(binascii.hexlify(length_bytes),16) - 1
            print("Length bytes: " + str(length_bytes))
            print("Length: " + str(length))
            # Flags
            frame_flags = f.read(3)
            print("Frame flags: " + str(frame_flags))
            # Frame info
            if(length > 1000):
                f.seek(length,1)
                print("Skipped: too large")
            else:
                info = f.read(length).decode("utf-8")
                print(info)
            count+= 1



