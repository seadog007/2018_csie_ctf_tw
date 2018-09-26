import java.util.Arrays;

public class Main {

   public static void main(String[] argv) {
      if(argv.length != 1) {
         System.out.println("Usage: java Main [password]");
      } else {
         byte[] input = argv[0].getBytes();

         for(int i = 0; i < input.length; ++i) {
            input[i] = (byte)(input[i] ^ (i * 42 + 1 ^ 66) & 255);
         }

         byte[] key = new byte[]{(byte)37, (byte)5, (byte)118, (byte)90, (byte)-112, (byte)-13, (byte)-34, (byte)7, (byte)106, (byte)102, (byte)-115, (byte)-20, (byte)-51, (byte)0, (byte)80, (byte)84, (byte)-115, (byte)-3, (byte)-34, (byte)2, (byte)121, (byte)84, (byte)-87, (byte)-8};
         if(Arrays.equals(input, key)) {
            System.out.println("OK");
         } else {
            System.out.println("Nope");
         }
         for(int i = 0; i < key.length; ++i) {
            for(int j = 0; j < 255; ++j) {
                if ((byte)(j ^ (i * 42 + 1 ^ 66) & 255) == key[i]){
                   System.out.println(j);
                }
            }
         }
      }
   }
}
