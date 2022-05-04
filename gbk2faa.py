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
        if not os.path.exists('faa_files'):
            os.mkdir('faa_files')
        for name,path in self.na_ph:
            output_name = f'faa_files/{name}.faa'
            output_line = []
            for seq_record in SeqIO.parse(path,'genbank'):
                gp_count = 1
                for seq_feature in seq_record.features:
                    if seq_feature.type == 'CDS':
                        try:
                            locus_tag = seq_feature.qualifiers['locus_tag'][0]
                        except KeyError:
                            print(f'Error: locus_tag empty in {name}')
                            locus_tag = f'gp{gp_count}'
                        try:
                            product = seq_feature.qualifiers['product'][0]
                        except KeyError:
                            print(f'Error: product empty in {name}')
                            product = 'hypothetical protein'
                        tag_name = f'{locus_tag} {product} [{name}]'
                        try:
                            seq = seq_feature.qualifiers['translation'][0]
                        except:
                            print(f'Error: translation empty in {name}')
                            continue
                        output_line.append(f'>{tag_name}\n{seq}\n')
                    gp_count += 1
            if output_line:
                with open(output_name, 'w') as f:
                    f.writelines(output_line)


if __name__ == "__main__":
    ex_seq()