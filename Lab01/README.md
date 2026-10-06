# Lab 01 - Hadoop, HDFS and MapReduce

Lab 01 introduces the basic workflow of working with **Hadoop**, **HDFS**, and **MapReduce** on the Cloudera QuickStart environment.

The lab includes transaction-analysis exercises and MovieLens-style rating-analysis exercises implemented in Java.

## Folder Structure

```text
Lab01/
├── data/
│   ├── movielens/
│   │   ├── movies.txt
│   │   ├── ratings_1.txt
│   │   ├── ratings_2.txt
│   │   └── users.txt
│   ├── trans/
│   │   ├── cust.txt
│   │   └── trans.txt
│   └── README.md
│
├── src/
│   ├── TransAnalysis1.java
│   ├── TransAnalysis2.java
│   ├── TransAnalysis3.java
│   ├── TransAnalysis4.java
│   ├── TransAnalysis5.java
│   ├── TransAnalysis6.java
│   ├── MovieRatingAverage.java
│   ├── GenreRatingAverage.java
│   └── GenderRatingAverage.java
│
├── docs/
│   ├── Huong_dan_Lab1_Hadoop_MapReduce.md
│   └── screenshots/
│       ├── setup/
│       ├── B01/
│       ├── B02/
│       ├── B03/
│       ├── B04/
│       ├── B05/
│       ├── B06/
│       ├── C01_1/
│       ├── C01_2/
│       └── C01_3/
│
├── report/
│   └── 23521720_Lab_1.pdf
│
└── README.md
```

## Exercises

### Part B - Transaction Analysis

| Exercise | Java class | Main task |
| --- | --- | --- |
| B.1 | `TransAnalysis1` | Calculate total transaction amount by game type |
| B.2 | `TransAnalysis2` | Add the list of customer IDs for each game type |
| B.3 | `TransAnalysis3` | Remove duplicate customer IDs |
| B.4 | `TransAnalysis4` | Count distinct customers instead of listing them |
| B.5 | `TransAnalysis5` | Use Distributed Cache to map customer IDs to names |
| B.6 | `TransAnalysis6` | Add customer age and calculate totals correctly |

### Part C.1 - Rating Analysis

| Exercise | Java class | Main task |
| --- | --- | --- |
| C.1.1 | `MovieRatingAverage` | Calculate average rating and rating count by movie, then determine the highest-rated movie |
| C.1.2 | `GenreRatingAverage` | Calculate average rating and rating count by genre |
| C.1.3 | `GenderRatingAverage` | Calculate average rating by gender for each movie using a reduce-side join |

Part C.1 is required. Part C.2 is optional and is not included in this folder.

## Environment

The lab was completed using:

- Cloudera QuickStart VM
- Hadoop
- HDFS
- MapReduce
- Java
- Eclipse
- VMware

## Local Working Paths

Files copied into the Cloudera VM were stored under:

```text
/home/cloudera/Lab01/
```

The Eclipse project was stored separately under:

```text
/home/cloudera/workspace/Lab01/
```

The exported JAR used to run all exercises was:

```text
/home/cloudera/Lab01/lab1.jar
```

## HDFS Layout

```text
/user/cloudera/lab1/
├── trans/
│   └── trans.txt
└── ml/
    ├── movies.txt
    ├── ratings_1.txt
    ├── ratings_2.txt
    └── users.txt
```

The customer file used by the Distributed Cache exercises is stored at:

```text
/mycache/cust
```

## Build

The Java files are imported into an Eclipse Java project and compiled with the Hadoop libraries from:

```text
/usr/lib/hadoop/client
```

The project is then exported as:

```text
/home/cloudera/Lab01/lab1.jar
```

To verify the JAR:

```bash
jar tf /home/cloudera/Lab01/lab1.jar | grep TransAnalysis
jar tf /home/cloudera/Lab01/lab1.jar | grep RatingAverage
```

## Running the Lab

Each Hadoop exercise follows the same general workflow:

```bash
hdfs dfs -rm -r -f <output-path>
hadoop jar /home/cloudera/Lab01/lab1.jar <MainClass> <input...> <output-path>
hdfs dfs -cat <output-path>/part-r-00000
```

Detailed commands for every exercise are available in:

```text
docs/Huong_dan_Lab1_Hadoop_MapReduce.md
```

## Screenshots

The `docs/` directory contains the detailed Lab 01 guide and its supporting screenshots. Screenshots are organized under `docs/screenshots/` as follows:

- `setup/` documents copying files into Cloudera, verifying the HDFS input data, verifying the Distributed Cache, and verifying the generated JAR classes.
- `B01/` through `B06/` contain execution and output evidence for exercises B.1 through B.6.
- `C01_1/` through `C01_3/` contain execution and output evidence for the three required Part C.1 exercises.

Each exercise directory normally contains:

- `*-hadoop-jar.png`: the `hadoop jar` command and successful job execution.
- `*-output.png`: the `hdfs dfs -cat` command and resulting output.

When an exercise requires more than one output screenshot, the output filenames use numbered suffixes such as `*-output-1.png` and `*-output-2.png`.

## Report

For each exercise, the report contains:

1. A screenshot of the `hadoop jar` command and successful job completion.
2. A screenshot of the `hdfs dfs -cat` command and its output.

The long Hadoop `Counters` section is not required in the report.

## Submission

The lab submission follows the format:

```text
<MSSV>-Lab1.zip
```

The archive contains:

- Java source files for the exercises
- The final PDF report

Generated Eclipse metadata and compiled build files are not required for submission.
