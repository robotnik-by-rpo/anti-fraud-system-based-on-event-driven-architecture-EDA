GOBIN := $(shell go env GOPATH)/bin

#Installing protobuf
proto-download:
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

#Installing grpc
grpc-download:
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Building gRPC file for request
grpc-transaction:
	PATH="$(GOBIN):$$PATH" protoc \
		-I shared/grpc/transaction/proto \
		--go_out=shared/grpc/transaction/gen/go --go_opt=paths=source_relative \
		--go-grpc_out=shared/grpc/transaction/gen/go --go-grpc_opt=paths=source_relative \
		transaction.proto