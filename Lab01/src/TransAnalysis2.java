import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class TransAnalysis2 {

	// read trans file and show the list of: Game_type List_of_all_playerIDs
	// Total_amount

	public static class TransMapper extends Mapper<Object, Text, Text, Text> {
		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			String record = value.toString().trim();
			String[] parts = record.split(",");

			String gametype = parts[4];
			String id = parts[2];
			String amount = parts[3];

			context.write(new Text(gametype), new Text(id + " " + amount));
		}
	}

	public static class TransReducer extends Reducer<Text, Text, Text, Text> {
		public void reduce(Text key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {

			double total = 0.0;

			String IDlist = "";
			for (Text t : values) {
				String[] parts = t.toString().trim().split(" ");

				total += Float.parseFloat(parts[1]);
				IDlist += parts[0] + ",";
			}
			if (IDlist.length() > 0) {
				IDlist = IDlist.substring(0, IDlist.length() - 1);
				IDlist = "[" + IDlist + "]";
			}
			context.write(key, new Text(IDlist + "   " + Double.toString(total)));
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "Trans analysis 2");
		job.setJarByClass(TransAnalysis2.class);
		job.setMapperClass(TransMapper.class);
		job.setReducerClass(TransReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
