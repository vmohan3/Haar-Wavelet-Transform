import java.io.FileInputStream;
import java.io.BufferedInputStream;
import java.io.IOException;
import java.util.Scanner;
import java.math.BigDecimal;

class Tester
{
	public static void main(String args[])throws IOException
	{	
		Scanner _scanner;
		HaarFilter haar = new HaarFilter(2048);
		haar.setFractionalBits(0);
		_scanner = new Scanner(new BufferedInputStream(new FileInputStream("/root/datasets/smalldataset.csv")));
		byte data[] = new byte[2048*2048];
		int ll = 2048;
		for(int i=0;i<ll;i++) 
		{
			String line = _scanner.nextLine();
			if (line.trim().length() == 0)
				   continue;

			String[] split_line = line.split(" ");
			for(int j=0;j<2048;j++)
			{
				data[i*2048+j]=(byte)new BigDecimal(split_line[j]).intValue();//Byte.parseByte(split_line[j]);
			}
		}
		

		int[] filter = haar.filter(data, null);

		for(int i=0;i<8;i++)
                {
                        for(int j=0;j<8;j++)
                        {
                                System.out.print(filter[i*2048+j]+"\t");
                        }
                        System.out.println();
                }
		System.out.println();
	}
}
