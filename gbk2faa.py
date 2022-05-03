#!/bin/env python3
#-* coding = UTF-8 *-
# @Author = Shixuan Huang
from Bio import SeqIO
import os
import sys
class ex_seq():
    def __init__(self) -> None:
        self.input_gate = self.get_gate()
        self.na_ph = self.get_input()
        self.main()
    
    def get_gate(self):
        try:
            return sys.argv[1]
        except:
            return input('gbk dir here')

    def get_input(self):
        def check_end(file):
            gb_file = ['gbk','gb','gbff']
            for gb in gb_file:
                if file.endswith(gb):
                    return True
                else:
                    return False
        na_ph = []
        for file in os.listdir(self.input_gate):
            end2cut = check_end(file)
            if end2cut != False:
                name = os.path.basename(file).rsplit('.',1)[0]
                path = os.path.join(self.input_gate,file)
                na_ph.append([name,path])
        return na_ph
    
    def main(self):
        if not os.path.exists('output'):
            os.mkdir('output')
        for name,path in self.na_ph:
            output_name = f'output/{name}.faa'
            output_line = []
            for seq_record in SeqIO.parse(path,'genbank'):
                for seq_feature in seq_record.features:
                    if seq_feature.type == 'CDS':
                        assert len(seq_feature.qualifiers['translation']) == 1
                        tag_name = seq_feature.qualifiers['locus_tag'] + 'from' + seq_record.name
                        seq = seq_feature.qualifiers['translation']
                        output_line.append(f'>{tag_name}\n{seq}\n')
            with open(output_name, 'w') as f:
                f.writelines(output_line)

    
if __name__ == "__main__":
    ex_seq()