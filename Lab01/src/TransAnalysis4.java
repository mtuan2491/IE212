import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class TransAnalysis4 {

    // Game_type Number_of_all_distinct_playerIDs Total_amount
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

            List<String> IDs = new ArrayList<String>();
            double total = 0.0;

            for (Text t : values) {
                String[] parts = t.toString().trim().split(" ");

                String id = parts[0];
                total += Float.parseFloat(parts[1]);

                if (!IDs.contains(id)) {
                    IDs.add(id);
                }
            }

            int count = IDs.size();
            context.write(key,
                    new Text(Integer.toString(count) + "   " + Double.toString(total)));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Trans analysis 4");

        job.setJarByClass(TransAnalysis4.class);
        job.setMapperClass(TransMapper.class);
        job.setReducerClass(TransReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
