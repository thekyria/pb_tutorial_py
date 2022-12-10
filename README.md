# Prerequisites

- Install [Docker](https://docs.docker.com/get-docker/) for your platform.

# Create a Dockerfile 

A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image.

`Dockerfile` sytax help:
-  The `# syntax` directive defines the location of the Dockerfile syntax that is used to build the `Dockerfile`.
-  `ARG` sets up a variable to be passed at build-time to the builder. This can be later be used like `${CODE_VERSION}` in the `FROM` line.
- `FROM` this is the basic container that your container is going to be based on. [Kali Linux](https://www.kali.org/blog/official-kali-linux-docker-images/) is used here as a base image just as an example.
- `LABEL` key-value pairs of metadata for your container. This can later be inspected with `docker image inspect --format='' myimage`.
- `SHELL` defines the default shell for the container. In Linux by default it is `SHELL ["/bin/sh", "-c"]` (included in the example `Dockerfile` above for educational purposes).
-  `RUN` will execute commands in a new layer on top of the current image and commit the results. The result will be used for any next step in the Dockerfile.
-  `WORKDIR` sets the working directory fory any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it.

For a complete reference of Dockerfiles see here: https://docs.docker.com/engine/reference/builder/

# Build the image

To create a docker image you need to build your `Dockerfile`. This is done by the Docker daemon, not by the CLI. The CLI passes the build context to the daemon with the following command.

```bash
docker build -f ./Dockerfile -t thekyria/thekali:latest .
```

WARNING: In the above, `./Dockerfile` asusmes Linux path naming.

Syntax help for docker build:
- `-f` specifies the Dockerfile location. If omitted, the default location is `./Dockerfile`.
- `-t` specifies a repository (`thekyria/thekali`) and a version (`latest`) to tag the image with.
- `.` is the context of the `docker build` command.

If you want to not consider cached layers when building you can include the flag `--no-cache`. 
If you want to always attempt to pull a latest version of the underlying (i.e. `FROM`) image when building you can include the flag `--pull`.

If everything is successfull, you should be able to see your new image.

```bat
PS > docker images
REPOSITORY                    TAG              IMAGE ID       CREATED          SIZE
thekyria/thekali              latest           8b77b2f4032d   13 minutes ago   265MB
```

It is a good practice to include a `.dockerignore` file in the directory of your `Dockerfile`. Patterns matched in `.dockerignore` (in a similar fashion as for `.gitignore`) will be excluded from the build context (i.e. `.` in the above example).

# Run the image 

## In foreground mode 

You can start the container with:

```bash
docker run -i -t --name kali1 thekyria/thekali:latest bash
```

Explanation of the docker run command:
- `-i` flag directs STDIN of the host into the container.
- `-t` flag gives you TTY to the docker container as if you were inside the shell of the container. The combination of `i` and `t` gives access the the prompt of the container.
- `--name kali1` gives the name `kali1` to the container instance. This can be seen in `docker ps`. If the `--name` is not specified, a random name is generated upon `docker run` execution, e.g. `lucid_dewdney`.
- `thekyria/thekali:latest` specify the image to run
- `bash` specifies the command to run in the container

For a complete reference on the run command see here: 
https://docs.docker.com/engine/reference/run/

This will bring you in the bash of the container.

```bash
┌──(root㉿b254622c25d6)-[/home/kali]
└─#
```

From another cmd on the host, you can verify that the container is running with:

```bash
PS > docker ps
CONTAINER ID   IMAGE                     COMMAND       CREATED         STATUS         PORTS     NAMES
b254622c25d6   thekyria/thekali:latest   "/bin/bash"   3 seconds ago   Up 4 seconds             xenodochial_newton
```

## In detached (background) mode

A container can be started in detached mode. 

```bash
docker run -it -d thekyria/thekali:latest bash
```

The above will start the container, launch the `bash` command in the container, and return to the prompt in the host. You can verify that an image is running with the `docker ps` command.

The `-it` flag is a combination of `-i`, `-t`. It is still needed 

We can attach to (the process running in the) container with:

```bash
docker attach ff506a507bbd
```

Where `ff506a507bbd`  is the `CONTAINER ID` as shown by the `docker ps` command.

## Start, stop, and attach

The `CONTAINER_ID` can be used to start and stop containers.

```bash
docker run -i -t -d thekyria/thekali:latest bash
docker run -i -t -d thekyria/thekali:latest bash
docker ps
```

The above will list two containers, based off the same image, in running state.

We can stop them:

```bash
docker stop 3f8447557f1b
docker stop f6872f405f0b
```

Now the output list of `docker ps` will be empty. We should look into `docker ps -a` for the stopped containers.

We can start them again with:

```bash
docker start 3f8447557f1b
docker start f6872f405f0b
```

Once they have been restarted, we can attach host prompts to the containers with 

```bash
docker attach 3f8447557f1b
```

And from another bash: 

```bash
docker attach f6872f405f0b
```


# Networking


## Ping from container to container 

Start two containers.

```bash
docker run -i -t -d --name kali1 --network="bridge" --rm thekyria/thekali:latest bash
docker run -i -t -d --name kali2 --network="bridge" --rm thekyria/thekali:latest bash
```

The `--network="bridge"` flag creates a network stack on the default Docker bridge (this is the default behavior). Alternative options (e.g. "none", "host", etc.) are available [here](https://docs.docker.com/engine/reference/run/#network-settings).

The docker pseudonetworks can be examined on the host with:

```bash
docker network ls
```

More information on the `bridge` network can be seen with:

```bash
docker network inspect bridge
```

Attach to the two containers from different prompts on the host. Check the IP addresses with `ip a`. On one of the two start `tcpdump` and on the other ping the first  with `ping <ip-address>`.

For the above to work, make sure `ping` and `tcpdump` are installed on the image(s) that you use.

A similar walkthrough can be found under:
https://docs.docker.com/network/network-tutorial-standalone/

## Ping from the host to a container

In Windows there is not a `docker0` bridge interface and therefore linux containers cannot be pinged. See also:
https://docs.docker.com/desktop/windows/networking/



# Housekeeping 

## Containers 

When you start a container without the `--rm` flag it persists after exiting/stopping. List all containers in the system with:

```bash
docker ps -a
```

You can prune all stopped containers with:

```bash
docker container prune
```


## Images 

Prune unused images with:

```bash
docker image prune
```
This will clean up all dangling images, i.e. not tagged and not reference by any container.

A deeper cleanup is possible with:

```bash
docker image prune -a
```


# Protocol buffers

Protocol buffers are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data – think XML, but smaller, faster, and simpler. You define how you want your data to be structured once, then you can use special generated source code to easily write and read your structured data to and from a variety of data streams and using a variety of languages.

All pages under this one are worth it.
https://developers.google.com/protocol-buffers/docs/overview
Especially interesting is the Encoding page.

## C++ Tutorial

From here: https://developers.google.com/protocol-buffers/docs/cpptutorial

Create a `.proto` file.

```protoc
syntax = "proto2";

package tutorial;

message Person {
  optional string name = 1;
  optional int32 id = 2;
  optional string email = 3;

  enum PhoneType {
    MOBILE = 0;
    HOME = 1;
    WORK = 2;
  }

  message PhoneNumber {
    optional string number = 1;
    optional PhoneType type = 2 [default = HOME];
  }

  repeated PhoneNumber phones = 4;
}

message AddressBook {
  repeated Person people = 1;
}
```


## Manually generating .c and .h files

Run the `protoc` compiler to your `.proto` file.

```powershell
protoc.exe --proto_path=. --cpp_out=. .\addressbook.proto
```

You should now have a `.pb.h` and a `.pb.c`  in your output directory.



# Applications in containers

An application can copied over to a container through `Dockerfile` `COPY` commands and can be run from there via a combination of `ENTRYPOINT` and `CMD` commands.

The sourcefiles of this example can be found in this repo. Two python sibling applications (server-client) have been created that can exchange UDP messages. The payload of the exchanged message is serialized using [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/pythontutorial).

## Protocol Buffers and Python

A basic protocol description has been created in `simple_message.proto`.

```
syntax = "proto2";

package thepb;

message simple_message {
    optional int32 opcode = 1;
    optional string payload = 2;
    optional int32 crc32 = 3;
}
```

The corresponding `.py` file can be created by parsing the `.proto` definition with `protoc` (as seen in `Dockerfile:32`):

```bash
protoc --proto_path=. --python_out=. simple_message/simple_message.proto
```

The output `simple_message_pb2.py` is imported and used where needed. Example excerpt from `udp_client.py`.

```python
...
from simple_message import simple_message_pb2
...
message_tx = simple_message_pb2.simple_message()
message_tx.opcode = 11
message_tx.payload = payload
message_tx.crc32 = crc32.calculate_crc(payload)
...
rx_tx_socket.sendto(message_tx.SerializeToString(), (_target_ip, _target_port))
...
```

## New dockerfiles for a server and a client

Two new `Dockerfiles` are generated:
- `Dockerfile.server` corresponding to the "server" application of the example, and
- `Dockerfile.client` corresponding to the client.

```dockerfile
# syntax=docker/dockerfile:1

ARG CODE_VERSION=latest
FROM thekyria/thekali:${CODE_VERSION}

ENTRYPOINT ["/home/kali/udp_client.py"]
CMD ["-a", "172.17.0.2", "-p", "20212"]
```

Syntax help:
- `FROM` basically denoting that this image is extending the one from `thekyria/thekali` before
- `ENTRYPOINT` (exec form) is the command that is automatically executed when the corresponding image is run with a `docker run`. 
- `CMD` (exec form) is the command that will execute right after the `ENTRYPOINT`. 
In total the command that will be executed upon running the container is `ENTRYPOINT + CMD`.

We can build the two images with:

```bash
docker build -f ./Dockerfile -t thekyria/thekali:latest .
docker build -f ./Dockerfile.server -t thekyria/udp_server:latest .
docker build -f ./Dockerfile.client -t thekyria/udp_client:latest .
```

WARNING: In the above, `./Dockerfile` asusmes Linux path naming.

Notice that before we build `Dockerfile.server` or `Dockerfile.client` we need to make sure that `thekyria/thekali` is up to date (first `build` command).

We can run containers from the two images (on separate prompts).

```bash
docker run -i -t --name udp_server1 --network="bridge" --rm thekyria/udp_server:latest 20211
```

```bash
docker run -i -t --name udp_client1 --network="bridge" --rm thekyria/udp_client:latest -a 172.17.0.2 -p 20211
```

Let's examine the first command:
- A container named `udp_server1` is started from the image `thekyria/udp_client:latest`
- The container is attached to docker network `bridge`.
- An interactive shell is started to the container (`-i -t`).
- The daemon is notified to delete the container after it exits (`-rm`).
- Since the container is `run`, it starts by executing its `ENTRYPOINT`, i.e. `/home/kali/udp_server.py -p`, as seen in `Dockerfile.server`
- The last part of the command `20211`, is the part where the `CMD` default of `["20212"]` (of `Dockerfile.server`) is overriden. The full command that will be executed in the container when it is run will be: `ENTRYPOINT + CMD` = `/home/kali/udp_server.py -p 20211`.

Analogous explanations hold for the second command. `172.17.0.2` has been chosen to match the Docker `bridge` network IP address of container `udp_server1`. This is to initialize the sample UDP client application to target a valid IP (through the `-a` argparse argument of `udp_client.py`).

We can see that the two containers can communicate to each other.

_udp_client1_
```bash
udp_client[1024] :20212 -> 172.17.0.2:20212
input message payload: asdf
tx (172.17.0.2:20212): | 11 | asdf | 1361703869 |
rx (172.17.0.2:20212): ACK | 11 | asdf | 1361703869 |
```

_udp_server1_
```bash
udp_server[1024] 0.0.0.0:20212
rx (('172.17.0.3', 20212)): | 11 | asdf | 1361703869 | (raw: b'\x08\x0b\x12\x04asdf\x18\xbd\xe7\xa7\x89\x05')
tx (('172.17.0.3', 20212)): ACK | 11 | asdf | 1361703869 |
```

## Overriding ENTRYPOINT and CMD

The entrypoint can be overriden with `docker run --entrypoint XXX`. For example, we can always start a bash in our container with:

```bash
docker run -i -t --name udp_client1 --network="bridge" --rm --entrypoint bash thekyria/udp_client:latest
```

A more thorough description of `ENTRYPOINT` and `CMD` can be found [here](https://www.ctl.io/developers/blog/post/dockerfile-entrypoint-vs-cmd/).

# docker compose

[Compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications, quite similar to what we want to do in this case. 

The way services are defined is through a YAML file, the `docker-compose.yaml`.

Syntax help:
- `version` is the version of the `docker-compose` `yaml` syntax.
- `networks` defines [networks](https://docs.docker.com/compose/networking/) for our deployment. `driver: bridge` refers to the type of the underlying Docker network stack as explained in a [previous section](#networking). We will use `udpexample` to connect our services to.
- `services` is the section where our containers are specified. In this example we have three: `base`, `udp_server` and `udp_client`. The reason `base` (dummy service) is needed is that the images of the latter two services (i.e. `thekyria/udp_server`, `thekyria/udp_client`) depend on image `thekyria/thekali`. This service-image dependency is declared with `depends_on:`.
-  For each service:
  - `image` specifies the image needed for the service.
  - `build` gives the instructions on how to build the image. When both `image` and `build` are specified, then compose names the built image according to the `image` value. Substatements `context` and `dockerfile` are the equivalents of `docker build` command flags (e.g. `-f ./Dockerfile`).
  - `networks` section points to the `udpexample` network defined before and assignes an ip for the container from the subnet defined in the network; this is analogous to the `docker run` command flag `--network="bridge"`. `network_mode` complements _how_ the container will be connected to the network.
  - `tty` and `stdin_open` are the compose equivalents of `docker run` flags `-i -t`.
  - `entrypoint` and `command` are related to the `Dockerfile` keywords `ENTRYPOINT` and `CMD` (or equivalently with the `docker run --entrypoint ENTRYPOINT myimage COMMAND` )

Putting everything together we see that indeed the command executed under the hood for the `udp_server` is something like:

```bash
docker run -it --network=udpexample --entrypoint "/home/kali/udp_server.py -p" thekyria/udp_server:latest 20212
```

A complete reference on compose files can be [here](https://docs.docker.com/compose/compose-file/compose-file-v3/).


## Environment variables

The `.env` file is used to set [environment variables](https://docs.docker.com/compose/environment-variables/)

```ini
CLIENT_IP=10.1.0.3
```

which are then available to `docker-compose.yaml`,e.g.

```yaml
ipv4_address: ${CLIENT_IP}
```

The default filename that `docker compose` will search for environment variables is `.env` but this can be overriden:

```bash
docker compose --env-file ./path/to/.env.file up 
```

You can test that substitution of the environment variables happens correctly with:

```bash
docker compose config
```

## Execute docker compose 

While in the same folder as `docker-compose.yaml`, execute:

```bash
docker compose up -d
```

The `up` [command](https://docs.docker.com/compose/reference/up/) builds, (re)creates, starts, and attaches to containers for a service. Unless they are already running, this command also starts any linked services.

You can only build (and not run them) the images defined in the compose file with `docker compose build` instead..

The `-d` flag tells compose to start in a detached mode, again similar to the `docker run -d` flag. 

You can verify that two containers started with either:

```bash
docker ps
```

```bash
$ docker compose ps
NAME                    COMMAND                  SERVICE             STATUS
   PORTS
pb_tutorial_py-base-1   "bash"                   base                exited (0)

udp_client1             "/home/kali/udp_clie…"   udp_client          running

udp_server1             "/home/kali/udp_serv…"   udp_server          running
```

We can see that `base` service was only used to build the image, and the corresponding `pb_tutorial_py-base-1` container is not running. We can attach to any of the other two containers and verify their behavior.

```bash
$ docker attach udp_client1

tx (10.1.0.2:20212): | 11 |  | 0 |
rx (10.1.0.2:20212): ACK | 11 |  | 0 |
input message payload: asdf
tx (10.1.0.2:20212): | 11 | asdf | 1361703869 |
rx (10.1.0.2:20212): ACK | 11 | asdf | 1361703869 |
input message payload:
```

The compose containers can be stopped with:

```bash
docker compose down
```

Cleanup corresponding images, containers and volumes can be done:

```bash
docker compose rm -fsv
```

This is the equivalent of the `-rm` flag in the `docker run` command.


## V1 vs V2 compose 

- `docker-compose` is the V1 version of the command
- `docker compose` is the [V2](https://docs.docker.com/compose/cli-command/) version of the command (starting Docker Desktop version  3.4.0 - check your version with `docker version`).

In all commands in this example, either can be used, i.e. by using the dash "-" or not.
