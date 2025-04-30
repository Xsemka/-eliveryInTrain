import rsa
(pkey, ckey) = rsa.newkeys(4096)
print(pkey)
print(ckey)