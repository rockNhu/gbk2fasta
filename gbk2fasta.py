#!/bin/env/python3
#coding = UTF-8
from Bio import SeqIO
import os

class ex_seq():
    def __init__(self) -> None:
        self.input_gate = input('gbk dir here')
        self.na_ph = self.get_input()
        self.main()
    
    def get_input(self):
        def check_end(file):
            if file.endswith('gbk'):
                return -4
            elif file.endswith('gb'):
                return -3
            elif file.endswith('gbff'):
                return -5
            else:
                return False
        na_ph = []
        for file in os.listdir(self.input_gate):
            end2cut = check_end(file)
            if end2cut != False:
                name = os.path.basename(file)[:end2cut]
                path = os.path.join(self.input_gate,file)
                na_ph.append([name,path])
        return na_ph
    
    def main(self):
        if not os.path.exists('output'):
            os.mkdir('output')
        for name,path in self.na_ph:
            SeqIO.convert(path,'genbank','output/{}.fasta'.format(name),'fasta')
    
if __name__ == "__main__":
    ex_seq()