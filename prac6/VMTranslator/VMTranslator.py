class VMTranslator:

    def vm_push(segment, offset):
        '''Generate Hack Assembly code for a VM push operation'''
        ans = []
        if segment == 'constant':
            ans.extend([
                f'@{offset}',
                'D=A'
            ]) 
        elif segment in ('local', 'argument', 'this', 'that'):
            base = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}[segment]
            ans.extend([
                f'@{offset}',
                'D=A',
                f'@{base}',
                'A=M+D',
                'D=M',
            ])
        elif segment == 'temp':
            ans.extend([
                f'@{int(offset) + 5}',
                'D=M'
            ])
        elif segment == 'pointer':
            ptr = 'THIS' if int(offset) == 0 else 'THAT'
            ans.extend([
                f'@{ptr}',
                'D=M'
            ])
        elif segment == 'static' :
            ans.extend([
                f'@{int(offset) + 16}',
                'D=M'
            ])
        else:
            return ""
        ans.extend([
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ])
        return '\n'.join(ans) + '\n'

    def vm_pop(segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        ans=[]
        ans.extend([
            '@SP',
            'AM=M-1',
            'D=M'
        ])
        if segment in ('local', 'argument', 'this', 'that'):
            base = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}[segment]
            ans.extend([
                f'@{offset}',
                'D=A',
                f'@{base}',
                'D=M+D',
                '@R13',
                'M=D',
                '@SP',
                'A=M',
                'D=M',
                '@R13',
                'A=M',
                'M=D'
            ])
        elif segment == 'temp':
            ans.extend([
                f'@{int(offset) + 5}',
                'M=D'
            ])
        elif segment == 'pointer':
            ptr = 'THAT' if offset == 1 else 'THIS'
            ans.extend([
                f'@{ptr}',
                'M=D'
            ])
        elif segment == 'static':
            ans.extend([
                f'@{int(offset + 16)}',
                'M=D'
            ])
        else:
            return ""
        return '\n'.join(ans) + '\n'

    def vm_add():
        '''Generate Hack Assembly code for a VM add operation'''
        ans=[
            '@SP',
            'AM=M-1',
            'D=M',
            '@SP',
            'AM=M-1',
            'M=D+M',
            '@SP',
            'M=M+1'
        ]
        return '\n'.join(ans) + '\n'

    def vm_sub():
        '''Generate Hack Assembly code for a VM sub operation'''
        ans=[
            '@SP',
            'AM=M-1',
            'D=M',
            '@SP',
            'AM=M-1',
            'M=M-D',
            '@SP',
            'M=M+1'
        ]
        return '\n'.join(ans) + '\n'

    def vm_neg():
        '''Generate Hack Assembly code for a VM neg operation'''
        ans=[
            '@SP',
            'A=M-1',
            'M=-M'
        ]
        return '\n'.join(ans) + '\n'


    def vm_eq():
        '''Generate Hack Assembly code for a VM eq operation'''
        return ''

    def vm_gt():
        '''Generate Hack Assembly code for a VM gt operation'''
        return ''

    def vm_lt():
        '''Generate Hack Assembly code for a VM lt operation'''
        return ''

    def vm_and():
        '''Generate Hack Assembly code for a VM and operation'''
        ans = [
            '@SP',
            'AM=M-1',
            'D=M',
            '@SP',
            'A=M-1',
            'M=D&M'
        ]
        return '\n'.join(ans) + '\n'

    def vm_or():
        '''Generate Hack Assembly code for a VM or operation'''
        ans = [
            '@SP',
            'AM=M-1',
            'D=M',
            '@SP',
            'A=M-1',
            'M=D|M'
        ]
        return '\n'.join(ans) + '\n'

    def vm_not():
        '''Generate Hack Assembly code for a VM not operation'''
        ans = [
            '@SP',
            'A=M-1',
            'M=!M'
        ]
        return '\n'.join(ans) + '\n'

    def vm_label(label):
        '''Generate Hack Assembly code for a VM label operation'''
        ans = f'({label})\n'
        return ans

    def vm_goto(label):
        '''Generate Hack Assembly code for a VM goto operation'''
        ans = [
            f'@{label}',
            '0;JMP'
        ]
        return '\n'.join(ans) + '\n'

    def vm_if(label):
        '''Generate Hack Assembly code for a VM if-goto operation'''
        ans = [
            '@SP',
            'AM=M-1',
            'D=M',
            f'@{label}',
            'D;JNE'        
        ]
        return '\n'.join(ans) + '\n'

    def vm_function(function_name, n_vars):
        '''Generate Hack Assembly code for a VM function operation'''
        ans = [f'({function_name})']
        for _ in range(n_vars):
            ans.extend([
                '@0',
                'D=A',
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1'
            ])
        return '\n'.join(ans) + '\n'

    def vm_call(function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        return_label = f"{function_name}$ret"
        ans=[
            f'@{return_label}',
            'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
            '@LCL',
            'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
            '@ARG',
            'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
            '@THIS',
            'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
            '@THAT',
            'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', 
            '@SP', 'D=M', f'@{n_args + 5}', 'D=D-A',
            '@ARG', 'M=D',
            '@SP', 'D=M',
            '@LCL', 'M=D',
            f'@{function_name}', '0;JMP',
            f'({return_label})'        
        ]
        return '\n'.join(ans) + '\n'

    def vm_return():
        '''Generate Hack Assembly code for a VM return operation'''
        ans = [
            '@LCL', 'D=M', '@R13', 'M=D', 
            '@5', 'A=D-A', 'D=M', '@R14', 'M=D',
            '@SP', 'AM=M-1', 'D=M', '@ARG', 'A=M', 'M=D',
            '@ARG', 'D=M+1', '@SP', 'M=D',
            '@R13', 'A=M-1', 'D=M', '@THAT', 'M=D',
            '@R13', 'D=M', '@2', 'A=D-A', 'D=M', '@THIS', 'M=D',
            '@R13', 'D=M', '@3', 'A=D-A', 'D=M', '@ARG', 'M=D',
            '@R13', 'D=M', '@4', 'A=D-A', 'D=M', '@LCL', 'M=D',
            '@R14', 'A=M', '0;JMP'
        ]
        return '\n'.join(ans) + '\n'

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))

        