package counter

import (
	"sync"
	"time"
)

var mu sync.Mutex

var current int64

func NextID() int64 {
	// lock the gorounting
	mu.Lock()
	// after unlock function exit
	defer mu.Unlock()

	id := current
	time.Sleep(0)
	current++
	return id
}
