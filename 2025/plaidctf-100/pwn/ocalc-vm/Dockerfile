FROM --platform=x86_64 alpine@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c

RUN apk add socat gmp
COPY ocalc /problem/ocalc
COPY flag /problem/flag
WORKDIR /problem
ENV OCAMLRUNPARAM=o=10,s=100
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:timeout 120 /problem/ocalc"]