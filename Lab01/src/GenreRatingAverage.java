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
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

// C.1.2
public class GenreRatingAverage {

    public static class GenreMapper
            extends Mapper<Object, Text, Text, DoubleWritable> {

        // MovieID -> Genres
        private Map<Integer, String> genreMap = new HashMap<Integer, String>();

        protected void setup(Context context) throws IOException {
            BufferedReader br = new BufferedReader(new FileReader("movies.txt"));
            String line;

            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",", 3);

                int movieId = Integer.parseInt(parts[0].trim());
                String genres = parts[2].trim();

                genreMap.put(movieId, genres);
            }

            br.close();
        }

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String[] parts = value.toString().split(",");
            if (parts.length < 4) {
                return;
            }

            int movieId = Integer.parseInt(parts[1].trim());
            double rating = Double.parseDouble(parts[2].trim());

            String genres = genreMap.get(movieId);
            if (genres == null) {
                return;
            }

            String[] genreList = genres.split("\\|");

            for (String genre : genreList) {
                context.write(new Text(genre.trim()),
                        new DoubleWritable(rating));
            }
        }
    }

    public static class GenreReducer
            extends Reducer<Text, DoubleWritable, Text, Text> {

        public void reduce(Text key, Iterable<DoubleWritable> values,
                Context context) throws IOException, InterruptedException {

            double sum = 0.0;
            int count = 0;

            for (DoubleWritable value : values) {
                sum += value.get();
                count++;
            }

            double average = sum / count;

            context.write(key,
                    new Text(String.format(Locale.US, "%.2f (%d)",
                            average, count)));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Genre rating average");

        job.setJarByClass(GenreRatingAverage.class);
        job.setMapperClass(GenreMapper.class);
        job.setReducerClass(GenreReducer.class);

        job.setMapOutputKeyClass(Text.class);
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
