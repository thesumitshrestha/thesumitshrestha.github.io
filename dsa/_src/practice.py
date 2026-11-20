"""LeetCode practice links.

PATTERN_LC[slug] is a list, one entry per <article class="pattern"> on that page, in order.
Each entry is a list of (name, leetcode-slug, level, premium?).
DEEP_LC[slug] links the problem worked in the page's "Deep analysis" section.
SD_LC[slug] lists coding problems that mirror a system design page's ideas.
Levels follow LeetCode's own labels (your checklist may label a few differently).
"""
E, M, H = "easy", "medium", "hard"
P = True  # LeetCode Premium

PATTERN_LC = {
    "arrays": [
        [("Two Sum", "two-sum", E), ("Contains Duplicate II", "contains-duplicate-ii", E), ("4Sum II", "4sum-ii", M)],
        [("Two Sum II", "two-sum-ii-input-array-is-sorted", M), ("3Sum", "3sum", M), ("3Sum Closest", "3sum-closest", M), ("Container With Most Water", "container-with-most-water", M)],
        [("Range Sum Query - Immutable", "range-sum-query-immutable", E), ("Find Pivot Index", "find-pivot-index", E), ("Subarray Sum Equals K", "subarray-sum-equals-k", M), ("Continuous Subarray Sum", "continuous-subarray-sum", M)],
        [("Maximum Subarray", "maximum-subarray", M), ("Maximum Product Subarray", "maximum-product-subarray", M), ("Maximum Sum Circular Subarray", "maximum-sum-circular-subarray", M)],
        [("Find All Numbers Disappeared in an Array", "find-all-numbers-disappeared-in-an-array", E), ("Find the Duplicate Number", "find-the-duplicate-number", M), ("Set Matrix Zeroes", "set-matrix-zeroes", M), ("First Missing Positive", "first-missing-positive", H)],
        [("Spiral Matrix", "spiral-matrix", M), ("Spiral Matrix II", "spiral-matrix-ii", M), ("Rotate Image", "rotate-image", M), ("Diagonal Traverse", "diagonal-traverse", M)],
    ],
    "strings": [
        [("Valid Anagram", "valid-anagram", E), ("First Unique Character in a String", "first-unique-character-in-a-string", E), ("Group Anagrams", "group-anagrams", M)],
        [("Longest Substring Without Repeating Characters", "longest-substring-without-repeating-characters", M), ("Permutation in String", "permutation-in-string", M), ("Longest Repeating Character Replacement", "longest-repeating-character-replacement", M), ("Minimum Window Substring", "minimum-window-substring", H)],
        [("Valid Palindrome", "valid-palindrome", E), ("Valid Palindrome II", "valid-palindrome-ii", E), ("Reverse String", "reverse-string", E)],
        [("Longest Palindromic Substring", "longest-palindromic-substring", M), ("Palindromic Substrings", "palindromic-substrings", M)],
        [("String to Integer (atoi)", "string-to-integer-atoi", M), ("Decode String", "decode-string", M), ("Basic Calculator II", "basic-calculator-ii", M)],
    ],
    "linked-lists": [
        [("Merge Two Sorted Lists", "merge-two-sorted-lists", E), ("Remove Linked List Elements", "remove-linked-list-elements", E), ("Partition List", "partition-list", M)],
        [("Reverse Linked List", "reverse-linked-list", E), ("Palindrome Linked List", "palindrome-linked-list", E), ("Reverse Linked List II", "reverse-linked-list-ii", M), ("Reverse Nodes in k-Group", "reverse-nodes-in-k-group", H)],
        [("Middle of the Linked List", "middle-of-the-linked-list", E), ("Linked List Cycle", "linked-list-cycle", E), ("Linked List Cycle II", "linked-list-cycle-ii", M), ("Find the Duplicate Number", "find-the-duplicate-number", M)],
        [("Remove Nth Node From End of List", "remove-nth-node-from-end-of-list", M), ("Rotate List", "rotate-list", M)],
        [("Copy List with Random Pointer", "copy-list-with-random-pointer", M), ("Clone Graph", "clone-graph", M)],
    ],
    "trees": [
        [("Maximum Depth of Binary Tree", "maximum-depth-of-binary-tree", E), ("Balanced Binary Tree", "balanced-binary-tree", E), ("Same Tree", "same-tree", E), ("Path Sum", "path-sum", E)],
        [("Diameter of Binary Tree", "diameter-of-binary-tree", E), ("Longest Univalue Path", "longest-univalue-path", M), ("Binary Tree Maximum Path Sum", "binary-tree-maximum-path-sum", H)],
        [("Minimum Depth of Binary Tree", "minimum-depth-of-binary-tree", E), ("Binary Tree Level Order Traversal", "binary-tree-level-order-traversal", M), ("Binary Tree Right Side View", "binary-tree-right-side-view", M), ("Binary Tree Zigzag Level Order Traversal", "binary-tree-zigzag-level-order-traversal", M)],
        [("Range Sum of BST", "range-sum-of-bst", E), ("Validate Binary Search Tree", "validate-binary-search-tree", M), ("Kth Smallest Element in a BST", "kth-smallest-element-in-a-bst", M)],
        [("Lowest Common Ancestor of a BST", "lowest-common-ancestor-of-a-binary-search-tree", M), ("Lowest Common Ancestor of a Binary Tree", "lowest-common-ancestor-of-a-binary-tree", M)],
        [("Implement Trie", "implement-trie-prefix-tree", M), ("Design Add and Search Words", "design-add-and-search-words-data-structure", M), ("Word Search II", "word-search-ii", H)],
    ],
    "stacks-queues": [
        [("Valid Parentheses", "valid-parentheses", E), ("Minimum Remove to Make Valid Parentheses", "minimum-remove-to-make-valid-parentheses", M), ("Longest Valid Parentheses", "longest-valid-parentheses", H)],
        [("Next Greater Element I", "next-greater-element-i", E), ("Daily Temperatures", "daily-temperatures", M), ("Online Stock Span", "online-stock-span", M), ("Largest Rectangle in Histogram", "largest-rectangle-in-histogram", H)],
        [("Implement Queue using Stacks", "implement-queue-using-stacks", E), ("Min Stack", "min-stack", M)],
        [("Evaluate Reverse Polish Notation", "evaluate-reverse-polish-notation", M), ("Decode String", "decode-string", M), ("Simplify Path", "simplify-path", M), ("Basic Calculator", "basic-calculator", H)],
        [("Sliding Window Maximum", "sliding-window-maximum", H), ("Shortest Subarray with Sum at Least K", "shortest-subarray-with-sum-at-least-k", H)],
    ],
    "graphs": [
        [("Shortest Path in Binary Matrix", "shortest-path-in-binary-matrix", M), ("01 Matrix", "01-matrix", M), ("Open the Lock", "open-the-lock", M)],
        [("Number of Islands", "number-of-islands", M), ("Max Area of Island", "max-area-of-island", M), ("Surrounded Regions", "surrounded-regions", M), ("Clone Graph", "clone-graph", M)],
        [("Rotting Oranges", "rotting-oranges", M), ("As Far from Land as Possible", "as-far-from-land-as-possible", M), ("Walls and Gates", "walls-and-gates", M, P)],
        [("Course Schedule", "course-schedule", M), ("Course Schedule II", "course-schedule-ii", M), ("Alien Dictionary", "alien-dictionary", H, P)],
        [("Number of Provinces", "number-of-provinces", M), ("Redundant Connection", "redundant-connection", M), ("Accounts Merge", "accounts-merge", M)],
        [("Network Delay Time", "network-delay-time", M), ("Path With Minimum Effort", "path-with-minimum-effort", M), ("Cheapest Flights Within K Stops", "cheapest-flights-within-k-stops", M), ("Swim in Rising Water", "swim-in-rising-water", H)],
    ],
    "dp": [
        [("Subsets", "subsets", M), ("Subsets II", "subsets-ii", M), ("Permutations", "permutations", M), ("Combination Sum", "combination-sum", M), ("N-Queens", "n-queens", H)],
        [("Fibonacci Number", "fibonacci-number", E), ("Climbing Stairs", "climbing-stairs", E), ("Decode Ways", "decode-ways", M)],
        [("Coin Change", "coin-change", M), ("Coin Change II", "coin-change-ii", M), ("Perfect Squares", "perfect-squares", M)],
        [("Min Cost Climbing Stairs", "min-cost-climbing-stairs", E), ("House Robber", "house-robber", M), ("House Robber II", "house-robber-ii", M), ("Delete and Earn", "delete-and-earn", M)],
        [("Unique Paths", "unique-paths", M), ("Minimum Path Sum", "minimum-path-sum", M), ("Longest Common Subsequence", "longest-common-subsequence", M), ("Edit Distance", "edit-distance", M)],
        [("Partition Equal Subset Sum", "partition-equal-subset-sum", M), ("Target Sum", "target-sum", M), ("Last Stone Weight II", "last-stone-weight-ii", M)],
    ],
    "heaps": [
        [("Kth Largest Element in a Stream", "kth-largest-element-in-a-stream", E), ("Kth Largest Element in an Array", "kth-largest-element-in-an-array", M), ("K Closest Points to Origin", "k-closest-points-to-origin", M)],
        [("Top K Frequent Elements", "top-k-frequent-elements", M), ("Top K Frequent Words", "top-k-frequent-words", M), ("Sort Characters By Frequency", "sort-characters-by-frequency", M)],
        [("Find K Pairs with Smallest Sums", "find-k-pairs-with-smallest-sums", M), ("Kth Smallest Element in a Sorted Matrix", "kth-smallest-element-in-a-sorted-matrix", M), ("Merge k Sorted Lists", "merge-k-sorted-lists", H)],
        [("Find Median from Data Stream", "find-median-from-data-stream", H), ("Sliding Window Median", "sliding-window-median", H)],
        [("Task Scheduler", "task-scheduler", M), ("Reorganize String", "reorganize-string", M), ("Meeting Rooms II", "meeting-rooms-ii", M, P), ("IPO", "ipo", H)],
    ],
    "hashing": [
        [("Contains Duplicate", "contains-duplicate", E), ("Happy Number", "happy-number", E), ("Longest Consecutive Sequence", "longest-consecutive-sequence", M)],
        [("Ransom Note", "ransom-note", E), ("Majority Element", "majority-element", E), ("Top K Frequent Elements", "top-k-frequent-elements", M)],
        [("Isomorphic Strings", "isomorphic-strings", E), ("Word Pattern", "word-pattern", E)],
        [("Group Anagrams", "group-anagrams", M), ("Valid Sudoku", "valid-sudoku", M), ("Group Shifted Strings", "group-shifted-strings", M, P)],
        [("Subarray Sum Equals K", "subarray-sum-equals-k", M), ("Contiguous Array", "contiguous-array", M), ("Continuous Subarray Sum", "continuous-subarray-sum", M)],
        [("Design HashMap", "design-hashmap", E), ("Insert Delete GetRandom O(1)", "insert-delete-getrandom-o1", M), ("LRU Cache", "lru-cache", M)],
    ],
    "bits": [
        [("Single Number", "single-number", E), ("Missing Number", "missing-number", E), ("Find the Difference", "find-the-difference", E)],
        [("Number of 1 Bits", "number-of-1-bits", E), ("Power of Two", "power-of-two", E), ("Hamming Distance", "hamming-distance", E)],
        [("Counting Bits", "counting-bits", E)],
        [("Subsets", "subsets", M), ("Maximum Length of a Concatenated String with Unique Characters", "maximum-length-of-a-concatenated-string-with-unique-characters", M)],
        [("Add Binary", "add-binary", E), ("Sum of Two Integers", "sum-of-two-integers", M)],
    ],
    "sorting": [
        [("Sort an Array", "sort-an-array", M), ("Sort List", "sort-list", M), ("Count of Smaller Numbers After Self", "count-of-smaller-numbers-after-self", H), ("Reverse Pairs", "reverse-pairs", H)],
        [("Kth Largest Element in an Array", "kth-largest-element-in-an-array", M), ("K Closest Points to Origin", "k-closest-points-to-origin", M)],
        [("Relative Sort Array", "relative-sort-array", E), ("Sort Colors", "sort-colors", M), ("Maximum Gap", "maximum-gap", M)],
        [("Merge Intervals", "merge-intervals", M), ("Insert Interval", "insert-interval", M), ("Non-overlapping Intervals", "non-overlapping-intervals", M), ("Meeting Rooms", "meeting-rooms", E, P)],
        [("Largest Number", "largest-number", M), ("Sort Characters By Frequency", "sort-characters-by-frequency", M), ("Reorder Data in Log Files", "reorder-data-in-log-files", M)],
        [("Assign Cookies", "assign-cookies", E), ("H-Index", "h-index", M), ("Minimum Number of Arrows to Burst Balloons", "minimum-number-of-arrows-to-burst-balloons", M)],
    ],
    "searching": [
        [("Binary Search", "binary-search", E), ("Guess Number Higher or Lower", "guess-number-higher-or-lower", E), ("Search a 2D Matrix", "search-a-2d-matrix", M)],
        [("First Bad Version", "first-bad-version", E), ("Search Insert Position", "search-insert-position", E), ("Find First and Last Position of Element in Sorted Array", "find-first-and-last-position-of-element-in-sorted-array", M), ("Time Based Key-Value Store", "time-based-key-value-store", M)],
        [("Search in Rotated Sorted Array", "search-in-rotated-sorted-array", M), ("Find Minimum in Rotated Sorted Array", "find-minimum-in-rotated-sorted-array", M), ("Search in Rotated Sorted Array II", "search-in-rotated-sorted-array-ii", M)],
        [("Koko Eating Bananas", "koko-eating-bananas", M), ("Capacity To Ship Packages Within D Days", "capacity-to-ship-packages-within-d-days", M), ("Minimum Number of Days to Make m Bouquets", "minimum-number-of-days-to-make-m-bouquets", M), ("Split Array Largest Sum", "split-array-largest-sum", H)],
        [("Peak Index in a Mountain Array", "peak-index-in-a-mountain-array", M), ("Find Peak Element", "find-peak-element", M)],
    ],
}

DEEP_LC = {
    "arrays": [("Trapping Rain Water", "trapping-rain-water", H)],
    "strings": [("Minimum Window Substring", "minimum-window-substring", H)],
    "linked-lists": [("Reorder List", "reorder-list", M)],
    "trees": [("Binary Tree Maximum Path Sum", "binary-tree-maximum-path-sum", H), ("Construct Binary Tree from Preorder and Inorder Traversal", "construct-binary-tree-from-preorder-and-inorder-traversal", M)],
    "stacks-queues": [("Largest Rectangle in Histogram", "largest-rectangle-in-histogram", H), ("Maximal Rectangle", "maximal-rectangle", H)],
    "graphs": [("Word Ladder", "word-ladder", H), ("Word Ladder II", "word-ladder-ii", H)],
    "dp": [("Longest Increasing Subsequence", "longest-increasing-subsequence", M), ("Russian Doll Envelopes", "russian-doll-envelopes", H)],
    "heaps": [("Kth Largest Element in an Array", "kth-largest-element-in-an-array", M)],
    "hashing": [("Find All Anagrams in a String", "find-all-anagrams-in-a-string", M), ("Permutation in String", "permutation-in-string", M)],
    "bits": [("Single Number II", "single-number-ii", M)],
    "searching": [("Split Array Largest Sum", "split-array-largest-sum", H), ("Capacity To Ship Packages Within D Days", "capacity-to-ship-packages-within-d-days", M)],
}

SD_LC = {
    "sd-caching": ("Build the cache yourself: these are the eviction policies from this page, as coding problems.", [
        ("LRU Cache", "lru-cache", M), ("LFU Cache", "lfu-cache", H), ("Design HashMap", "design-hashmap", E)]),
    "sd-data": ("Small versions of storage-engine ideas: versioned values, snapshots and hashing.", [
        ("Time Based Key-Value Store", "time-based-key-value-store", M), ("Snapshot Array", "snapshot-array", M), ("Design HashSet", "design-hashset", E)]),
    "sd-async": ("Queues and rate limiting, as data-structure design problems.", [
        ("Design Circular Queue", "design-circular-queue", M), ("Logger Rate Limiter", "logger-rate-limiter", E, P),
        ("Design Hit Counter", "design-hit-counter", M, P), ("Design Bounded Blocking Queue", "design-bounded-blocking-queue", M, P),
        ("Moving Average from Data Stream", "moving-average-from-data-stream", E, P)]),
    "sd-reliability": ("Coding problems that mirror ideas from this page: graph-based leader/dependency ordering and time-windowed counting.", [
        ("Course Schedule II", "course-schedule-ii", M), ("Design Hit Counter", "design-hit-counter", M, P), ("Time Based Key-Value Store", "time-based-key-value-store", M)]),
    "sd-cases-1": ("The coding-sized versions of these three designs.", [
        ("Encode and Decode TinyURL", "encode-and-decode-tinyurl", M), ("Logger Rate Limiter", "logger-rate-limiter", E, P),
        ("Design Hit Counter", "design-hit-counter", M, P), ("Web Crawler", "web-crawler", M, P), ("Web Crawler Multithreaded", "web-crawler-multithreaded", M, P)]),
    "sd-cases-2": ("The coding-sized versions of these designs.", [
        ("Design Twitter", "design-twitter", M), ("Design Search Autocomplete System", "design-search-autocomplete-system", H, P),
        ("Implement Trie", "implement-trie-prefix-tree", M), ("Top K Frequent Words", "top-k-frequent-words", M), ("Merge k Sorted Lists", "merge-k-sorted-lists", H)]),
    "sd-interview": ("\"Design a class\" questions that sometimes appear in Google coding rounds. Practice explaining your API choices out loud.", [
        ("Design Browser History", "design-browser-history", M), ("Design Underground System", "design-underground-system", M),
        ("LRU Cache", "lru-cache", M), ("Design File System", "design-file-system", M, P), ("Design Twitter", "design-twitter", M)]),
}
