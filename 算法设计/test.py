
chinese_char = "A你好"  # 一个中文字符
binary_encoding = chinese_char.encode('utf-8')
binary_representation = ' '.join(format(bit, '08b') for bit in binary_encoding)
print(binary_representation)
# import binascii

# # 二进制字符串
# binary_str = "01000001111001001011110110100000111001011010010110111101"

# # 使用 binascii.unhexlify 将二进制字符串转换为字节对象
# byte_data = binascii.unhexlify(format(int(binary_str, 2), 'x'))

# # 将字节对象转换为文本字符串
# text_str = byte_data.decode('utf-8')
# print(text_str)

import heapq
from collections import defaultdict

class HuffmanEncoder:
    def __init__(self):
        self.freq_dict = defaultdict(int)
        self.encoding = {}
        self.decoding = {}

    def build_freq_dict(self, text):
        for char in text:
            self.freq_dict[char] += 1

    def build_huffman_tree(self):
        priority_queue = [(freq, char) for char, freq in self.freq_dict.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            freq1, char1 = heapq.heappop(priority_queue)
            freq2, char2 = heapq.heappop(priority_queue)
            combined_freq = freq1 + freq2
            combined_char = char1 + char2
            heapq.heappush(priority_queue, (combined_freq, combined_char))

        huffman_tree = priority_queue[0][1]
        self.build_huffman_codes(huffman_tree, "")

    def build_huffman_codes(self, node, code):
        if len(node) == 1:
            self.encoding[node] = code
            self.decoding[code] = node
        else:
            self.build_huffman_codes(node[0], code + "0")
            self.build_huffman_codes(node[1], code + "1")

    def encode(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.encoding[char]
        return encoded_text

    def decode(self, encoded_text):
        decoded_text = ""
        current_code = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.decoding:
                decoded_text += self.decoding[current_code]
                current_code = ""
        return decoded_text
