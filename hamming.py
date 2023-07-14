from math import log2


class Hamming:
    def __init__(self):
        self.control_bits_num = 3

    @staticmethod
    def encode(message, mistake='0'):
        bin_message = Hamming._str_to_bin(message)
        print(f'bin_message: {bin_message}')
        hamming_message = Hamming._hamming_encode(bin_message)
        print(f'hamming_message: {hamming_message}')
        return Hamming.__make_mistake_in_encoded_message(hamming_message, mistake)

    @staticmethod
    def _hamming_encode(message):
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
            # print(check, lst)
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
        # print(checkbits)

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

    @staticmethod
    def decode(message):
        datalist = list(message)
        datalistcopy = list(message)

        # расставляем пустые биты
        # count = int(log2(len(message)))
        count = 6
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

    @staticmethod
    def _fix_errors(checkbits, datalist, datalistcopy):
        error_bits = []
        for i in range(len(checkbits)):
            # print(checkbits[i], datalist[2 ** i - 1])
            if checkbits[i] != datalist[2 ** i - 1]:
                error_bits.append(2 ** i)
        if error_bits:
            error_bits_sum = sum(error_bits) - 1
            if datalist[error_bits_sum] == '0':
                datalist[error_bits_sum] = '1'
            else:
                datalist[error_bits_sum] = '0'
        print(error_bits)

    @staticmethod
    def _delete_control_bits(datalist, count):
        res = []

        for i in range(2, len(datalist)):
            if log2(i + 1) - int(log2(i + 1)) != 0 or i + 1 == 2 ** count:
                res.append(datalist[i])

        return res

    @staticmethod
    def __make_mistake_in_encoded_message(message, mistake='0'):
        if mistake == '0':
            return message
        dec_mistake = int(mistake)
        dec_message = int(message, 2)
        res = dec_message ^ dec_mistake
        return bin(res)[2:]


if __name__ == '__main__':
    Hamming.encode('hello')
    print(Hamming.decode("10111011000110001011101100110110001101111"))
