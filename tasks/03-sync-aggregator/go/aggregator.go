// Package aggregator – stub for Concurrent File Stats Processor.
package aggregator

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// Result mirrors one JSON object in the final array.
type Result struct {
	Path   string `json:"path"`
	Lines  int    `json:"lines,omitempty"`
	Words  int    `json:"words,omitempty"`
	Status string `json:"status"` // "ok" or "timeout"
}

func processFile(path string, timeout time.Duration) Result {
	// result := Result{Path: path, Status: "ok"}
	resultChan := make(chan Result, 1)
	errorChan := make(chan error, 1)

	go func() {
		file, err := os.Open(path)
		if err != nil {
			errorChan <- err
			return
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		var lines []string

		if scanner.Scan() {
			firstLine := scanner.Text()
			if strings.HasPrefix(firstLine, "#sleep=") {
				delayStr := strings.TrimPrefix(firstLine, "#sleep=")
				if delay, err := time.ParseDuration(delayStr + "s"); err == nil {
					if delay > timeout {
						errorChan <- fmt.Errorf("sleep duration exceds timeout.")
					}
					time.Sleep(delay)
				}
			} else {
				lines = append(lines, firstLine)
			}
		}

		for scanner.Scan() {
			lines = append(lines, scanner.Text())
		}

		wordCount := 0
		for _, line := range lines {
			wordCount += len(strings.Fields(line))
		}

		resultChan <- Result{
			Path:   path,
			Lines:  len(lines),
			Words:  wordCount,
			Status: "ok",
		}
	}()

	select {
	case res := <-resultChan:
		return res
	case <-errorChan:
		return Result{Path: path, Status: "timeout"}
	// case <-time.After(time.Duration(timeout)):
	// 	return Result{Path: path, Status: "timeout"}
	}
}

// Aggregate must read filelistPath, spin up *workers* goroutines,
// apply a per‑file timeout, and return results in **input order**.
func Aggregate(filelistPath string, workers, timeout int) ([]Result, error) {
	// ── TODO: IMPLEMENT ────────────────────────────────────────────────────────

	file, err := os.Open(filelistPath)
	if err != nil {
		return nil, fmt.Errorf("error opening files : %w", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var paths []string
	for scanner.Scan() {
		path := strings.TrimSpace(scanner.Text())
		if path != "" {
			paths = append(paths, path)
		}
	}

	results := make([]Result, len(paths))
	var wg sync.WaitGroup
	sem := make(chan struct{}, workers)

	for i, path := range paths {
		wg.Add(1)
		sem <- struct{}{}

		go func(idx int, p string) {
			defer wg.Done()
			defer func() { <-sem }()

			res := processFile(p, time.Duration(timeout)*time.Second)
			res.Path = paths[idx]
			results[idx] = res
		}(i, filepath.Join(filepath.Dir(filelistPath), path))
	}

	wg.Wait()

	return results, nil

	// ───────────────────────────────────────────────────────────────────────────
}
