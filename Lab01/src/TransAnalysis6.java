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

public class TransAnalysis6 {

    // Game_type List_of_Names_of_all_distinct_players_with_age Total_amount
    public static class TransMapper extends Mapper<Object, Text, Text, Text> {

        // CustID -> "FirstName,Age"
        private Map<Integer, String> userMap = new HashMap<Integer, String>();

        public void setup(Context context) throws IOException, InterruptedException {
            try (BufferedReader br = new BufferedReader(new FileReader("cust"))) {
                String line;

                while ((line = br.readLine()) != null) {
                    String[] columns = line.split(",");

                    int id = Integer.parseInt(columns[0]);
                    String name = columns[1];
                    String age = columns[3];

                    userMap.put(id, name + "," + age);
                }
            }
        }

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String record = value.toString().trim();
            String[] parts = record.split(",");

            String gametype = parts[4];
            String id = parts[2];
            String amount = parts[3];

            String nameAndAge = userMap.get(Integer.parseInt(id));

            // Value has 4 parts after split(","):
            // id, name, age, amount
            context.write(new Text(gametype),
                    new Text(id + "," + nameAndAge + "," + amount));
        }
    }

    public static class TransReducer extends Reducer<Text, Text, Text, Text> {
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {

            List<String> IDs = new ArrayList<String>();
            double total = 0.0;
            String playerList = "";

            for (Text t : values) {
                String[] parts = t.toString().trim().split(",");

                String id = parts[0];
                String name = parts[1];
                String age = parts[2];

                // parts[3] is amount.
                total += Float.parseFloat(parts[3]);

                if (!IDs.contains(id)) {
                    IDs.add(id);
                    playerList += name + "," + age + ",";
                }
            }

            if (playerList.length() > 0) {
                playerList = playerList.substring(0, playerList.length() - 1);
                playerList = "[" + playerList + "]";
            }

            context.write(key,
                    new Text(playerList + "   " + Double.toString(total)));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Trans analysis 6");

        job.setJarByClass(TransAnalysis6.class);
        job.setMapperClass(TransMapper.class);
        job.setReducerClass(TransReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

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
