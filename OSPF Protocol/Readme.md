how to run :
    running of code is normal with inline arguments given after the main.py.
    for example
        python main.py {args}

the code that I have written will not end untill you give ctrl-C as we cannot exit the thread 
that is receiving the packets as the thread waits for a packet almost all the time 

you can use the termination when it shows that the outpointer is closed. 
the changes made to the outputfile doesnot reflect until the outpointer is closed that's why 
we have to wait untill the outpointer is closed. 

I am closing the thread that writes into the outfile after 30 seconds 
