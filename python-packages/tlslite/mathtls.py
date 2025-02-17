# Authors:
#   Trevor Perrin
#   Dave Baggett (Arcode Corporation) - MD5 support for MAC_SSL
#   Yngve Pettersen (ported by Paul Sokolovsky) - TLS 1.2
#   Hubert Kario - SHA384 PRF
#
# See the LICENSE file for legal information regarding use of this file.

"""Miscellaneous helper functions."""

from .utils.compat import *
from .utils.cryptomath import *
from .constants import CipherSuite
from .utils import tlshashlib as hashlib

import hmac

#1024, 1536, 2048, 3072, 4096, 6144, and 8192 bit groups]
goodGroupParameters = [(2,0xEEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3),\
                       (2,0x9DEF3CAFB939277AB1F12A8617A47BBBDBA51DF499AC4C80BEEEA9614B19CC4D5F4F5F556E27CBDE51C6A94BE4607A291558903BA0D0F84380B655BB9A22E8DCDF028A7CEC67F0D08134B1C8B97989149B609E0BE3BAB63D47548381DBC5B1FC764E3F4B53DD9DA1158BFD3E2B9C8CF56EDF019539349627DB2FD53D24B7C48665772E437D6C7F8CE442734AF7CCB7AE837C264AE3A9BEB87F8A2FE9B8B5292E5A021FFF5E91479E8CE7A28C2442C6F315180F93499A234DCF76E3FED135F9BB),\
                       (2,0xAC6BDB41324A9A9BF166DE5E1389582FAF72B6651987EE07FC3192943DB56050A37329CBB4A099ED8193E0757767A13DD52312AB4B03310DCD7F48A9DA04FD50E8083969EDB767B0CF6095179A163AB3661A05FBD5FAAAE82918A9962F0B93B855F97993EC975EEAA80D740ADBF4FF747359D041D5C33EA71D281E446B14773BCA97B43A23FB801676BD207A436C6481F1D2B9078717461A5B9D32E688F87748544523B524B0D57D5EA77A2775D2ECFA032CFBDBF52FB3786160279004E57AE6AF874E7303CE53299CCC041C7BC308D82A5698F3A8D0C38271AE35F8E9DBFBB694B5C803D89F7AE435DE236D525F54759B65E372FCD68EF20FA7111F9E4AFF73),\
                       (2,0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF),\
                       (5,0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C934063199FFFFFFFFFFFFFFFF),\
                       (5,0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C93402849236C3FAB4D27C7026C1D4DCB2602646DEC9751E763DBA37BDF8FF9406AD9E530EE5DB382F413001AEB06A53ED9027D831179727B0865A8918DA3EDBEBCF9B14ED44CE6CBACED4BB1BDB7F1447E6CC254B332051512BD7AF426FB8F401378CD2BF5983CA01C64B92ECF032EA15D1721D03F482D7CE6E74FEF6D55E702F46980C82B5A84031900B1C9E59E7C97FBEC7E8F323A97A7E36CC88BE0F1D45B7FF585AC54BD407B22B4154AACC8F6D7EBF48E1D814CC5ED20F8037E0A79715EEF29BE32806A1D58BB7C5DA76F550AA3D8A1FBFF0EB19CCB1A313D55CDA56C9EC2EF29632387FE8D76E3C0468043E8F663F4860EE12BF2D5B0B7474D6E694F91E6DCC4024FFFFFFFFFFFFFFFF),\
                       (5,0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C93402849236C3FAB4D27C7026C1D4DCB2602646DEC9751E763DBA37BDF8FF9406AD9E530EE5DB382F413001AEB06A53ED9027D831179727B0865A8918DA3EDBEBCF9B14ED44CE6CBACED4BB1BDB7F1447E6CC254B332051512BD7AF426FB8F401378CD2BF5983CA01C64B92ECF032EA15D1721D03F482D7CE6E74FEF6D55E702F46980C82B5A84031900B1C9E59E7C97FBEC7E8F323A97A7E36CC88BE0F1D45B7FF585AC54BD407B22B4154AACC8F6D7EBF48E1D814CC5ED20F8037E0A79715EEF29BE32806A1D58BB7C5DA76F550AA3D8A1FBFF0EB19CCB1A313D55CDA56C9EC2EF29632387FE8D76E3C0468043E8F663F4860EE12BF2D5B0B7474D6E694F91E6DBE115974A3926F12FEE5E438777CB6A932DF8CD8BEC4D073B931BA3BC832B68D9DD300741FA7BF8AFC47ED2576F6936BA424663AAB639C5AE4F5683423B4742BF1C978238F16CBE39D652DE3FDB8BEFC848AD922222E04A4037C0713EB57A81A23F0C73473FC646CEA306B4BCBC8862F8385DDFA9D4B7FA2C087E879683303ED5BDD3A062B3CF5B3A278A66D2A13F83F44F82DDF310EE074AB6A364597E899A0255DC164F31CC50846851DF9AB48195DED7EA1B1D510BD7EE74D73FAF36BC31ECFA268359046F4EB879F924009438B481C6CD7889A002ED5EE382BC9190DA6FC026E479558E4475677E9AA9E3050E2765694DFC81F56E880B96E7160C980DD98EDD3DFFFFFFFFFFFFFFFFF)]

def P_hash(macFunc, secret, seed, length):
    bytes = bytearray(length)
    A = seed
    index = 0
    while 1:
        A = macFunc(secret, A)
        output = macFunc(secret, A + seed)
        for c in output:
            if index >= length:
                return bytes
            bytes[index] = c
            index += 1
    return bytes

def PRF(secret, label, seed, length):
    #Split the secret into left and right halves
    # which may share a byte if len is odd
    S1 = secret[ : int(math.ceil(len(secret)/2.0))]
    S2 = secret[ int(math.floor(len(secret)/2.0)) : ]

    #Run the left half through P_MD5 and the right half through P_SHA1
    p_md5 = P_hash(HMAC_MD5, S1, label + seed, length)
    p_sha1 = P_hash(HMAC_SHA1, S2, label + seed, length)

    #XOR the output values and return the result
    for x in range(length):
        p_md5[x] ^= p_sha1[x]
    return p_md5

def PRF_1_2(secret, label, seed, length):
    """Pseudo Random Function for TLS1.2 ciphers that use SHA256"""
    return P_hash(HMAC_SHA256, secret, label + seed, length)

def PRF_1_2_SHA384(secret, label, seed, length):
    """Pseudo Random Function for TLS1.2 ciphers that use SHA384"""
    return P_hash(HMAC_SHA384, secret, label + seed, length)

def PRF_SSL(secret, seed, length):
    bytes = bytearray(length)
    index = 0
    for x in range(26):
        A = bytearray([ord('A')+x] * (x+1)) # 'A', 'BB', 'CCC', etc..
        input = secret + SHA1(A + secret + seed)
        output = MD5(input)
        for c in output:
            if index >= length:
                return bytes
            bytes[index] = c
            index += 1
    return bytes

def calcExtendedMasterSecret(version, cipherSuite, premasterSecret,
                             handshakeHashes):
    """Derive Extended Master Secret from premaster and handshake msgs"""
    assert version in ((3, 1), (3, 2), (3, 3))
    if version in ((3, 1), (3, 2)):
        masterSecret = PRF(premasterSecret, b"extended master secret",
                           handshakeHashes.digest('md5') +
                           handshakeHashes.digest('sha1'),
                           48)
    else:
        if cipherSuite in CipherSuite.sha384PrfSuites:
            masterSecret = PRF_1_2_SHA384(premasterSecret,
                                          b"extended master secret",
                                          handshakeHashes.digest('sha384'),
                                          48)
        else:
            masterSecret = PRF_1_2(premasterSecret,
                                   b"extended master secret",
                                   handshakeHashes.digest('sha256'),
                                   48)
    return masterSecret


def calcMasterSecret(version, cipherSuite, premasterSecret, clientRandom,
                     serverRandom):
    """Derive Master Secret from premaster secret and random values"""
    if version == (3,0):
        masterSecret = PRF_SSL(premasterSecret,
                            clientRandom + serverRandom, 48)
    elif version in ((3,1), (3,2)):
        masterSecret = PRF(premasterSecret, b"master secret",
                            clientRandom + serverRandom, 48)
    elif version == (3,3):
        if cipherSuite in CipherSuite.sha384PrfSuites:
            masterSecret = PRF_1_2_SHA384(premasterSecret,
                                          b"master secret",
                                          clientRandom + serverRandom,
                                          48)
        else:
            masterSecret = PRF_1_2(premasterSecret,
                                   b"master secret",
                                   clientRandom + serverRandom,
                                   48)
    else:
        raise AssertionError()
    return masterSecret

def calcFinished(version, masterSecret, cipherSuite, handshakeHashes,
                 isClient):
    """Calculate the Handshake protocol Finished value

    @param version: TLS protocol version tuple
    @param masterSecret: negotiated master secret of the connection
    @param cipherSuite: negotiated cipher suite of the connection,
    @param handshakeHashes: running hash of the handshake messages
    @param isClient: whether the calculation should be performed for message
    sent by client (True) or by server (False) side of connection
    """
    assert version in ((3, 0), (3, 1), (3, 2), (3, 3))
    if version == (3,0):
        if isClient:
            senderStr = b"\x43\x4C\x4E\x54"
        else:
            senderStr = b"\x53\x52\x56\x52"

        verifyData = handshakeHashes.digestSSL(masterSecret, senderStr)
    else:
        if isClient:
            label = b"client finished"
        else:
            label = b"server finished"

        if version in ((3,1), (3,2)):
            handshakeHash = handshakeHashes.digest()
            verifyData = PRF(masterSecret, label, handshakeHash, 12)
        else: # version == (3,3):
            if cipherSuite in CipherSuite.sha384PrfSuites:
                handshakeHash = handshakeHashes.digest('sha384')
                verifyData = PRF_1_2_SHA384(masterSecret, label,
                                            handshakeHash, 12)
            else:
                handshakeHash = handshakeHashes.digest('sha256')
                verifyData = PRF_1_2(masterSecret, label, handshakeHash, 12)

    return verifyData

def makeX(salt, username, password):
    if len(username)>=256:
        raise ValueError("username too long")
    if len(salt)>=256:
        raise ValueError("salt too long")
    innerHashResult = SHA1(username + bytearray(b":") + password)
    outerHashResult = SHA1(salt + innerHashResult)
    return bytesToNumber(outerHashResult)

#This function is used by VerifierDB.makeVerifier
def makeVerifier(username, password, bits):
    bitsIndex = {1024:0, 1536:1, 2048:2, 3072:3, 4096:4, 6144:5, 8192:6}[bits]
    g,N = goodGroupParameters[bitsIndex]
    salt = getRandomBytes(16)
    x = makeX(salt, username, password)
    verifier = powMod(g, x, N)
    return N, g, salt, verifier

def PAD(n, x):
    nLength = len(numberToByteArray(n))
    b = numberToByteArray(x)
    if len(b) < nLength:
        b = (b"\0" * (nLength-len(b))) + b
    return b

def makeU(N, A, B):
  return bytesToNumber(SHA1(PAD(N, A) + PAD(N, B)))

def makeK(N, g):
  return bytesToNumber(SHA1(numberToByteArray(N) + PAD(N, g)))

def createHMAC(k, digestmod=hashlib.sha1):
    h = hmac.HMAC(k, digestmod=digestmod)
    h.block_size = digestmod().block_size
    return h

def createMAC_SSL(k, digestmod=None):
    mac = MAC_SSL()
    mac.create(k, digestmod=digestmod)
    return mac


class MAC_SSL(object):
    def create(self, k, digestmod=None):
        self.digestmod = digestmod or hashlib.sha1
        self.block_size = self.digestmod().block_size
        # Repeat pad bytes 48 times for MD5; 40 times for other hash functions.
        self.digest_size = 16 if (self.digestmod is hashlib.md5) else 20
        repeat = 40 if self.digest_size == 20 else 48
        opad = b"\x5C" * repeat
        ipad = b"\x36" * repeat

        self.ohash = self.digestmod(k + opad)
        self.ihash = self.digestmod(k + ipad)

    def update(self, m):
        self.ihash.update(m)

    def copy(self):
        new = MAC_SSL()
        new.ihash = self.ihash.copy()
        new.ohash = self.ohash.copy()
        new.digestmod = self.digestmod
        new.digest_size = self.digest_size
        new.block_size = self.block_size
        return new

    def digest(self):
        ohash2 = self.ohash.copy()
        ohash2.update(self.ihash.digest())
        return bytearray(ohash2.digest())
