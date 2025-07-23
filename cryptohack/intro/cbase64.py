import base64

flag_encode = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

bflag = bytes.fromhex(flag_encode)

flag = base64.b64encode(bflag)

print(flag)
