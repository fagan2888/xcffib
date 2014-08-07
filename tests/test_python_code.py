""" Test list packing and unpacking. """

import xcffib
import xcffib.xproto
import struct

class TestPythonCode(object):

    def test_struct_pack_uses_List(self):
        # suppose we have a list of ints...
        ints = struct.pack("=IIII", *range(4))

        # Unpacker wants a cffi.cdata
        cffi_ints = xcffib.bytes_to_cdata(ints)

        l = xcffib.List(xcffib.Unpacker(cffi_ints), "I", count=4)
        ints2 = struct.pack("=IIII", *l)

        # after packing and unpacking, we should still have those ints
        assert ints == ints2

    def test_union_pack(self):
        data = struct.pack("=" + ("b" * 20), *range(20))
        cffi_data = xcffib.bytes_to_cdata(data)

        cm = xcffib.xproto.ClientMessageData(xcffib.Unpacker(cffi_data))

        for actual, expected in zip(range(20), cm.data8):
            assert actual == expected, actual

        assert cm.data32[0] == 0x03020100
        assert cm.data32[1] == 0x07060504
        assert cm.data32[2] == 0x0b0a0908
