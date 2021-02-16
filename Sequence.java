import java.util.Scanner;
class Sequence
{
    public static void printSequence(int n)
    {
        int x = 8, a = 4;
        String  res = a+" "  ;
        for(int i=1; i<n ; i++)
        {
            if(i != n-1)
            {
             res += a*x+" ";   
            }
            else
            {
                res += a*x;
            }
            a = a*x;
            x = x/2;
        }
        System.out.print(res);
    }
    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);
        int n = Integer.parseInt(sc.nextLine());
        Sequence.printSequence(n);
        sc.close();
    }
}