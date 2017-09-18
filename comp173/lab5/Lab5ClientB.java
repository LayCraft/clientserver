package comp173.lab5;

import java.io.*;
import java.net.*;

/**
 * java Lab5ClientB.java [portnum] [operator] [int] [int2] [int...]
 * @author Curtis LayCraft
 */
public class Lab5ClientB {

    public byte signEncoder(String x){
        if ("+".equals(x)){
                //0000 0001
                return 1;
        } else if ("-".equals(x)){
                //0000 0010
                return 2;
        } else if ("*".equals(x)){
                //0000 0100		
                return 4;
        }
        return 0;
    }

    /* convert byte array into a single value*/
    public int toInt(byte[] i){
        //for (byte b: i) printByteAsBits(b);
        int total = i[0] << 24 | (i[1] & 0xFF) << 16 | (i[2] & 0xFF) << 8 | (i[3] & 0xFF);
        return total;
    }
    
    public void printByteAsBits(byte b){
        String bits = String.format("%8s", Integer.toBinaryString(b & 0xFF)).replace(' ', '0');
        System.out.println(bits);
    }
    public void printByteArray(byte[] array){
    	for (byte b : array) {
            System.out.print("["+b+"]");
    	}
    	System.out.println();
    }


    /* 	Command line should look like:
    * 	comp173.lab5.Lab5ClientB localhost 12345 + 1 2 3 4 5 
    *	args: [sock] [port] [operator] [operand1] [operand2] [operand3] ...
    * 	The protocol defined only allows for 10 operands
    *	All operands must be less than 15
    *	Server may return a value > 16777215. Not required to handle.
    */
    public static void main(String[] args) throws IOException{

        // make a new client (for functions)
        Lab5ClientB client = new Lab5ClientB();


        // set the port number
        int port = Integer.parseInt(args[1]);
        //int port = 12345;

        //set the sock
        String sock = args[0];
        //String sock = "localhost";

        try (
            Socket clientSocket = new Socket(sock, port);
            BufferedInputStream in = new BufferedInputStream(clientSocket.getInputStream());
            BufferedOutputStream out = new BufferedOutputStream(clientSocket.getOutputStream());
            BufferedReader reader =  new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            DataInputStream dataIn = new DataInputStream(in);
            ){
            // collect ready (5 chars)
            char[] readyState = new char[5];
            int n = reader.read(readyState);
            String s = new String(readyState);

    	    // If ready didn't come, kill the program 
            if (! s.equals("READY")){
                System.out.println("The server isn't ready.");
                return;
            }
			
            //encode byte array
            // array: [operator] [size] [operand1|operand2] [operand3|operand4]...
            // create an empty byte array
            byte[] buffer = new byte[7];
            // add sign
            buffer[0] = client.signEncoder(args[2]);
            // add the count of the operands
            int count = args.length -3;
            buffer[1] = (byte)count;
            System.out.println("There are " + count);


            boolean left = true;
            short position = 2;
            for (short i = 0; i < buffer[1]; i++){
                if (left==true){
                    buffer[position] = (byte) (Byte.valueOf(args[i+3])<<4);
                    // the next one isn't left
                    left = false;
                } else {
                    buffer[position] = (byte) (Byte.valueOf(args[i+3]) | buffer[position]);
                    //the next one is left
                    left = true;
                }
                if (left==true) position++;				
            }
            
            // Send the byte array to the server
            out.write(buffer);
            out.flush();


            int data = dataIn.readInt();
            System.out.println(data);
            
            // server returns 4 bit response
            //byte[] response = new byte[4];
            //int read = in.read(response);

            // show the server's reply
            //System.out.print("Server sent back: ");
            //client.printByteArray(response);

            // convert the response and print it.
            //count = client.toInt(response);
            //System.out.println(count);
			
        } catch (IOException e){
            //Do nothing because the error isn't really serious
        }
    }
}
