from math import log2


class Hamming:
    def __init__(self):
        # self._generating_matrix_filename = 'generating_matrix.txt'
        # self.generating_matrix = self._generate_matrix()
        self.generating_matrix = [0] + [0 if log2(i + 1) - int(log2(i + 1)) == 0 else None for i in range(1, 50)]
        self.hamming_message_len = None

    def _fill_generating_matrix(self, message):
        gen_index = 2
        msg_index = 0
        while msg_index < len(message):
            # if gen_index > len(self.generating_matrix[0]): ...
            if self.generating_matrix[gen_index] is None:
                self.generating_matrix[gen_index] = int(message[msg_index])
                msg_index += 1
            gen_index += 1
        self.hamming_message_len = gen_index
        # print(self.hamming_message_len)
        # print(self.generating_matrix)

    def encode(self, message, mistake='0'):
        bin_message = Hamming._str_to_bin(message)
        print(f'bin_message: {bin_message}')
        hamming_message = self._hamming_encode(bin_message)
        print(f'hamming_message: {hamming_message}')
        return Hamming.__make_mistake_in_encoded_message(hamming_message, mistake)

    def _hamming_encode(self, message):
        self._fill_generating_matrix(message)
        # print(self.generating_matrix)

        check = 1
        while check <= self.hamming_message_len:
            lst = []
            for i in range(check - 1, self.hamming_message_len, 2 * check):
                line = map(lambda x: 0 if not x else x, self.generating_matrix[i:i + check])
                lst.extend(line)
            # print(check, lst)
            counter = sum(lst)
            self.generating_matrix[check - 1] = 1 if counter % 2 else 0
            # print(self.generating_matrix)
            check *= 2

        # print(self.generating_matrix)
        return ''.join(map(str, self.generating_matrix[:self.hamming_message_len]))

    @staticmethod
    def _hamming_encode2(message):
        # if all(char in '01' for char in data) and data != "":
        datalist = list(message)
        datalistcopy = list(message)
        result = ""

        log_len = log2(len(datalist))
        count = int(log_len) + 1
        # print(count)

        # расставляем пустые биты
        checkbits = count
        for i in range(checkbits):
            pos = (2 ** i) - 1
            datalist.insert(pos, '*')
            datalistcopy.insert(pos, '*')

        check = 1
        checkbits = []
        while check <= len(datalist):
            # берем в lst нужные биты для текущего бита
            lst = []
            for i in range(check - 1, len(datalist), 2 * check):
                lst.extend(datalist[i:i + check])
            print(check, lst)
            check *= 2

            # считаем единички
            counter = 0
            for u in range(len(lst)):
                if lst[u] == "1":
                    counter += 1
            # ставим наш бит
            if counter % 2 == 0:
                lst[0] = "0"
                checkbits += "0"
            else:
                lst[0] = "1"
                checkbits += "1"
        print(checkbits)

        # составляем строку ответа
        c = 0
        for e in range(0, len(datalist)):
            if datalist[e] == "*":
                result += checkbits[c]
                c += 1
            else:
                result += datalist[e]

        return result

    # else:
    #     return "Error: Input must be binary!"

    @staticmethod
    def _str_to_bin(string):
        return ''.join(format(ord(x), 'b') for x in string)

    @staticmethod
    def _bin_to_str(bin_data):
        str_data = ''

        for i in range(0, len(bin_data), 7):
            temp_data = bin_data[i:i + 7]
            decimal_data = int(temp_data, 2)
            str_data = str_data + chr(decimal_data)

        return str_data

    def decode(self, message):
        msg_without_control_bits = ''
        check_bits = []
        for i in range(2, len(message)):
            if log2(i + 1) - int(log2(i + 1)) != 0:
                msg_without_control_bits = ''.join((msg_without_control_bits, message[i]))
            else:
                check_bits.append(message[i])
        # print(msg_without_control_bits)
        encoded = self._hamming_encode(msg_without_control_bits)

        fixed_message = self._fix_errors(message, encoded)
        bin_result = Hamming._delete_control_bits(fixed_message)
        string_result = Hamming._bin_to_str(''.join(bin_result))
        return string_result

    @staticmethod
    def decode2(message):
        datalist = list(message)
        datalistcopy = list(message)

        # расставляем пустые биты
        count = int(log2(len(message)))
        # count = 6
        print(count)
        for i in range(count):
            pos = (2 ** i) - 1
            # datalist.insert(pos, '*')
            datalistcopy[pos] = '*'
        print(datalistcopy)

        check = 1
        checkbits = []
        while check <= len(datalist):
            # берем в lst нужные биты для текущего бита
            lst = []
            for i in range(check - 1, len(datalistcopy), 2 * check):
                lst.extend(datalistcopy[i:i + check])
            print(check, lst)
            check *= 2

            # считаем единички
            counter = 0
            for u in range(len(lst)):
                if lst[u] == "1":
                    counter += 1
            # ставим наш бит
            if counter % 2 == 0:
                lst[0] = "0"
                checkbits += "0"
            else:
                lst[0] = "1"
                checkbits += "1"

        print(checkbits)
        Hamming._fix_errors(checkbits[:count + 1], datalist, datalistcopy)
        bin_result = Hamming._delete_control_bits(datalist, count)
        string_result = Hamming._bin_to_str(''.join(bin_result))
        return string_result

    def _fix_errors(self, original, encoded):
        error_bits = []
        i = 1
        while i < self.hamming_message_len:
            if original[i - 1] != encoded[i - 1]:
                error_bits.append(i)
            i *= 2

        error_bits_sum_index = sum(error_bits) - 1
        if error_bits:
            new_bit = '1' if original[error_bits_sum_index] == '0' else '0'
        else:
            return original
        # print(error_bits)
        return ''.join((encoded[:error_bits_sum_index], new_bit, encoded[error_bits_sum_index + 1:]))

    @staticmethod
    def _delete_control_bits(datalist):
        res = []

        for i in range(2, len(datalist)):
            if log2(i + 1) - int(log2(i + 1)) != 0:
                res.append(datalist[i])

        return res

    @staticmethod
    def __make_mistake_in_encoded_message(message, mistake='0'):
        if mistake == '0':
            return message
        try:
            dec_mistake = int(mistake)
        except ValueError:
            return message
        dec_message = int(message, 2)
        if dec_mistake > dec_message:
            return message
        res = dec_message ^ dec_mistake
        return bin(res)[2:]


if __name__ == '__main__':
    hm = Hamming()
    # print(hm.generating_matrix)
    # msg = '10101010110'
    # print(len(msg))
    # hm._fill_generating_matrix(msg)
    print(hm.encode('go'))
    hm = Hamming()
    print(hm.decode('0010100011111011111'))
