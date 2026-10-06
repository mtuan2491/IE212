import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

// C.1.1
public class MovieRatingAverage {

    public static class RatingMapper
            extends Mapper<Object, Text, IntWritable, DoubleWritable> {

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String[] parts = value.toString().split(",");
            if (parts.length < 4) {
                return;
            }

            int movieId = Integer.parseInt(parts[1].trim());
            double rating = Double.parseDouble(parts[2].trim());

            context.write(new IntWritable(movieId), new DoubleWritable(rating));
        }
    }

    public static class RatingReducer
            extends Reducer<IntWritable, DoubleWritable, Text, Text> {

        private static final int MIN_RATINGS = 2;

        // MovieID -> Title
        private Map<Integer, String> movieMap = new HashMap<Integer, String>();

        private String maxMovie = null;
        private double maxRating = -1.0;

        protected void setup(Context context) throws IOException {
            BufferedReader br = new BufferedReader(new FileReader("movies.txt"));
            String line;

            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",", 3);

                int movieId = Integer.parseInt(parts[0].trim());
                String title = parts[1].trim();

                movieMap.put(movieId, title);
            }

            br.close();
        }

        public void reduce(IntWritable key, Iterable<DoubleWritable> values,
                Context context) throws IOException, InterruptedException {

            double sum = 0.0;
            int count = 0;

            for (DoubleWritable value : values) {
                sum += value.get();
                count++;
            }

            double average = sum / count;
            String title = movieMap.get(key.get());

            if (title == null) {
                title = "Unknown Movie " + key.get();
            }

            context.write(new Text(title),
                    new Text(String.format(Locale.US, "%.2f (%d)", average, count)));

            if (count >= MIN_RATINGS && average > maxRating) {
                maxRating = average;
                maxMovie = title;
            }
        }

        protected void cleanup(Context context)
                throws IOException, InterruptedException {

            if (maxMovie != null) {
                String message = maxMovie
                        + " is the highest rated movie with an average rating of "
                        + String.format(Locale.US, "%.2f", maxRating)
                        + " among movies with at least "
                        + MIN_RATINGS + " ratings.";

                context.write(new Text("Highest Rated Movie"), new Text(message));
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Movie rating average");

        job.setJarByClass(MovieRatingAverage.class);
        job.setMapperClass(RatingMapper.class);
        job.setReducerClass(RatingReducer.class);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(DoubleWritable.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        job.setNumReduceTasks(1);

        job.addCacheFile(new URI(
                "hdfs://localhost:8020/user/cloudera/lab1/ml/movies.txt"));

        // args[0] = ratings_1.txt
        // args[1] = ratings_2.txt
        // args[2] = output directory
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileInputFormat.addInputPath(job, new Path(args[1]));
        FileOutputFormat.setOutputPath(job, new Path(args[2]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
