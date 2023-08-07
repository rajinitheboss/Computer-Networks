How to run:
    I have written a make file already to run.
    All you have to do is to type
        $ make run file={inputfile you want to give} portnum={value of k you want to give}
    and the code will run automatically and gives you the result
    The code runs asking the user for the server name. 
    The code runs until the user gives 'bye' to the terminal.

For the ease of testing I have given some random IP addresses to some random domain names 


Code Explanation:
    Here I have implemented DNS server in iterative manner
    Every query from client directly goes to local DNS server first and the local DNS server 
    sends the request to Root DNS which replies to local DNS server the TDS server IP address
    the local DNS server then goes to TDS server which gives the IP address of the ADS server address
    the local DNS server then goes to ADS server which gives the actual IP address of the server required

    If in the middle any server replies that the domain does not present then the local DNS sends 'sorry' to client
    which then knows DNS record does not exist