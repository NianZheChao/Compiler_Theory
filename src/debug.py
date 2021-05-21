import csv
import lexical_analysis
from collections import defaultdict
import tkinter
from tkinter import filedialog
import module_debug


src = lexical_analysis.get_source_file(
    'D:\\2020\GitHub\Compiler_Theory\src\\testData\\test1.txt')

# print('method: lexical_analysis.get_source_file:')
# print(src)

src = lexical_analysis.remove_note(src)
# print('method: lexical_analysis.remove_note')
# print(src)

seed = lexical_analysis.get_seed_code()
# print('method: lexical_analysis.get_seed_code')
# print(seed)

seed = defaultdict(int)
with open('D:\\2020\\GitHub\\Compiler_Theory\\src\\test.csv', 'r', encoding='UTF-8') as f:
    k = csv.reader(f)
    # print('k = csv.reader(f): ')
    # print(k)
    # print('遍历：')
    for i in k:
        print(i)
        seed[str(i[0])] = i[1]
        print(i[1])
# print('种别码seed: ')
