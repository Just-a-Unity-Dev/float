# float

a simple dice roller bot made for me and my friends. hosted under MIT license.

mostly on maintenance because there's not much stuff you can put in a diceroller bot.

[support me on ko-fi](https://ko-fi.com/raincaldwell)

## how do i host this

float has only been tested on docker. podman may be broken, refer to [this issue for more](https://github.com/Just-a-Unity-Dev/float/issues/1).

### docker

1. install `docker`, `docker-compose` and git by extension
2. clone this repo with git
2.1. checkout the version that suits your need
3. `docker-compose build`
4. `docker run -e TOKEN=<DISCORD_TOKEN> -d float_bot`
5. `history -c` to clear your history so that the token is hidden

### podman

1. install `podman` and relevant
2. clone this repo with git
2.1. checkout the version that suits your need
3. `podman build .`
4. get image id in `podman images`
5. `podman run -e TOKEN=<DISCORD_TOKEN> -d <IMAGE_ID>`
6. `history -c` to clear your history so that the token is hidden
