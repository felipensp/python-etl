import sys
import re
import subprocess

def match_rules(content):   
    blocks = re.findall(r'(?m:^)/[^/]+\/\s*{(?s:(?:[^{}]+|\{.*?\})*)}', content)

    for m in blocks:
        match = re.match(r'(?m:^)/([^/]+)\/\s*{((?s:(?:[^{}]+|\{.*?\})*))}', m)
                
        repl = r'if re.search(r"\1", _input):\n'
        repl += r'    for m1 in re.findall(r"(\1)", _input):\n'
        repl += r'        m0 = re.match(r"\1", m1[0])\n' 
        
        # code block
        repl2 = match.group(2)
        # group reference
        repl2 = re.sub(r'\$(\d+)', r'm0.group(\1)', repl2)    
        # fix ident
        repl += re.sub(r'(?m:^)', '    ', repl2)
            
        content = re.sub(r'(?m:^)/([^/]+)\/\s*{((?s:(?:[^{}}]+|\{.*?\})*))}', repl, content, 1)
    return content    

def get_input():
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as fp:
            return fp.read()
    else:
        return sys.stdin.read()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('regex-etl.py etl-file [input]')
        exit()
        
    with open(sys.argv[1]) as fp:
        file_content = fp.read()
        file_content = match_rules(file_content)
        file_content = 'import re\nimport sys\n\n_input = sys.stdin.read()\n' + file_content
        
        with open('_script.py', 'w') as fw:
            fw.write(file_content)
        
        _input = get_input()
        proc = subprocess.Popen(['python', '_script.py'], stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
        
        output_out = proc.communicate(input=_input.encode())[0]
        print(output_out.decode('utf-8').strip())
        
        output_err = proc.communicate()[1]
        if output_err:
            print('ERROR: ' + output_err.decode('utf-8').strip())