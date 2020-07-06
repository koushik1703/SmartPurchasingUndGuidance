import java.util.Random;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;

public class SearchAlgo {

	public static ArrayList<Point> minPath = new ArrayList<Point>();
	public static float distance = 0;
	public static float minDistance = 1000;
	public static Point initialPoint = new Point(0,0);
	
	public static void main(String[] h) {
		
		int range = 10;
		Random random = new Random();
		int numberOfPoint = random.nextInt() % range;
		
		if(numberOfPoint < 0)
			numberOfPoint = numberOfPoint * -1;
		
		Point p[] = new Point[numberOfPoint];
		
		for(int i = 0; i < numberOfPoint; i++) {
			
			int x = random.nextInt() % range;
			int y = random.nextInt() % range;
			if(x < 0)
				x = x * -1;
			if(y < 0)
				y = y * -1;
			p[i] = new Point(x,y);
			PointList.getInstance().add(p[i]);
		}
		
		
		for(Point point : PointList.getInstance().pointArrayList) {
			System.out.println("("+point.x+","+point.y+")");
		}
		
		permute(PointList.getInstance().pointArrayList, 0);
		
		System.out.println("The path :");
		
		for(Point point : minPath) {
			System.out.println("("+point.x+","+point.y+")");
		}
	}
	
	static void permute(ArrayList<Point> a, int k) {
        if (k == a.size()) {
        	distance = initialPoint.distanceTo(a.get(0));
        	Point beforePoint = a.get(0);
        	System.out.println("");
            for(Point point : a) {
            	System.out.print("("+point.x+","+point.y+") ");
            	distance = distance + beforePoint.distanceTo(point);
            	beforePoint = point;
            }
            if(distance < minDistance) {
            	minPath.removeAll(minPath);
            	for(Point point : a) {
            		minPath.add(point);
            	}
            	minDistance = distance;
            }
        } 
        else {
            for (int i = k; i < a.size(); i++) {
                Collections.swap(a, i, k);
 
                permute(a, k + 1);
 
                Collections.swap(a, i, k);
            }
        }
	}
}
