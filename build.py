import os

def zeroSumBuilder():
    root = './'
    excluded = [
					'.git', 
					'docs', 
					"First L'Aquila International PlanetWars Competition", 
					'__pycache__'
			   ]
    for subdir, dirs, files in os.walk(root):
        if len(set(subdir.split('/')) & set(excluded)) > 0:
            continue
        for file in files:
            if file == 'makefile':
                os.system(f"(cd {subdir} && make && make clean)")

if __name__ == '__main__':
    zeroSumBuilder()
