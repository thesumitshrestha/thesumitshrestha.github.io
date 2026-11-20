"""Per-page "Learn more" links. Each entry: (kind, title, url, why).

kind is one of: video, course, read, visual, practice, book, paper.
YouTube links that end in a search are labeled "(YouTube search)" so it's clear
they open a list of videos on that topic rather than one fixed video.
"""
from urllib.parse import quote_plus


def yt(q):
    return "https://www.youtube.com/results?search_query=" + quote_plus(q)


TIH = "https://www.techinterviewhandbook.org/algorithms/"
SDP = "https://github.com/donnemartin/system-design-primer#"
NEET = "https://neetcode.io/roadmap"
MIT006 = "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
FISET_DS = "https://www.youtube.com/watch?v=RBSGKlAvoiM"
BBG = "https://www.youtube.com/@ByteByteGo"
GKCS = "https://www.youtube.com/@gkcs"
JORDAN = "https://www.youtube.com/@jordanhasnolife5163"
HELLO = "https://www.hellointerview.com/learn/system-design/in-a-hurry"
SD101 = "https://github.com/ByteByteGoHq/system-design-101"
USFCA = "https://www.cs.usfca.edu/~galles/visualization/Algorithms.html"

LEARN = {
    "arrays": [
        ("video", "NeetCode: arrays, two pointers and sliding window (YouTube search)", yt("neetcode two pointers sliding window arrays"), "Short, clear walkthroughs of the exact checklist problems"),
        ("course", "Data Structures Easy to Advanced (William Fiset, freeCodeCamp)", FISET_DS, "Free 8-hour course by an ex-Google engineer; watch the array and dynamic array parts"),
        ("read", "Tech Interview Handbook: Array cheatsheet", TIH + "array/", "Corner cases and techniques in one page"),
        ("practice", "NeetCode roadmap: Arrays & Hashing, Two Pointers", NEET, "Same patterns, ordered by difficulty"),
    ],
    "strings": [
        ("video", "NeetCode: sliding window and palindrome problems (YouTube search)", yt("neetcode longest substring without repeating characters sliding window"), "Watch after attempting each problem"),
        ("read", "Tech Interview Handbook: String cheatsheet", TIH + "string/", "Anagram, palindrome and counting techniques"),
        ("practice", "NeetCode roadmap: Sliding Window", NEET, "Six graded window problems"),
    ],
    "linked-lists": [
        ("video", "NeetCode: linked list problems (YouTube search)", yt("neetcode reverse linked list reorder list"), "Pointer rewiring drawn step by step"),
        ("course", "William Fiset: linked lists (in the freeCodeCamp course)", FISET_DS, "Singly vs doubly linked lists explained with diagrams"),
        ("read", "Tech Interview Handbook: Linked list cheatsheet", TIH + "linked-list/", "Dummy nodes, fast/slow pointers, common traps"),
        ("visual", "VisuAlgo: linked list", "https://visualgo.net/en/list", "Watch inserts and deletes animate"),
    ],
    "trees": [
        ("video", "NeetCode: binary tree and trie problems (YouTube search)", yt("neetcode binary tree maximum path sum diameter"), "DFS return-value thinking, problem by problem"),
        ("course", "MIT 6.006 (Spring 2020): binary trees and AVL lectures", MIT006, "University-level explanations, free on MIT OpenCourseWare"),
        ("read", "Tech Interview Handbook: Tree and Trie cheatsheets", TIH + "tree/", "Traversals, BST rules and trie tips"),
        ("visual", "VisuAlgo: binary search tree", "https://visualgo.net/en/bst", "Insert, delete and traverse with animation"),
    ],
    "stacks-queues": [
        ("video", "NeetCode: monotonic stack problems (YouTube search)", yt("neetcode daily temperatures largest rectangle in histogram monotonic stack"), "The trickiest pattern on this page, visualized"),
        ("read", "Tech Interview Handbook: Stack and Queue cheatsheets", TIH + "stack/", "When to reach for each"),
        ("practice", "NeetCode roadmap: Stack", NEET, "Graded stack problems"),
    ],
    "graphs": [
        ("video", "William Fiset: graph theory series (YouTube search)", yt("William Fiset graph theory algorithms"), "BFS, DFS, topological sort, Dijkstra, union-find, each in 10–15 minutes"),
        ("video", "NeetCode: graph problems (YouTube search)", yt("neetcode number of islands course schedule graph"), "Interview-style solutions to the checklist problems"),
        ("video", "Abdul Bari: Dijkstra and graph algorithms (YouTube search)", yt("Abdul Bari dijkstra algorithm"), "Whiteboard explanations of how the algorithms work"),
        ("read", "Tech Interview Handbook: Graph cheatsheet", TIH + "graph/", "Templates and corner cases"),
        ("visual", "USFCA algorithm visualizations: BFS, DFS, Dijkstra, topological sort", USFCA, "Step through algorithms on your own graphs"),
    ],
    "dp": [
        ("video", "NeetCode: dynamic programming problems (YouTube search)", yt("neetcode dynamic programming coin change house robber"), "From recursion to table, one problem at a time"),
        ("video", "Abdul Bari: dynamic programming (YouTube search)", yt("Abdul Bari dynamic programming"), "Classic DP explained on a whiteboard"),
        ("video", "freeCodeCamp: Dynamic Programming for beginners (YouTube search)", yt("freeCodeCamp dynamic programming learn to solve algorithmic problems coding challenges"), "A popular 5-hour course on memoization and tabulation"),
        ("read", "Tech Interview Handbook: Dynamic programming and Recursion", TIH + "dynamic-programming/", "How to spot DP and set up the state"),
    ],
    "heaps": [
        ("video", "NeetCode: heap / priority queue problems (YouTube search)", yt("neetcode find median from data stream kth largest heap"), "Two heaps and top-k explained"),
        ("video", "Abdul Bari: heap and heap sort (YouTube search)", yt("Abdul Bari heap sort heapify"), "How sift-up and sift-down really work"),
        ("read", "Tech Interview Handbook: Heap cheatsheet", TIH + "heap/", "Top-k and merge-k techniques"),
        ("visual", "VisuAlgo: binary heap", "https://visualgo.net/en/heap", "Watch pushes and pops reorder the tree"),
    ],
    "hashing": [
        ("video", "NeetCode: arrays and hashing problems (YouTube search)", yt("neetcode arrays and hashing group anagrams"), "Hashmap patterns in action"),
        ("course", "MIT 6.006 (Spring 2020): hashing lecture", MIT006, "How hash tables really work, including collisions"),
        ("read", "Tech Interview Handbook: Hash table cheatsheet", TIH + "hash-table/", "Common uses and gotchas"),
        ("visual", "VisuAlgo: hash table", "https://visualgo.net/en/hashtable", "Collisions, probing and chaining animated"),
    ],
    "bits": [
        ("video", "NeetCode: bit manipulation problems (YouTube search)", yt("neetcode bit manipulation single number counting bits"), "Short solutions to the checklist problems"),
        ("read", "Tech Interview Handbook: Binary cheatsheet", TIH + "binary/", "Bit tricks and edge cases"),
        ("practice", "NeetCode roadmap: Bit Manipulation", NEET, "Graded bit problems"),
    ],
    "sorting": [
        ("video", "Abdul Bari: merge sort and quick sort (YouTube search)", yt("Abdul Bari merge sort quick sort"), "Clear step-by-step traces"),
        ("course", "MIT 6.006 (Spring 2020): sorting lectures", MIT006, "Why O(n log n), and counting/radix sort"),
        ("read", "Tech Interview Handbook: Sorting and searching, and Interval cheatsheets", TIH + "sorting-searching/", "When sorting first helps"),
        ("visual", "VisuAlgo: sorting", "https://visualgo.net/en/sorting", "Compare sorting algorithms side by side"),
    ],
    "searching": [
        ("video", "NeetCode: binary search problems (YouTube search)", yt("neetcode binary search koko eating bananas rotated sorted array"), "Search on index and on answer"),
        ("read", "Tech Interview Handbook: Sorting and searching cheatsheet", TIH + "sorting-searching/", "Binary search templates and traps"),
        ("practice", "NeetCode roadmap: Binary Search", NEET, "Graded binary search problems"),
    ],
    "patterns": [
        ("read", "freeCodeCamp: DSA patterns for LeetCode interviews", "https://www.freecodecamp.org/news/data-structure-and-algorithm-patterns-for-leetcode-interviews/", "Another take on mapping problems to patterns"),
        ("practice", "NeetCode roadmap", NEET, "150 problems grouped by pattern"),
        ("read", "Tech Interview Handbook: study cheatsheets", TIH + "study-cheatsheet/", "One-page overview of every topic"),
    ],
    "python": [
        ("read", "Python docs: collections", "https://docs.python.org/3/library/collections.html", "Counter, deque, defaultdict"),
        ("read", "Python docs: heapq and bisect", "https://docs.python.org/3/library/heapq.html", "Exact behavior of the heap functions"),
        ("read", "Python wiki: time complexity of built-ins", "https://wiki.python.org/moin/TimeComplexity", "What each list, dict and set operation costs"),
    ],
    "interview": [
        ("read", "Google: How we hire", "https://www.google.com/about/careers/applications/how-we-hire/", "Google's own description of the process"),
        ("read", "Tech Interview Handbook: coding interview prep", "https://www.techinterviewhandbook.org/", "Free guide covering the whole process"),
        ("practice", "Pramp (free mock interviews)", "https://www.pramp.com/", "Practice talking out loud with another candidate"),
        ("practice", "Interviewing.io (mock interviews)", "https://interviewing.io/", "Mocks with engineers from big tech companies"),
    ],
    # ---------------- system design ----------------
    "sd-basics": [
        ("video", "freeCodeCamp: System Design for Beginners", "https://www.youtube.com/watch?v=m8Icp_Cid5o", "A full beginner course in one video"),
        ("video", "Jordan has no life: \"What is Systems Design?\" (ex-Google SWE series)", "https://www.youtube.com/watch?v=bwt09KXDH94", "Start of a 0-to-1 interview playlist"),
        ("read", "System Design Primer: latency numbers and back-of-envelope math", SDP + "appendix", "Powers of two and latency tables"),
        ("read", "Hello Interview: System Design in a Hurry", HELLO, "Short, interview-focused overview"),
    ],
    "sd-scaling": [
        ("video", "ByteByteGo channel (load balancers, CDNs, scaling)", BBG, "Animated 5–10 minute explainers by the author of System Design Interview"),
        ("video", "Gaurav Sen: horizontal vs vertical scaling, load balancing (YouTube search)", yt("Gaurav Sen horizontal vs vertical scaling load balancing"), "Beginner-friendly whiteboard videos"),
        ("read", "System Design Primer: load balancer", SDP + "load-balancer", "Layer 4 vs layer 7, active-passive"),
        ("read", "System Design Primer: content delivery network", SDP + "content-delivery-network", "Push vs pull CDNs"),
    ],
    "sd-caching": [
        ("video", "ByteByteGo: caching explained (YouTube search)", yt("ByteByteGo cache strategies"), "Cache-aside vs write-through animated"),
        ("read", "System Design Primer: cache", SDP + "cache", "Every caching layer and update strategy"),
        ("read", "Redis documentation", "https://redis.io/docs/latest/", "The cache most designs use"),
    ],
    "sd-data": [
        ("video", "Gaurav Sen: consistent hashing and sharding (YouTube search)", yt("Gaurav Sen consistent hashing database sharding"), "The classic intuitive explanation"),
        ("video", "ByteByteGo: SQL vs NoSQL, sharding, CAP (YouTube search)", yt("ByteByteGo database sharding CAP theorem"), "Short animated explainers"),
        ("book", "Designing Data-Intensive Applications, 2nd edition (Kleppmann)", "https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/", "The best book on databases, replication and partitioning"),
        ("paper", "Bigtable paper (Google, 2006)", "https://research.google.com/archive/bigtable-osdi06.pdf", "How Google's wide-column store works"),
        ("read", "System Design Primer: database", SDP + "database", "Replication, federation, sharding, denormalization"),
    ],
    "sd-async": [
        ("video", "ByteByteGo: message queues, Kafka, API styles (YouTube search)", yt("ByteByteGo message queue kafka REST gRPC"), "Visual comparisons"),
        ("read", "System Design Primer: asynchronism and communication", SDP + "asynchronism", "Queues, back pressure, REST vs RPC"),
        ("read", "ByteByteGo: System Design 101 (GitHub)", SD101, "Hundreds of free diagrams on APIs, protocols and more"),
    ],
    "sd-reliability": [
        ("course", "Martin Kleppmann: Distributed Systems lectures (Cambridge)", "https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/materials.html", "Free notes and video lectures on clocks, replication, consensus"),
        ("course", "MIT 6.5840 Distributed Systems", "https://pdos.csail.mit.edu/6.824/", "The famous MIT course: papers, lectures and labs"),
        ("visual", "The Secret Lives of Data: Raft", "https://thesecretlivesofdata.com/raft/", "An animated walkthrough of leader election and log replication"),
        ("read", "Google SRE books (free online)", "https://sre.google/books/", "SLOs, error budgets, handling overload, from Google itself"),
        ("paper", "MapReduce paper (Google, 2004)", "https://research.google.com/archive/mapreduce.html", "The batch processing model behind Hadoop and Spark"),
    ],
    "sd-cases-1": [
        ("video", "Gaurav Sen and ByteByteGo: URL shortener and rate limiter (YouTube search)", yt("system design URL shortener rate limiter interview"), "Compare other people's designs with yours"),
        ("read", "Hello Interview: Bit.ly and web crawler breakdowns", "https://hellointerview.com/learn/system-design", "Detailed written answers with follow-up questions"),
        ("read", "System Design Primer: interview questions with solutions", SDP + "system-design-interview-questions-with-solutions", "Pastebin, web crawler and more"),
    ],
    "sd-cases-2": [
        ("video", "Jordan has no life: news feed, chat and more designs", JORDAN, "Deep, detailed design videos by an ex-Google engineer"),
        ("video", "ByteByteGo: design a chat system / news feed (YouTube search)", yt("ByteByteGo design chat system news feed"), "Animated case studies"),
        ("read", "Hello Interview: product design breakdowns", "https://hellointerview.com/learn/system-design", "News feed, WhatsApp, typeahead and more"),
    ],
    "sd-interview": [
        ("read", "Hello Interview: System Design in a Hurry", HELLO, "The delivery framework and what interviewers want"),
        ("read", "System Design Primer (GitHub)", "https://github.com/donnemartin/system-design-primer", "The most-starred free system design guide"),
        ("book", "System Design Interview, Vol. 1 and 2 (Alex Xu)", "https://bytebytego.com/", "Step-by-step interview designs; the ByteByteGo site has the content"),
        ("practice", "Pramp / Interviewing.io system design mocks", "https://interviewing.io/", "Practice out loud with a real person"),
    ],
}
