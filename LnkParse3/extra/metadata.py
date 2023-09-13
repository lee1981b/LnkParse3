from struct import unpack
from LnkParse3.extra.lnk_extra_base import LnkExtraBase
from LnkParse3.decorators import uuid
from enum import IntEnum
"""
------------------------------------------------------------------
|     0-7b     |     8-15b     |     16-23b     |     24-31b     |
------------------------------------------------------------------
|              <u_int32> BlockSize >= 0x0000000C                 |
------------------------------------------------------------------
|            <u_int32> BlockSignature == 0xA0000009              |
------------------------------------------------------------------
|                    <u_int32> StorageSize                       |
------------------------------------------------------------------
|                    Version == 0x53505331                       |
------------------------------------------------------------------
|                      <GUID> FormatID                           |
|                            16 B                                |
------------------------------------------------------------------
|   <vector<MS_OLEPS>> SerializedPropertyValue (see MS-OLEPS)    |
|                             ? B                                |
------------------------------------------------------------------
"""


class PropertyType(IntEnum):
    VT_EMPTY = 0x0000 #Type is undefined, and the minimum property set version is 0.
    VT_NULL = 0x0001 #Type is null, and the minimum property set version is 0.
    VT_I2 = 0x0002 #Type is 16-bit signed integer, and the minimum property set version is 0.
    VT_I4 = 0x0003 #Type is 32-bit signed integer, and the minimum property set version is 0.
    VT_R4 = 0x0004 #Type is 4-byte (single-precision) IEEE floating-point number, and the
                   #minimum property set version is 0.
    VT_R8 = 0x0005 #Type is 8-byte (double-precision) IEEE floating-point number, and the
                   #minimum property set version is 0.
    VT_CY = 0x0006 #Type is CURRENCY, and the minimum property set version is 0.
    VT_DATE = 0x0007 #Type is DATE, and the minimum property set version is 0.
    VT_BSTR = 0x0008 #Type is CodePageString, and the minimum property set version is 0.
    VT_ERROR = 0x000A #Type is HRESULT, and the minimum property set version is 0.
    VT_BOOL = 0x000B #Type is VARIANT_BOOL, and the minimum property set version is 0.
    VT_DECIMAL = 0x000E #Type is DECIMAL, and the minimum property set version is 0.
    VT_I1 = 0x0010 #Type is 1-byte signed integer, and the minimum property set version is 1.
    VT_UI1 = 0x0011 #Type is 1-byte unsigned integer, and the minimum property set version is 0.
    VT_UI2 = 0x0012 #Type is 2-byte unsigned integer, and the minimum property set version is 0.
    VT_UI4 = 0x0013 #Type is 4-byte unsigned integer, and the minimum property set version is 0.
    VT_I8 = 0x0014 #Type is 8-byte signed integer, and the minimum property set version is 0.
    VT_UI8 = 0x0015 #Type is 8-byte unsigned integer, and the minimum property set version is 0.
    VT_INT = 0x0016 #Type is 4-byte signed integer, and the minimum property set version is 1.
    VT_UINT = 0x0017 #Type is 4-byte unsigned integer, and the minimum property set version is 1.
    VT_LPSTR = 0x001E #Type is CodePageString, and the minimum property set version is 0.
    VT_LPWSTR = 0x001F #Type is UnicodeString, and the minimum property set version is 0.
    VT_FILETIME = 0x0040 #Type is FILETIME, and the minimum property set version is 0.
    VT_BLOB = 0x0041 #Type is binary large object (BLOB), and the minimum property set version is 0.
    VT_STREAM = 0x0042 #Type is Stream, and the minimum property set version is 0. VT_STREAM is not
                       #allowed in a simple property set.
    VT_STORAGE = 0x0043 #Type is Storage, and the minimum property set version is 0. VT_STORAGE is not
                        #allowed in a simple property set.
    VT_STREAMED_Object = 0x0044 #Type is Stream representing an Object in an application-specific manner, and the
                                #minimum property set version is 0. VT_STREAMED_Object is not allowed in a simple
                                #property set.
    VT_STORED_Object = 0x0045 #Type is Storage representing an Object in an application-specific manner, and the
                              #minimum property set version is 0. VT_STORED_Object is not allowed in a simple
                              #property set.
    VT_BLOB_Object = 0x0046 #Type is BLOB representing an object in an application-specific manner. The minimum
                            #property set version is 0.
    VT_CF = 0x0047 #Type is PropertyIdentifier, and the minimum property set version is 0.
    VT_CLSID = 0x0048 #Type is CLSID, and the minimum property set version is 0.
    VT_VERSIONED_STREAM = 0x0049 #Type is Stream with application-specific version GUID (VersionedStream). The
                                 #minimum property set version is 0. VT_VERSIONED_STREAM is not allowed in a
                                 #simple property set.

    VT_VECTOR_I2 = 0x1002 #Type is Vector of 16-bit signed integers, and the minimum property set version is 0.
    VT_VECTOR_I4 = 0x1003 #Type is Vector of 32-bit signed integers, and the minimum property set version is 0.
    VT_VECTOR_R4 = 0x1004 #Type is Vector of 4-byte (single-precision) IEEE floating-point numbers, and
                          #the minimum property set version is 0
    VT_VECTOR_R8 = 0x1005 #Type is Vector of 8-byte (double-precision) IEEE floating-point numbers, and
                          #the minimum property set version is 0.
    VT_VECTOR_CY = 0x1006 #Type is Vector of CURRENCY, and the minimum property set version is 0.
    VT_VECTOR_DATE = 0x1007 #Type is Vector of DATE, and the minimum property set version is 0.
    VT_VECTOR_BSTR = 0x1008 #Type is Vector of CodePageString, and the minimum property set version is 0.
    VT_VECTOR_ERROR = 0x100A #Type is Vector of HRESULT, and the minimum property set version is 0.
    VT_VECTOR_BOOL = 0x100B #Type is Vector of VARIANT_BOOL, and the minimum property set version is 0.
    VT_VECTOR_VARIANT = 0x100C #Type is Vector of variable-typed properties, and the minimum property set version is 0.
    VT_VECTOR_I1 = 0x1010 #Type is Vector of 1-byte signed integers and the minimum property set version is 1.
    VT_VECTOR_UI1 = 0x1011 #Type is Vector of 1-byte unsigned integers, and the minimum property set version is 0.
    VT_VECTOR_UI2 = 0x1012 #Type is Vector of 2-byte unsigned integers, and the minimum property set version is 0.
    VT_VECTOR_UI4 = 0x1013 #Type is Vector of 4-byte unsigned integers, and the minimum property set version is 0.
    VT_VECTOR_I8 = 0x1014 #Type is Vector of 8-byte signed integers, and the minimum property set version is 0.
    VT_VECTOR_UI8 = 0x1015 #Type is Vector of 8-byte unsigned integers and the minimum property set version is 0.
    VT_VECTOR_LPSTR = 0x101E #Type is Vector of CodePageString, and the minimum property set version is 0.
    VT_VECTOR_LPWSTR = 0x101F #Type is Vector of UnicodeString, and the minimum property set version is 0.
    VT_VECTOR_FILETIME = 0x1040 #Type is Vector of FILETIME, and the minimum property set version is 0.
    VT_VECTOR_CF = 0x1047 #Type is Vector of PropertyIdentifier, and the minimum property set version is 0.
    VT_VECTOR_CLSID = 0x1048 #Type is Vector of CLSID, and the minimum property set version is 0

    VT_ARRAY_I2 = 0x2002 #Type is Array of 16-bit signed integers, and the minimum property set version is 1.
    VT_ARRAY_I4 = 0x2003 #Type is Array of 32-bit signed integers, and the minimum property set version is 1.
    VT_ARRAY_R4 = 0x2004 #Type is Array of 4-byte (single-precision) IEEE floating-point numbers, and
                         #the minimum property set version is 1.
    VT_ARRAY_R8 = 0x2005 #Type is IEEE floating-point numbers, and the minimum property set version is 1.
    VT_ARRAY_CY = 0x2006 #Type is Array of CURRENCY, and the minimum property set version is 1.
    VT_ARRAY_DATE = 0x2007 #Type is Array of DATE, and the minimum property set version is 1.
    VT_ARRAY_BSTR = 0x2008 #Type is Array of CodePageString, and the minimum property set version is 1.
    VT_ARRAY_ERROR = 0x200A #Type is Array of HRESULT, and the minimum property set version is 1.
    VT_ARRAY_BOOL = 0x200B #Type is Array of VARIANT_BOOL, and the minimum property set version is 1.
    VT_ARRAY_VARIANT = 0x200C #Type is Array of variable-typed properties, and the minimum property set version is 1.
    VT_ARRAY_DECIMAL = 0x200E #Type is Array of DECIMAL, and the minimum property set version is 1.
    VT_ARRAY_I1 = 0x2010 #Type is Array of 1-byte signed integers, and the minimum property set version is 1.
    VT_ARRAY_UI1 = 0x2011 #Type is Array of 1-byte unsigned integers, and the minimum property set version is 1.
    VT_ARRAY_UI2 = 0x2012 #Type is Array of 2-byte unsigned integers, and the minimum property set version is 1.
    VT_ARRAY_UI4 = 0x2013 #Type is Array of 4-byte unsigned integers, and the minimum property set version is 1.
    VT_ARRAY_INT = 0x2016 #Type is Array of 4-byte signed integers, and the minimum property set version is 1.
    VT_ARRAY_UINT = 0x2017 #Type is Array of 4-byte unsigned integers, and the minimum property set version is 1


class Metadata(LnkExtraBase):
    def name(self):
        return "METADATA_PROPERTIES_BLOCK"

    def storage_size(self):
        start, end = 8, 12
        return unpack("<I", self._raw[start:end])[0]

    def version(self):
        start, end = 12, 16
        version = unpack("<I", self._raw[start:end])[0]
        return hex(version)

    @uuid
    def format_id(self):
        start, end = 16, 32
        return self._raw[start:end]

    def as_dict(self):
        tmp = super().as_dict()
        tmp["storage_size"] = self.storage_size()
        tmp["version"] = self.version()
        tmp["format_id"] = self.format_id()
        tmp["property_values"] = self.serialized_property_value()
        return tmp

    def serialized_property_value(self):
        start = 32
        result = []
        if self.format_id().upper() == 'D5CDD5052E9C101B939708002B2CF9AE':
            # Serialized Property Value (String Name)
            while True:
                value = dict()
                value['value_size'] = unpack('<I', self._raw[start: start + 4])[0]
                if hex(value['value_size']) == hex(0x0):
                    break
                value['name_size'] = unpack('<I', self._raw[start + 4: start + 8])[0]
                name_size_end = (start + 9 + int(value['name_size'])) * 2
                binary = self._raw[start + 9: name_size_end]
                value['name'] = self.text_processor.read_unicode_string(binary)

                value_type = unpack('<H', self._raw[name_size_end: name_size_end + 2])[0]
                value_padding = unpack('<H', self._raw[name_size_end + 2: name_size_end + 4])[0]
                if value_padding == 0:
                    match value_type:
                        case PropertyType.VT_I2:
                            value['value'] = unpack('<I', self._raw[name_size_end + 4: name_size_end + 6])[0]
                        case PropertyType.VT_LPWSTR:
                            unicode_string_size = unpack('<I', self._raw[name_size_end + 6: name_size_end + 10])[0] * 2
                            unicode_string = self._raw[name_size_end + 10: name_size_end + 10 + unicode_string_size]
                            value['value'] = self.text_processor.read_unicode_string(unicode_string)
                        case _:
                            pass

                result.append(value)
                start += 4 + 4 + 2 + value['name_size'] + value['value_size']

            return result
        else:
            # Serialized Property Value (Integer Name)
            while True:
                value = dict()
                value['value_size'] = unpack('<I', self._raw[start: start + 4])[0]
                if hex(value['value_size']) == hex(0x0):
                    break
                value['id'] = unpack('<I', self._raw[start + 4: start + 8])[0]

                value_type = unpack('<H', self._raw[start + 9: start + 11])[0]
                value_padding = unpack('<H', self._raw[start + 11: start + 13])[0]

                if value_padding == 0:
                    match value_type:
                        # case PropertyType.VT_I2:
                        #     value['value'] = unpack('<I', self._raw[start + 13: start + 15])[0]
                        case PropertyType.VT_LPWSTR:
                            unicode_string_size = unpack('<I', self._raw[start + 13: start + 17])[0] * 2
                            unicode_string = self._raw[start + 17: start + 17 + unicode_string_size]
                            value['value'] = self.text_processor.read_unicode_string(unicode_string)
                        case _:
                            pass

                result.append(value)
                start += value['value_size']

            return result
