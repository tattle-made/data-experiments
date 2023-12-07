import easyocr

# supports multiple indian languages -> add language in ''
# reader = easyocr.Reader(['ch_sim','en'])
reader = easyocr.Reader(['hi'])

result = reader.readtext('path/to/image')
print(result)