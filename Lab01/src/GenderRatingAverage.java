import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

// C.1.3
public class GenderRatingAverage {

    public static class MovieMapper
            extends Mapper<Object, Text, IntWritable, Text> {

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String[] parts = value.toString().split(",", 3);
            if (parts.length < 3) {
                return;
            }

            int movieId = Integer.parseInt(parts[0].trim());
            String title = parts[1].trim();

            context.write(new IntWritable(movieId),
                    new Text("MOVIE|" + title));
        }
    }

    public static class RatingMapper
            extends Mapper<Object, Text, IntWritable, Text> {

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String[] parts = value.toString().split(",");
            if (parts.length < 4) {
                return;
            }

            int userId = Integer.parseInt(parts[0].trim());
            int movieId = Integer.parseInt(parts[1].trim());
            double rating = Double.parseDouble(parts[2].trim());

            context.write(new IntWritable(movieId),
                    new Text("RATING|" + userId + "|" + rating));
        }
    }

    public static class GenderJoinReducer
            extends Reducer<IntWritable, Text, Text, Text> {

        // UserID -> "M" or "F"
        private Map<Integer, String> genderMap =
                new HashMap<Integer, String>();

        protected void setup(Context context) throws IOException {
            BufferedReader br = new BufferedReader(new FileReader("users.txt"));
            String line;

            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");

                int userId = Integer.parseInt(parts[0].trim());
                String gender = parts[1].trim();

                genderMap.put(userId, gender);
            }

            br.close();
        }

        public void reduce(IntWritable key, Iterable<Text> values,
                Context context) throws IOException, InterruptedException {

            String title = "Unknown";

            double maleSum = 0.0;
            double femaleSum = 0.0;

            int maleCount = 0;
            int femaleCount = 0;

            for (Text value : values) {
                String record = value.toString();

                if (record.startsWith("MOVIE|")) {
                    title = record.substring("MOVIE|".length());
                } else if (record.startsWith("RATING|")) {
                    String[] parts = record.split("\\|");

                    int userId = Integer.parseInt(parts[1].trim());
                    double rating = Double.parseDouble(parts[2].trim());

                    String gender = genderMap.get(userId);

                    if ("M".equals(gender)) {
                        maleSum += rating;
                        maleCount++;
                    } else if ("F".equals(gender)) {
                        femaleSum += rating;
                        femaleCount++;
                    }
                }
            }

            String maleAvg = maleCount == 0
                    ? "N/A"
                    : String.format(Locale.US, "%.2f",
                            maleSum / maleCount);

            String femaleAvg = femaleCount == 0
                    ? "N/A"
                    : String.format(Locale.US, "%.2f",
                            femaleSum / femaleCount);

            context.write(new Text(title),
                    new Text(maleAvg + ", " + femaleAvg));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Gender rating average");

        job.setJarByClass(GenderRatingAverage.class);

        // args[0] = movies.txt
        // args[1] = ratings_1.txt
        // args[2] = ratings_2.txt
        // args[3] = output directory
        
        MultipleInputs.addInputPath(job, new Path(args[0]),
                TextInputFormat.class, MovieMapper.class);

        MultipleInputs.addInputPath(job, new Path(args[1]),
                TextInputFormat.class, RatingMapper.class);

        MultipleInputs.addInputPath(job, new Path(args[2]),
                TextInputFormat.class, RatingMapper.class);

        job.setReducerClass(GenderJoinReducer.class);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        job.setNumReduceTasks(1);

        job.addCacheFile(new URI(
                "hdfs://localhost:8020/user/cloudera/lab1/ml/users.txt"));

        FileOutputFormat.setOutputPath(job, new Path(args[3]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
