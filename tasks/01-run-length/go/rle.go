package rle

import (
	"strconv"
	"strings"
	"unicode/utf8"
)

// Encode returns the run‑length encoding of UTF‑8 string s.
//
// "AAB" → "A2B1"
func Encode(s string) string {
	// TODO: implement
	if len(s) == 0 {
		return ""
	}

	var result strings.Builder
	currentRune, _ := utf8.DecodeRuneInString(s)
	count := 1

	for _, r := range s[utf8.RuneLen(currentRune):] {
		if r == currentRune {
			count++
		} else {
			result.WriteRune(currentRune)
			result.WriteString(strconv.Itoa(count))
			currentRune = r
			count = 1
		}
	}
	result.WriteRune(currentRune)
	result.WriteString(strconv.Itoa(count))

	return result.String()
}
