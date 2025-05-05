FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y openssh-server sudo && \
    mkdir /var/run/sshd

RUN useradd -ms /bin/bash student && \
    echo "student:student" | chpasswd && \
    echo "student ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir /home/student/.ssh && \
    chmod 700 /home/student/.ssh && \
    chown student:student /home/student/.ssh

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]