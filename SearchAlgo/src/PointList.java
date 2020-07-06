import java.util.ArrayList;

public class PointList {

	static PointList pointList = null;
	static ArrayList<Point> pointArrayList = null;
	
	public PointList() {
		pointArrayList = new ArrayList<Point>();
	}
	
	public static PointList getInstance() {
		if(pointList == null) {
			pointList = new PointList();
		}
		return pointList;
	}
	
	public void add(Point point) {
		pointArrayList.add(point);
	}
}
