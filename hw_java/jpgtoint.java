import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.BufferedWriter;
import java.io.FileWriter;
import javax.imageio.ImageIO;
class jpgtoint
{
	public static int[][] convertImageToIntArray(BufferedImage image) {
		int[][] image_array = new int[image.getHeight()][image.getWidth()];
		for(int i = 0; i < image.getHeight(); i++) {  
			for(int j = 0; j < image.getWidth(); j++) {
				image_array[i][j] = image.getRGB(j, i);
			}  
		}
		return image_array;
	}
	
	public static BufferedImage loadImage(String ref) {  
		BufferedImage bimg = null;  
		try {  
			bimg = ImageIO.read(new File(ref));  
		} catch (Exception e) {  
			e.printStackTrace();  
		}  
		return bimg;  
	}

	public static void main(String args[])throws IOException
	{
		BufferedImage bi = loadImage(args[0]);
		int a[][]= convertImageToIntArray(bi);
		BufferedWriter bw = new BufferedWriter(new FileWriter("small.csv"));
		PrintWriter p = new PrintWriter(bw);
		for(int i = 0;i<a.length;i++)
		{
			for(int j=0;j<a[0].length;j++)
			{
				if(j==a[0].length-1)
					p.print(a[i][j]);
				else
					p.print(a[i][j]+",");
			}
			p.println();
		}
		p.close();
	}
}
