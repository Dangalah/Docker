package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"

	_ "github.com/go-sql-driver/mysql"
)

func Handler(w http.ResponseWriter, r *http.Request) {
	if !(r.URL.Path == "/" && r.Method == "GET") {
		http.NotFound(w, r)
		return
	}

	word_list := RunQuery()
	data, err := json.Marshal(word_list)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(data)
}

type words struct {
	Word   string
	Number int
}

func RunQuery() []words {
	db, err := sql.Open("mysql", "admin_db:admin_db@(db:3306)/db")
	if err != nil {
		log.Fatal(err)
		return nil
	}

	defer db.Close()

	rows, err := db.Query("select word, number from words")
	if err != nil {
		log.Fatal(err)
		return nil
	}
	defer rows.Close()

	word_list := []words{}

	for rows.Next() {
		w := words{}
		err := rows.Scan(&w.Word, &w.Number)
		if err != nil {
			log.Fatal(err)
			continue
		}
		word_list = append(word_list, w)
	}

	return word_list
}

func main() {
	http.HandleFunc("/", Handler)
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	})

	http.ListenAndServe(":5000", nil)
}
