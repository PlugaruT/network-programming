#Lab #1 - simple client/server application
###Server requirements
- The server must print debug information about each incoming connection, indicating the remote address [and other details you think that are relevant].
- The server must implement 5 special commands that can be received from the client, to which the server will react in a special way:
- `%Hastalavista` - if the server receives this command, it will terminate the connection and shut itself down;
- `%Time` - the server will react by sending the client the current time of the system on which the server is running
- The other 3 commands have to be chosen by you
- If the server receives an unknown command - it must respond with "Can you elaborate on that?"
- If the server receives an unknown command that ends with a '?' - it must respond with "42"

###Bonus features

- The server must be able to handle multiple client connections at the same time.
- The server supports an additional special command - `%Picsoritdidnthappen`. Upon receiving it, the server will send the following image to the client

###Client requirements
- The client must take its input commands from the keyboard
- The command will be sent to the server by pressing the Enter key
- If you implemented the file transfer feature, the client must receive the image and save it to a file in the current directory; i.e. your client does not have to display the image itself.
- The client will terminate the connection with the server if you try to send the `%Close` command
