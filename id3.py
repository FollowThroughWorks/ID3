import binascii

file_mp3 = r"C:\Users\Mike\Desktop\Pictures of Success.mp3"
#file_mp3 = r"C:\Users\Mike\Desktop\Get Up.mp3"
file_m4a = r"C:\Users\Mike\Desktop\On Distant Shores.m4a"
file_epub = r"C:\Users\Mike\Desktop\Emma.epub"

def hex_to_num(to_convert):
    return int(binascii.hexlify(to_convert),16)

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
    id3_size = hex_to_num(f.read(4))
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



