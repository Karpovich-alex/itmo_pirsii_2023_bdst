class LZW:
    def __init__(self):
        self.enc_dict_len = 256
        self.dec_dict_len = 256
        self.enc_dict = {chr(i): i for i in range(0, 123)}
        self.dec_dict = {i: chr(i) for i in range(0, 123)}

    def encode(self, data):
        prev = ''
        result = []

        for el in data:
            substr = prev + el
            if substr in self.enc_dict:
                prev = substr
            else:
                result.append(self.enc_dict[prev])
                self.enc_dict[substr] = self.enc_dict_len
                self.enc_dict_len += 1
                prev = el
        if prev != '':
            result.append(self.enc_dict[prev])

        return result

    def decode(self, data):
        result = []

        prev = data.pop(0)
        result.append(self.dec_dict[prev])

        for el in data:
            curr = self.dec_dict[el] if el in self.dec_dict else self.dec_dict[prev] + self.dec_dict[prev][0]
            result.append(curr)
            self.dec_dict[self.dec_dict_len] = self.dec_dict[prev] + curr[0]
            self.dec_dict_len += 1
            prev = el

        return ''.join(result)