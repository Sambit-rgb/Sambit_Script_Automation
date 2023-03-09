import os
x = [os.path.join(r, file) for r,d,f in os.walk('C://Users//neel//PycharmProjects//WinAflAutomation') for file in f ]

for fname in x:    # change directory as needed

     if os.path.isfile(fname):    # make sure it's a file, not a directory entry

      if fname.endswith(".log"):
            with open(fname) as f:   # open file
               for line in f:       # process line by line
                   if 'In pre_fuzz_handler' and 'In post_fuzz_handler' in line:
                     print('found string in file %s' % fname)
                     break
