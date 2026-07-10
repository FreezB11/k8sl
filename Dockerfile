FROM alpine:3.22

RUN apk add --no-cache bash build-base cmake git iproute2 \
    iputils tcpdump curl gdb strace util-linux

WORKDIR /app

# COPY . .

# RUN make

# ENTRYPOINT ["/app/bin/dfs"]
# CMD ["sh"]
CMD ["sleep", "infinity"]