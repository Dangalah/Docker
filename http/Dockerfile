FROM golang
RUN go get -u github.com/go-sql-driver/mysql
RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN go build -o main 
CMD ["/app/main"]

#port :5000
