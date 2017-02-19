#! /usr/bin/env python

"""
Smart Card Reader / Writer
"""

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString
from smartcard.ATR import ATR

card_type = AnyCardType()
card_request = CardRequest(timeout=1, cardType=card_type)
card_service = card_request.waitforcard()

card_service.connection.connect()
atr = ATR(card_service.connection.getATR())
print('------- SMART CARD INFO -------')
print(toHexString(card_service.connection.getATR()))
print('Historical bytes: ', toHexString(atr.getHistoricalBytes()))
print('Checksum: ', "0x%X" % atr.getChecksum())
print('Checksum OK: ', atr.checksumOK)
print('T0 supported: ', atr.isT0Supported())
print('T1 supported: ', atr.isT1Supported())
print('T15 supported: ', atr.isT15Supported())
print('-------------------------------')

GET = [0xFF, 0xCA, 0x00, 0x00, 0x00]
DF_TELECOM = [0xFF, 0xB0, 0x00, 0x04, 0x04]
AUTH_KEY = [0xFF, 0x82, 0x00, 0x00, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

def trace_command(apdu):
    print('sending ', toHexString(apdu))

def trace_response(response, sw1, sw2):
    if response is None:
        response = []
    print(
        'serial no.: ',
        toHexString(res),
        ' status words: ',
        "%x %x" % (sw1, sw2)
    )

print('-------- GET CARD DATA --------')
trace_command(GET)
res, s1, s2 = card_service.connection.transmit(GET)
trace_response(res, s1, s2)
print('-------------------------------')
