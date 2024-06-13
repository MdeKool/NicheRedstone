FROM ubuntu:latest
LABEL authors="mdk"

ENTRYPOINT ["top", "-b"]