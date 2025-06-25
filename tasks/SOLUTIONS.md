## Solution notes

### Task 01 – Run‑Length Encoder
- Language: Python
- Approach: The algorithm iterates with groupby,  groupby is group the any element with  key , value formate, key is the charator of group and value is the element group with generator, and then return the string format  key and add the total count, the group value need to iterates because it generator type.
- Why: The efficient using groupby is clear code and the generator type value is save the memory heat
- Time spent: ~20 min

- Language: Go
- Approach: The algorithm it first get current string and then loop the string  with utf8, if current equre item in loop count else add the result new and replace current by item ,
- Why: using utf8 function it get the charactar with byte code
- Time spent: ~25 min
- AI tools used: [ChatGPT]


### Task 02 – Fix‑the‑Bug
- Language: Python
- Approach: This fixed is to prvent paralle call and update the global variable _current, the thread lock is allow one thread and use the "With" the thread is acquire and auto release when the process end, it will prevent to duplicate value in the thread.
- Why:  The thread is running paralle so threads call the same time global variable befor process, so the threas will get the same value and then process, that why the generate id will duplicate.
- Time spent: ~20 min

- Language: Go
- Approach: This fixed is to prvent paralle call and update the global variable _current, the sync.Mutex lock is allow one gorounting and use the defer function it auto unlock when exite function 
- Why:  The gorounting is running paralle so threads call the same time global variable befor process, so the gorouting will get the same value and then process, that why the generate id will duplicate.
- Time spent: ~25 min
- AI tools used: [ChatGPT]

### Task 03 - sync-aggregator
- Language: Python
- Approach: Get the file path list from the filepath file, open file with "with" it will close after with and get the parent path.
 Open the ThreadPoolExecutor to execute the _scan_file in the loop paths wiht enumerate and receive with filedatas dict of iterator pool.sumit(), and then get the result from pool in iterator, if success update the pathe with enum index from Paths list else cach with excetption TimeoutError and update path and status.
 create the _scan_file function to heck file path and open file, read the first line and get the delay value, it will raise if the delay value is exceed then timeout value, if not read lines and words and then count line and words, the result return with dict count and status.
- Why: ThreadPoolExecutor is a concurrent.futures module used to manage a pool of threads for parallel execution of tasks. It's easier to use and best for I/O-bound tasks
- Time spent: ~2 hr
- AI tools used: [ChatGPT]

- Language: Go
- Approach: Get the file path list from the filepath file, open file get the paths list. close file with defer function. use sync.WaitGroup for gorounting it will wait rounting
 write gorounting anonymous function to call the processFile function in the loop paths,
 create the processFile function with result and error go channel than open file and read, get the delay value from the first line of file, if the delay value is exceed then timeout value set to cerror channel, if not read lines and words and then count line and words, after that set to result channel with struct. return with select that is listing the channel to return the result.
- Why: goroutine is a lightweight thread managed by the Go runtime. It allows you to run functions concurrently
- Time spent: ~2 hr
- AI tools used: [ChatGPT]

### Task 04 - sql-reasoning
- Language: Python
- Approach:  Select subquery using WITH for the scope and amount_thb to temp scope_pledges WITH create object table and then select the row and count from scope_pledges with window functions to temp ranked_pledges after select scope and p90_thb of ceil(0.9 * n) and order the global first
- Why: Raw data is required for get global and Thai scores. build table object scope_pledges that include global and thailand row and build rank table for score that select row count and number base on raw table, so the data row is ready for score.
- Time spent: ~12 min
- AI tools used: [ChatGPT]

- Language: Go
- Approach:  Select subquery using WITH for the scope and amount_thb to temp scope_pledges WITH create object table and then select the row and count from scope_pledges with window functions to temp ranked_pledges after select scope and p90_thb of ceil(0.9 * n) and order the global first
- Why: Raw data is required for get global and Thai scores. build table object scope_pledges that include global and thailand row and build rank table for score that select row count and number base on raw table, so the data row is ready for score.
- Time spent: ~12 min
- AI tools used: [ChatGPT]
