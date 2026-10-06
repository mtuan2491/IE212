# Data — Lab 1

## 1. `trans/` — Sports Center Transactions

Used for the in-class exercises (`TransAnalysis1–6`).

> 📦 Files used only for Assignment 1 (`cust20_*`, `profession*`, `trans240_20*`) were moved to `_archive/Lab 1 - Assignment 1/data/trans/` on 15/09/2026.

### Transaction files

| File | Number of lines | Used in |
|---|---:|---|
| `trans240_1.txt`, `trans240_2.txt` | 120 each | TransAnalysis 1–6 |

**Schema** (comma-separated, **no header**):

```text
TransID, Date, CustID, Cost, Game, Equipment, City, State, Mode
```

Example:

```text
0,Jun-26-2011,4000001,40.33,Exercise & Fitness,Cardio Machine Accessories,Clarksville,Tennessee,credit
```

> ⚠️ **The date format is `Jun-26-2011`** (month written as an abbreviation), **not** `06-26-2011`. The document `vi-du/Giải thích TransAnalysis.docx` uses `06-26-2011` in its example, which **does not match the actual data**. If the month is extracted using `Date.split("-")[0]`, the result will be the string `"Jun"`, not a number. The document should be corrected or this should be explained clearly to students.

> ⚠️ The `Game` column contains values with an **ampersand** (`Exercise & Fitness`), and the `Equipment` column contains **spaces**. Do not split records by whitespace.

### Customer file

`cust.txt` (10 lines):

```text
CustID, FirstName, LastName, Age, Profession
4000001,Kristina,Chung,55,Pilot
```

---

## 2. `movielens-mini/` — Mini MovieLens Dataset (Version A)

Used for the **submission section** (`de-bai/Phan-B-MovieLens-MapReduce.docx`).

| File | Number of lines |
|---|---:|
| `movies.txt` | 50 |
| `ratings_1.txt`, `ratings_2.txt` | 50 each |
| `users.txt` | 50 |

**Schema:**

```text
movies.txt   : MovieID, Title, Genres          (Genres are separated by "|")
ratings_1/2  : UserID, MovieID, Rating, Timestamp
users.txt    : UserID, Gender, Age, Occupation, Zip-code
```

Example:

```text
1043, Toy Story (1995), Animation|Children|Comedy
537, 1043, 4.0, 964982703
537, F, 25, 10, 48067
```

> ⚠️ **There is a space after each comma.** You must call `trim()` after `split(",")`; otherwise, `Integer.parseInt(" 1043")` will throw a `NumberFormatException`. This is one of the most common mistakes students make in this lab.

---

## 3. ⚠️ Important Note: The Two MovieLens Datasets Are NOT the Same

The dataset here (**Version A**) and the dataset in `Lab 2 - Spark RDD & DataFrame/data/movielens-mini/` (**Version B**) are **different datasets**:

| | Version A (Lab 1) | Version B (Lab 2) |
|---|---|---|
| Delimiter format | `,` + **space** | `,` with no space |
| MovieID range | 1043, 2589, 3791… | 1001–1030 |
| Timestamp | ~964982703 (year 2000) | ~1577836800 (year 2020) |
| Number of ratings | 100 | 184 |
| Includes `occupation.txt` | ❌ | ✅ |

**Consequence:** the exercise *"compare MapReduce vs RDD vs DataFrame on the same problem"* in Lab 2 **cannot compare numerical results directly** if the two labs use different datasets.

**Decision required:** standardize both labs on **one** dataset (recommended: **Version B** — cleaner, contains more data, and also includes `occupation.txt`), then copy it into both labs. See the outstanding tasks section in `TONG-HOP-NOI-DUNG-LAB.md`.

---

## 4. Uploading Data to HDFS

On the **Cloudera QuickStart VM**, the HDFS home directory is `/user/cloudera`:

```bash
hdfs dfs -mkdir -p /user/cloudera/lab1/trans
hdfs dfs -put trans/trans240_1.txt trans/trans240_2.txt /user/cloudera/lab1/trans/
hdfs dfs -ls -R /user/cloudera/lab1
```

**Required for `TransAnalysis5` and `TransAnalysis6`** — both programs load the file through Distributed Cache using the URI `hdfs://localhost:8020/mycache/cust` (Slide 4, page 16), so the file must be placed at exactly that path and **must be named `cust`, without the `.txt` extension**:

```bash
hdfs dfs -mkdir -p /mycache
hdfs dfs -put trans/cust.txt /mycache/cust
hdfs dfs -ls /mycache
```

> 💡 These steps should be completed **before class** — see section 6 in `../00-setup/README.md`.
