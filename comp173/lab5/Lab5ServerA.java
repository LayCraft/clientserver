package comp173.lab5;

import java.io.*;
import java.net.*;

/**
 *
* @author Curtis LayCraft
 */
public class Lab5ServerA {
    public short LEFT_NIBBLE = 15 << 4;
    public short RIGHT_NIBBLE = 15;
    
    /* 	This takes an array of integers and performs an operation on all of them
    *	This also takes a string: "1","2","4" representing +, -, *, respectively.
    * 		java comp173.lab5.Lab5ServerA 12345
    */
    public int mathit(byte[] array, short operator){
        // 1 2 4  is + - * 
        int sum = 0;
        switch(operator){
            case 1:
                sum = 0;
                for(int x : array){
                    sum = x + sum;
                }
                break;
            case 2:
                sum = array[0]*2;
                for (int x : array){
                    sum = sum - x;
                }
                break;
            case 4:
                sum = 1;
                for (int x : array){
                    sum = x * sum;
                }
                break;
            default:
                System.out.println("The operator is invalid");
        }
        return sum;
    }

    byte[] toBytes(int i){
		byte[] result = new byte[4];

		result[0] = (byte) (i >> 24);
		result[1] = (byte) (i >> 16);
		result[2] = (byte) (i >> 8);
		result[3] = (byte) (i /*>> 0*/);

		return result;
    }

    public static void main(String[] args) throws IOException {
        // collect port from command line
        int port = Integer.parseInt(args[0]); 
            Lab5ServerA functions = new Lab5ServerA();

        try ( 
            ServerSocket serverSocket = new ServerSocket(port);
        ) {
        	while (true){
            
            Socket clientSocket = serverSocket.accept();
            BufferedInputStream in = new BufferedInputStream(clientSocket.getInputStream());
            BufferedOutputStream out = new BufferedOutputStream(clientSocket.getOutputStream());        		
            
            // send ready message to client
            out.write("READY".getBytes());
            out.flush();
			
		// collect byte array
		byte[] mathArray = new byte[7];	
		int read = in.read(mathArray);

		for (byte x : mathArray) System.out.print("["+x+"]");
		System.out.println("\n");



		// a place to hold operands
		byte[] operands = new byte[mathArray[1]];

		// split left and right bytes and put into operands array
		boolean left = true;
		short i = 2;
		
		for (short position = 0; position < mathArray[1]; position++){
			
			if (left==true){
				// get left 4 bits
				operands[position] =(byte) ((mathArray[i] & functions.LEFT_NIBBLE) >> 4);
				left=false;
			} else {
				// get right 4 bits
				operands[position] =(byte) ((mathArray[i] & functions.RIGHT_NIBBLE));
				left=true;
				i++;
			}
		}

		for (byte x : operands) System.out.print("["+x+"]");
		System.out.println("\n");

		// perform appropriate math on bytes
		int result =functions.mathit(operands ,(short)mathArray[0]);

		// articulate response
		byte[] response = functions.toBytes(result);
		
		//send response to client
            out.write(response);
            out.flush();
            
            }
        }                
    }
}
