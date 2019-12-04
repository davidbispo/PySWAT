import sys

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

#Spinning cursor widget
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor
    
    spinner = spinning_cursor()
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    
        os.chdir(r'D:\TxtInOut')       
        print("Running Swat..")
        for path in execute(["swat.exe"]):
            print(path)
        
        print('Run Succesful!...Fetching Data...')