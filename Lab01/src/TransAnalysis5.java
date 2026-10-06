import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class TransAnalysis5 {

	// read trans file and show the list of: Game_type
	// List_of_Names_of_all_distinct_players Total_amount

	public static class TransMapper extends Mapper<Object, Text, Text, Text> {

		// user map to keep the userId-userName
		private Map<Integer, String> userMap = new HashMap<>();

		public void setup(Context context) throws IOException,
				InterruptedException {
			try (BufferedReader br = new BufferedReader(new FileReader("cust"))) {
				String line;
				while ((line = br.readLine()) != null) {
					String columns[] = line.split(",");
					userMap.put(Integer.parseInt(columns[0]), columns[1]);
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			String record = value.toString().trim();
			String[] parts = record.split(",");

			String gametype = parts[4];
			String id = parts[2];
			String amount = parts[3];
			String name = userMap.get(Integer.parseInt(id));

			context.write(new Text(gametype), new Text(id + "," + name + "," + amount));
		}
	}

	public static class TransReducer extends Reducer<Text, Text, Text, Text> {
		public void reduce(Text key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {

			List<String> IDs = new ArrayList<String>();
			double total = 0.0;

			String IDlist = "";
			String nameList = "";
			for (Text t : values) {
				String[] parts = t.toString().trim().split(",");

				total += Float.parseFloat(parts[2]);
				String id = parts[0];

				if (!IDs.contains(id)) {
					IDs.add(id);
					IDlist += parts[0] + ",";
					nameList += parts[1] + ",";
				}

			}
			if (IDlist.length() > 0) {
				IDlist = IDlist.substring(0, IDlist.length() - 1);
				IDlist = "[" + IDlist + "]";
				nameList = nameList.substring(0, nameList.length() - 1);
				nameList = "[" + nameList + "]";
			}
			context.write(key, new Text(nameList + "   " + Double.toString(total)));
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "Trans analysis 5");
		job.setJarByClass(TransAnalysis5.class);
		job.setMapperClass(TransMapper.class);
		job.setReducerClass(TransReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		// Setting reducer to zero
		// job.setNumReduceTasks(0);

		try {

			job.addCacheFile(new URI("hdfs://localhost:8020/mycache/cust"));
		} catch (Exception e) {
			System.out.println("File Not Added");
			System.exit(1);
		}

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
