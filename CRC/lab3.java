/*
 * This is created by Krishna Sai Kottakota
 * Roll No. CS20B044
 * Date : 15/03/2023
 */

import java.io.File;
import java.util.Scanner;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.Set;
import java.util.HashSet;

public class lab3{
    public static String G = "100000111";
    public static FileWriter outfile;
    public static void main(String[] args){
        try{
            String inputfile = args[0];
            String outputfile = args[1];
            File infile = new File(inputfile);
            outfile = new FileWriter(outputfile);
            Scanner scanner = new Scanner(infile);
            while(scanner.hasNextLine()){
                String D1 = scanner.nextLine();
                String D = D1;
                for(int i=0;i<G.length()-1;i++){
                    D = D + '0';
                }
                String T = Divison(D);
                checkrobustness(D1,D,T);
                outfile.write("\n\n");
            }
            scanner.close();
            outfile.close();
        }
        catch(IOException e){
            System.out.println("Error vachindi ra pooka crt ga code rayy");
            e.printStackTrace();
        }
    }
    public static String Divison(String D){
        String temp = D;
        String Q = "";
        while(temp.length() >= G.length()){
            if(temp.charAt(0) == '0'){
                Q = Q + "0";
                String buff = "";
                int q;
                for(q=1;q<temp.length();q++){
                    buff = buff + temp.charAt(q);
                }
                temp = buff;
            }
            else{
                Q = Q + "1";
                String buff = "";
                for(int q=1;q<G.length();q++){
                    if(temp.charAt(q) == '1' && G.charAt(q) == '1'){
                        buff = buff + "0";
                    }
                    else if(temp.charAt(q) == '1' && G.charAt(q) == '0'){
                        buff = buff + "1";
                    }
                    else if(temp.charAt(q) == '0' && G.charAt(q) == '0'){
                        buff = buff +"0";
                    }
                    else{
                        buff = buff + "1";
                    }
                }
                for(int q=G.length();q<temp.length();q++){
                    buff = buff + temp.charAt(q);
                }
                temp = buff;
            }
        }
        int len = D.length() - temp.length();
        String T = "";
        for(int q=0;q<len;q++){
            T = T + D.charAt(q);
        }
        for(int q=len;q<D.length();q++){
            if(D.charAt(q) == '1' && temp.charAt(q-len) == '1'){
                T = T + "0";
            }
            else if(D.charAt(q) == '0' && temp.charAt(q-len) == '0'){
                T = T + "0";
            }
            else if(D.charAt(q) == '1' && temp.charAt(q-len) == '0'){
                T = T + "1";
            }
            else{
                T = T + "1";
            }
        }
        return T;
    }
    public static void checkrobustness(String D1,String D,String T){
        try{
            Random random = new Random();
            int len = T.length();
            outfile.write("Original String: "+ D1 + "\n");
            outfile.write("Original String with CRC: " + T + "\n");
            for(int i=0;i<10;i++){
                int randomNumber = random.ints(1, 60)
                .findFirst().getAsInt();
                int wrongbits = 2*randomNumber + 1;
                Set<Integer> s = new HashSet<>();
                while(s.size()!=wrongbits){
                    int temp = random.ints(0,len).findFirst()
                                        .getAsInt();
                    s.add(temp);
                }
                char[] chars = T.toCharArray();
                for(Integer j:s){
                    if(T.charAt(j) == '1'){
                        chars[j] = '0';
                    }
                    else if(T.charAt(j) == '0'){
                        chars[j] = '1';
                    }
                }
                String corrupted = new String(chars);
                outfile.write("Corrupted String: "+ corrupted+"\n");
                outfile.write("Number of Errors Introduced: "+wrongbits+"\n");
                if(errordetected(corrupted)){
                    outfile.write("CRC Check: "+ "Error Detected\n");
                }
                else{
                    outfile.write("CRC Check: "+"Error Not Detected\n");
                }
            }
            int ind = random.ints(0,2).
            findFirst().getAsInt(); 
            if(ind == 1){
                for(int j=100;j<110;j+=2){
                    char[] chararray = T.toCharArray();
                    for(int k=0;k<6;k++){
                        if(chararray[j+k] == '1'){
                            chararray[j+k] = '0';
                        }
                        else{
                            chararray[j+k] = '1';
                        }
                    }
                    String corrupted = new String(chararray);
                    outfile.write("Corrupted String: "+ corrupted+"\n");
                    outfile.write("Number of Errors Introduced: "+6+"\n");
                    if(errordetected(corrupted)){
                        outfile.write("CRC Check: "+ "Error Detected\n");
                    }
                    else{
                        outfile.write("CRC Check: "+"Error Not Detected\n");
                    }
                }
            }
            else{
                for(int j=101;j<110;j+=2){
                    char[] chararray = T.toCharArray();
                    for(int k=0;k<6;k++){
                        if(chararray[j+k] == '1'){
                            chararray[j+k] = '0';
                        }
                        else{
                            chararray[j+k] = '1';
                        }
                    }
                    String corrupted = new String(chararray);
                    outfile.write("Corrupted String: "+ corrupted+"\n");
                    outfile.write("Number of Errors Introduced: "+6+"\n");
                    if(errordetected(corrupted)){
                        outfile.write("CRC Check: "+ "Error Detected\n");
                    }
                    else{
                        outfile.write("CRC Check: "+"Error Not Detected\n");
                    }
                }
            }
        }
        catch(IOException e){
            System.out.println("In the function robustness you have IO expection");
            System.out.println("which means that file pointer doesnot exist");
            e.printStackTrace();
        }
    }
    public static Boolean errordetected(String T){
        String temp = T;
        String Q = "";
        while(temp.length() >= G.length()){
            if(temp.charAt(0) == '0'){
                Q = Q + "0";
                String buff = "";
                int q;
                for(q=1;q<temp.length();q++){
                    buff = buff + temp.charAt(q);
                }
                temp = buff;
            }
            else{
                Q = Q + "1";
                String buff = "";
                for(int q=1;q<G.length();q++){
                    if(temp.charAt(q) == '1' && G.charAt(q) == '1'){
                        buff = buff + "0";
                    }
                    else if(temp.charAt(q) == '1' && G.charAt(q) == '0'){
                        buff = buff + "1";
                    }
                    else if(temp.charAt(q) == '0' && G.charAt(q) == '0'){
                        buff = buff +"0";
                    }
                    else{
                        buff = buff + "1";
                    }
                }
                for(int q=G.length();q<temp.length();q++){
                    buff = buff + temp.charAt(q);
                }
                temp = buff;
            }
        }
        Boolean ans = false;
        for(int i=0;i<temp.length();i++){
            if(temp.charAt(i) =='1'){
                ans = true;
                break;
            }
        }
        return ans;
    }
}